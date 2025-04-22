import pytest
from theme_news_agent.sub_agents.theme_clustering.agent import ThemeClusteringAgent

def test_theme_clustering_agent_creation():
    """
    테스트 케이스 4.1.1: ThemeClusteringAgent 객체 생성 확인
    """
    try:
        agent = ThemeClusteringAgent()
        assert isinstance(agent, ThemeClusteringAgent)
    except Exception as e:
        pytest.fail(f"ThemeClusteringAgent 생성 중 예외 발생: {e}")

def test_theme_clustering_agent_init_attributes():
    """
    테스트 케이스 4.1.2: __init__ 속성 확인
    """
    agent = ThemeClusteringAgent()

    # 예상값 설정 (agent.py의 __init__과 일치해야 함)
    expected_model = 'gemini-1.5-flash-latest'
    expected_instruction = "당신은 키워드 목록을 분석하여 의미적으로 연관된 키워드들을 그룹화하고 각 그룹에 적절한 테마 이름을 부여하는 전문가입니다. 입력된 키워드와 언급량 데이터를 기반으로 테마 클러스터링을 수행하고, 지정된 JSON 형식으로 결과를 반환해야 합니다."
    expected_description = "키워드 클러스터링 및 테마 이름 생성 에이전트"

    assert agent.model == expected_model
    assert agent.instruction == expected_instruction
    assert agent.description == expected_description 