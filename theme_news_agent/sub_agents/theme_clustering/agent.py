import json
import logging
from google.adk.agents.llm_agent import LlmAgent
from .prompt import get_clustering_prompt # 프롬프트 생성 함수 임포트

# TODO: 프롬프트 로딩 로직 추가 (4.2단계)
# from .prompt import get_clustering_prompt

# 로거 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 기본 로깅 레벨 설정

class ThemeClusteringAgent(LlmAgent):
    """
    키워드 목록을 입력받아 의미적으로 유사한 키워드를 그룹화하고,
    각 그룹에 테마 이름을 할당하는 LLM 기반 에이전트입니다.
    """
    def __init__(self):
        super().__init__(
            name='theme_clustering_agent',
            model='gemini-1.5-flash-latest', # TODO: 모델명은 필요시 설정에서 로드하도록 변경 가능
            instruction="당신은 키워드 목록을 분석하여 의미적으로 연관된 키워드들을 그룹화하고 각 그룹에 적절한 테마 이름을 부여하는 전문가입니다. 입력된 키워드와 언급량 데이터를 기반으로 테마 클러스터링을 수행하고, 지정된 JSON 형식으로 결과를 반환해야 합니다.",
            description="키워드 클러스터링 및 테마 이름 생성 에이전트"
        )

    async def process(self, ctx):
        """
        키워드 데이터를 로드하고, 클러스터링 프롬프트를 생성하여 반환합니다.
        (ADK 프레임워크가 이 프롬프트를 사용하여 LLM 호출을 수행할 것으로 예상)
        """
        logger.info("테마 클러스터링 에이전트 시작...")
        keyword_results = ctx.state.get("keyword_results")

        if not keyword_results:
            logger.warning("상태에서 'keyword_results'를 찾을 수 없거나 비어 있습니다.")
            # 오류 상황을 어떻게 처리할지 ADK 정책 확인 필요 (예: 예외 발생, 특정 메시지 반환)
            # 여기서는 이전과 같이 메시지 반환
            return "키워드 추출 결과가 없어 테마 클러스터링을 진행할 수 없습니다."

        # LLM 입력 생성
        try:
            prompt = get_clustering_prompt(keyword_results)
            logger.info("클러스터링 프롬프트 생성 완료.")
            return prompt # 생성된 프롬프트를 반환
        except Exception as e:
            logger.error(f"클러스터링 프롬프트 생성 중 오류 발생: {e}", exc_info=True)
            # 프롬프트 생성 실패 시 오류 메시지 반환
            return f"클러스터링 프롬프트 생성 중 오류 발생: {e}"
