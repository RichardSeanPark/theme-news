import pytest
from theme_news_agent.sub_agents.keyword_extraction.agent import KeywordExtractionAgent


def test_keyword_extraction_agent_initialization():
    """KeywordExtractionAgent 객체가 기본 인자로 정상적으로 생성되는지 확인합니다."""
    try:
        agent = KeywordExtractionAgent()
        assert agent is not None, "KeywordExtractionAgent 객체 생성에 실패했습니다."
    except Exception as e:
        pytest.fail(f"KeywordExtractionAgent 초기화 중 예외 발생: {e}")

def test_keyword_extraction_agent_attributes():
    """KeywordExtractionAgent 객체 생성 시 속성이 올바른 값으로 설정되었는지 확인합니다."""
    agent = KeywordExtractionAgent()
    assert agent.name == "KeywordExtractor", f"Expected name 'KeywordExtractor', but got '{agent.name}'"
    assert agent.description == "텍스트에서 주요 키워드를 추출하는 에이전트", \
           f"Expected description '텍스트에서 주요 키워드를 추출하는 에이전트', but got '{agent.description}'"
    assert agent.model == "gemma-3-27b-it", f"Expected model 'gemma-3-27b-it', but got '{agent.model}'"
    expected_instruction = "입력된 텍스트에서 주요 키워드(인물, 조직, 이벤트, 제품, 기술, 주제 명사구 등)를 추출하고 JSON 형식의 문자열 리스트로 반환해 주세요. 예: [\"키워드1\", \"키워드2\", ...]"
    assert agent.instruction == expected_instruction, \
           f"Expected instruction '{expected_instruction}', but got '{agent.instruction}'" 