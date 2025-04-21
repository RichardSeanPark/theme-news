import json # JSON 파싱을 위해 추가
import logging
import asyncio # 추가
import re # 정규식 사용을 위해 임포트

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.models.llm_request import LlmRequest # 추가
from google.genai import types # 추가
# 데이터 모델 및 프롬프트 임포트 추가
from theme_news_agent.sub_agents.data_collection.models import CollectedData, ArticleData
from .prompt import get_extraction_prompt

logger = logging.getLogger(__name__)

class KeywordExtractionAgent(LlmAgent):
    """
    수집된 데이터에서 주요 키워드를 추출하는 LLM 기반 에이전트입니다.
    """
    def __init__(
        self,
        name: str = "KeywordExtractor",
        description: str = "텍스트에서 주요 키워드를 추출하는 에이전트",
        model: str = "gemini-2.5-flash", # 사용할 LLM 모델 지정 (gemini-2.5-flash로 변경)
        instruction: str = "", # instruction은 프롬프트 함수에서 관리하므로 빈 문자열 또는 None 설정 가능
        # TODO: prompt.py에서 프롬프트를 로드하도록 수정 -> instruction 제거 또는 다른 용도로 활용 고려
    ):
        super().__init__(
            name=name,
            description=description,
            model=model,
            instruction=instruction, # instruction 대신 prompt_template 또는 유사 개념 사용 고려
        )

    # process 메서드를 비동기로 변경 (LLM 호출을 위해)
    async def process(self, ctx: InvocationContext) -> str:
        """
        데이터 수집 결과를 받아 키워드 추출을 수행하고 상태를 업데이트합니다.
        """
        logger.info(f"[{self.name}] 에이전트 실행 시작...") # 로그 추가
        collected_data_dict = ctx.state.get("collected_data")

        if not collected_data_dict:
            error_msg = "키워드 추출을 위한 수집된 데이터(collected_data)가 상태에 없습니다."
            logger.error(f"[{self.name}] {error_msg}") # 로그 추가
            # 상태에 오류 플래그 또는 메시지 저장 고려
            return f"오류: {error_msg}"
        logger.debug(f"[{self.name}] 상태에서 collected_data 로드 완료.") # 로그 추가

        try:
            # Pydantic 모델로 로드하여 데이터 접근 용이성 확보
            collected_data = CollectedData(**collected_data_dict)
            all_articles = collected_data.get_all_articles()
            logger.debug(f"[{self.name}] CollectedData 파싱 완료. 총 {len(all_articles)}개 기사 확인.") # 로그 추가
        except Exception as e:
            error_msg = f"collected_data 로드 또는 파싱 중 오류 발생: {e}"
            logger.exception(f"[{self.name}] {error_msg}") # 로그 추가
            return f"오류: {error_msg}"

        if not all_articles:
            msg = "키워드를 추출할 기사가 없습니다."
            logger.warning(f"[{self.name}] {msg}") # 로그 추가
            ctx.state["extracted_keywords_raw"] = [] # 빈 리스트 저장
            return msg

        # 1. collected_data에서 LLM 입력 생성 (모든 title, content 조합)
        # TODO: 매우 긴 텍스트 처리 전략 필요 (예: 청킹, 요약 후 추출)
        input_text = "\n\n".join(
            f"{article.title}\n{article.content or ''}" for article in all_articles
        ).strip()
        logger.debug(f"[{self.name}] LLM 입력 텍스트 생성 완료 (길이: {len(input_text)}).") # 로그 추가

        if not input_text:
            msg = "LLM에 입력할 텍스트 콘텐츠가 없습니다."
            logger.warning(f"[{self.name}] {msg}") # 로그 추가
            ctx.state["extracted_keywords_raw"] = []
            return msg

        # 프롬프트 생성
        prompt = get_extraction_prompt(input_text)
        # 여러 줄 f-string을 위해 삼중 따옴표 사용 및 주석 위치 조정
        logger.debug(f"""[{self.name}] 프롬프트 생성 완료:
--- 프롬프트 시작 ---
{prompt[:500]}...
--- 프롬프트 끝 ---""") # 로그 추가 (일부만)

        # 2. self.generate_content() 호출
        logger.info(f"[{self.name}] LLM ({self.model}) 호출하여 키워드 추출 시작...") # 로그 추가
        llm_response_text = "" # 초기화
        try:
            # canonical_model을 통해 LLM 객체에 접근하고 generate_content_async 호출
            llm_request = LlmRequest(contents=[types.Content(parts=[types.Part(text=prompt)], role="user")]) # LlmRequest 수정
            response_generator = self.canonical_model.generate_content_async(llm_request)

            # 스트리밍이 아니므로 첫 번째 응답만 사용 (ADK 기본 동작 가정)
            async for response_part in response_generator:
                llm_response_text = response_part.text # LlmResponse 객체의 text 속성 사용
                break # 첫 응답만 받고 종료

            if not llm_response_text:
                 logger.warning(f"[{self.name}] LLM으로부터 빈 응답을 받았습니다.")
                 llm_response_text = "[]" # 빈 응답 시 기본값 설정

            logger.info(f"[{self.name}] LLM 응답 수신 완료.")
            logger.debug(f"""[{self.name}] LLM Raw 응답:
--- 응답 시작 ---
{llm_response_text[:500]}...
--- 응답 끝 ---""")
        except Exception as e:
            error_msg = f"LLM 호출 중 오류 발생: {e}"
            logger.exception(f"[{self.name}] {error_msg}")
            ctx.state["extracted_keywords_raw"] = []
            return f"오류: {error_msg}"

        # 3. 결과 파싱 (JSON 리스트 확인)
        logger.debug(f"[{self.name}] LLM 응답 파싱 시작...")
        extracted_keywords = []
        json_part = None # 추출된 JSON 문자열 저장 변수
        try:
            # 정규식을 사용하여 JSON 부분 추출 시도
            # 1. ```json ... ``` 패턴 찾기
            match = re.search(r"```json\s*(\[.*?\])\s*```", llm_response_text, re.DOTALL)
            if match:
                json_part = match.group(1).strip()
            else:
                # 2. ``` ... ``` 패턴 찾기 (내용이 리스트 형태일 경우)
                match = re.search(r"```\s*(\[.*?\])\s*```", llm_response_text, re.DOTALL)
                if match:
                    json_part = match.group(1).strip()
                else:
                    # 3. 코드 블록 없이 [ ... ] 패턴만 찾기
                    match = re.search(r"^\s*(\[.*?\])\s*$", llm_response_text, re.DOTALL)
                    if match:
                       json_part = match.group(1).strip()

            if json_part:
                extracted_keywords = json.loads(json_part)
                if not isinstance(extracted_keywords, list):
                    raise ValueError("파싱된 결과가 리스트 타입이 아닙니다.")
                if not all(isinstance(item, str) for item in extracted_keywords):
                    raise ValueError("리스트 내 요소가 모두 문자열 타입이 아닙니다.")
                logger.info(f"[{self.name}] LLM 응답 파싱 성공: {len(extracted_keywords)}개 키워드 추출됨.")
            else:
                # JSON 부분을 찾지 못한 경우
                logger.warning(f"[{self.name}] LLM 응답에서 유효한 JSON 리스트를 찾지 못했습니다. 원본 응답: {llm_response_text[:200]}...")
                # 추가: 유효하지 않은 JSON이라도 파싱 시도해보기 (오류 로깅 목적)
                try:
                    json.loads(llm_response_text.strip())
                except json.JSONDecodeError as decode_error:
                     logger.error(f"[{self.name}] 원본 응답 직접 파싱 시도 실패: {decode_error}")

        except (json.JSONDecodeError, ValueError) as e:
            error_msg = f"LLM 응답 처리 중 오류 발생: {e}. 추출된 JSON 파트: {json_part[:200] if json_part else 'N/A'}... 원본 응답: {llm_response_text[:200]}..."
            logger.error(f"[{self.name}] {error_msg}")
            extracted_keywords = []

        # 4. ctx.state["extracted_keywords_raw"] 업데이트
        ctx.state["extracted_keywords_raw"] = extracted_keywords
        logger.info(f"[{self.name}] 추출된 원본 키워드 ({len(extracted_keywords)}개)를 상태에 저장했습니다.")

        return f"키워드 추출 완료: {len(extracted_keywords)}개 키워드 추출됨 (파싱 성공 여부 확인 필요)."
