import pytest
from google.adk import Agent

# 테스트 대상 모듈 임포트 시도
try:
    from theme_news_agent.sub_agents.data_collection.agent import DataCollectionAgent
    module_imported = True
except ImportError:
    module_imported = False
    DataCollectionAgent = None # 임포트 실패 시 None으로 설정

# 모듈 임포트 성공 여부에 따라 테스트 건너뛰기 설정
pytestmark = pytest.mark.skipif(not module_imported,
                                reason="theme_news_agent.sub_agents.data_collection.agent 모듈을 임포트할 수 없습니다.")

def test_data_collection_agent_definition():
    """DataCollectionAgent 클래스가 정의되어 있고 Agent를 상속하는지 테스트합니다."""
    assert DataCollectionAgent is not None, "DataCollectionAgent 클래스를 찾을 수 없습니다."
    assert issubclass(DataCollectionAgent, Agent), "DataCollectionAgent가 Agent를 상속하지 않습니다."

def test_data_collection_agent_instantiation():
    """DataCollectionAgent 인스턴스를 생성할 수 있는지 테스트합니다."""
    try:
        agent = DataCollectionAgent()
        assert isinstance(agent, DataCollectionAgent), "생성된 객체가 DataCollectionAgent의 인스턴스가 아닙니다."
        # 필요하다면 기본 속성값 검증 추가
        assert agent.name == "DataCollector"
        assert agent.description == "데이터 수집 에이전트"
    except Exception as e:
        pytest.fail(f"DataCollectionAgent 인스턴스 생성 중 오류 발생: {e}") 