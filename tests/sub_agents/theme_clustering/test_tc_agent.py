import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json
import logging

# 테스트 대상 모듈 임포트 시 경로 문제 해결
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from theme_news_agent.sub_agents.theme_clustering.agent import ThemeClusteringAgent
from google.adk.agents.invocation_context import InvocationContext

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

# --- Fixtures (4.3용) ---

@pytest.fixture
def agent_for_process():
    """ThemeClusteringAgent 인스턴스를 생성하는 픽스처 (process 테스트용)"""
    return ThemeClusteringAgent()

@pytest.fixture
def mock_ctx():
    """InvocationContext 모킹 픽스처"""
    ctx = MagicMock(spec=InvocationContext)
    ctx.state = {} # 각 테스트에서 상태를 설정
    return ctx

@pytest.fixture
def sample_keyword_results():
    """테스트용 keyword_results 데이터"""
    return [
        {"keyword": "ai", "frequency": {"total": 50}},
        {"keyword": "머신러닝", "frequency": {"total": 30}},
    ]

# --- Test Cases (4.3 - Refactored) ---

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.theme_clustering.agent.get_clustering_prompt', return_value="Expected Prompt String")
async def test_process_returns_prompt_on_success(mock_get_prompt, agent_for_process, mock_ctx, sample_keyword_results, caplog):
    """4.3.1 (수정): 정상 처리 시 생성된 프롬프트를 반환하는지 확인"""
    mock_ctx.state["keyword_results"] = sample_keyword_results
    caplog.set_level(logging.INFO) # 로깅 레벨 명시적 설정

    # Act
    result = await agent_for_process.process(mock_ctx)

    # Assert
    mock_get_prompt.assert_called_once_with(sample_keyword_results)
    assert result == "Expected Prompt String"
    assert "클러스터링 프롬프트 생성 완료" in caplog.text
    # 상태 저장 로직 제거됨 확인 (필요시)
    # assert "clustered_themes" not in mock_ctx.state

@pytest.mark.asyncio
async def test_process_missing_keyword_results(agent_for_process, mock_ctx, caplog):
    """4.3.2: 상태 누락 시 오류 메시지를 반환하는지 확인"""
    # Arrange: keyword_results 설정 안함
    caplog.set_level(logging.WARNING) # WARNING 레벨 확인을 위해 설정 (기본값보다 낮으므로)

    # Act
    result = await agent_for_process.process(mock_ctx)

    # Assert
    assert "상태에서 'keyword_results'를 찾을 수 없거나 비어 있습니다." in caplog.text
    assert result == "키워드 추출 결과가 없어 테마 클러스터링을 진행할 수 없습니다."

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.theme_clustering.agent.get_clustering_prompt', side_effect=Exception("Prompt generation error"))
async def test_process_prompt_generation_failure(mock_get_prompt, agent_for_process, mock_ctx, sample_keyword_results, caplog):
    """4.3.x (신규): 프롬프트 생성 실패 시 오류 메시지를 반환하는지 확인"""
    # Arrange
    mock_ctx.state["keyword_results"] = sample_keyword_results
    caplog.set_level(logging.ERROR) # ERROR 레벨 확인을 위해 설정

    # Act
    result = await agent_for_process.process(mock_ctx)

    # Assert
    mock_get_prompt.assert_called_once_with(sample_keyword_results)
    assert "클러스터링 프롬프트 생성 중 오류 발생" in caplog.text
    assert "Prompt generation error" in result
    assert result.startswith("클러스터링 프롬프트 생성 중 오류 발생:")

# --- 제거된 테스트 케이스 --- 
# 4.3.3 ~ 4.3.8: LLM 응답 처리 관련 테스트는 현재 process 메서드의 책임이 아님
# - test_process_empty_llm_result
# - test_process_llm_call_failure
# - test_process_json_parsing_failure
# - test_process_json_structure_not_list
# - test_process_json_structure_item_format_error
# - test_process_json_with_markdown 