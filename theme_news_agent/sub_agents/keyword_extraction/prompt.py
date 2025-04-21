"""
KeywordExtractionAgent를 위한 프롬프트를 정의합니다.
"""

# TODO: 다양한 프롬프트 전략(예: Few-shot)을 실험하고 최적화할 수 있도록 구조화합니다.

# 기본 키워드 추출 프롬프트
DEFAULT_EXTRACTION_PROMPT = (
    "다음 텍스트에서 주요 키워드를 추출해 주세요.\n"
    "키워드는 인물, 조직, 장소, 이벤트, 제품, 기술, 특정 주제를 나타내는 명사 또는 명사구여야 합니다.\n"
    "추출된 키워드들을 JSON 형식의 문자열 리스트로 반환해 주세요.\n"
    "예시: [\"인공지능\", \"머신러닝\", \"구글\", \"알파고\"]\n\n"
    "텍스트:\n"
    "---\n"
    "{text}\n"
    "---\n\n"
    "추출된 키워드 (JSON 리스트):"
)

def get_extraction_prompt(text: str) -> str:
    """
    주어진 텍스트를 포함하는 키워드 추출 프롬프트를 생성합니다.

    Args:
        text: 키워드를 추출할 원본 텍스트.

    Returns:
        LLM에게 전달될 완전한 프롬프트 문자열.
    """
    # TODO: 텍스트 길이 제한 및 청킹 전략 추가 고려
    return DEFAULT_EXTRACTION_PROMPT.format(text=text)
