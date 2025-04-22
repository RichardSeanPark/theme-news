import pytest
from theme_news_agent.sub_agents.keyword_extraction.prompt import get_extraction_prompt, DEFAULT_EXTRACTION_PROMPT

def test_get_extraction_prompt_basic():
    """get_extraction_prompt 함수가 기본 프롬프트 구조와 입력 텍스트를 포함하는지 확인합니다."""
    test_text = "AI 기술이 발전하고 있습니다."
    prompt = get_extraction_prompt(test_text)

    assert prompt is not None, "프롬프트가 생성되지 않았습니다."
    assert isinstance(prompt, str), f"반환된 프롬프트 타입이 문자열이 아닙니다: {type(prompt)}"

    # 기본 프롬프트 구조 포함 확인
    assert "다음 텍스트에서 주요 키워드를 추출해 주세요." in prompt, "기본 지침 누락"
    assert "텍스트:\n---\n" in prompt, "텍스트 섹션 구분자 누락"
    assert "\n---\n\n추출된 키워드 (JSON 리스트):" in prompt, "키워드 섹션 구분자 누락"

    # 입력 텍스트 포함 확인
    assert test_text in prompt, "입력 텍스트가 프롬프트에 포함되지 않았습니다."

    # 포맷팅 확인 (단순 테스트)
    assert "{text}" not in prompt, "{text} 플레이스홀더가 제거되지 않았습니다." 