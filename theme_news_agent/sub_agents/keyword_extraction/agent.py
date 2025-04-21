from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
import logging

logger = logging.getLogger(__name__)

class KeywordExtractionAgent(LlmAgent):
    """
    수집된 데이터에서 주요 키워드를 추출하는 LLM 기반 에이전트입니다.
    """
    def __init__(
        self,
        name: str = "KeywordExtractor",
        description: str = "텍스트에서 주요 키워드를 추출하는 에이전트",
        model: str = "gemma-3-27b-it", # 사용할 LLM 모델 지정
        instruction: str = "입력된 텍스트에서 주요 키워드(인물, 조직, 이벤트, 제품, 기술, 주제 명사구 등)를 추출하고 JSON 형식의 문자열 리스트로 반환해 주세요. 예: [\"키워드1\", \"키워드2\", ...]", # 기본 지침
        # TODO: prompt.py에서 프롬프트를 로드하도록 수정
    ):
        super().__init__(
            name=name,
            description=description,
            model=model,
            instruction=instruction,
        )

    def process(self, ctx: InvocationContext) -> str:
        """
        데이터 수집 결과를 받아 키워드 추출을 수행하고 상태를 업데이트합니다.
        """
        logger.info(f"Executing {self.name} agent...")
        collected_data = ctx.state.get("collected_data")

        if not collected_data:
            error_msg = "키워드 추출을 위한 수집된 데이터(collected_data)가 상태에 없습니다."
            logger.error(error_msg)
            return f"오류: {error_msg}"

        # TODO: 3.3 에이전트 로직 구현 - LLM 입력 생성 및 호출, 결과 파싱
        # 1. collected_data에서 LLM 입력 생성 (title, content 조합)
        # 2. self.generate_content() 호출
        # 3. 결과 파싱 (JSON 리스트 확인)
        # 4. ctx.state["keyword_results"] 업데이트 (다음 단계에서 빈도 계산 후)

        # 임시 반환 메시지
        temp_keywords = ["임시 키워드 1", "임시 키워드 2"] # 실제 LLM 결과로 대체 필요
        ctx.state["extracted_keywords_raw"] = temp_keywords # 임시로 상태 저장 (빈도 계산 전)
        logger.info(f"키워드 추출 완료 (임시): {len(temp_keywords)}개")

        return f"키워드 추출 완료 (임시): {len(temp_keywords)}개 키워드 추출됨."
