"""Tests for the TrendAnalysisAgent class."""

import pytest
from theme_news_agent.sub_agents.trend_analysis.agent import TrendAnalysisAgent
from unittest.mock import AsyncMock, MagicMock, patch  # Import necessary mock objects
# from google.adk.runtime.context import InvocationContext # 이전 경로 주석 처리
from google.adk.agents.invocation_context import InvocationContext # 새로운 경로로 수정


def test_trend_analysis_agent_creation():
    """Test case 5.1.1: Verify TrendAnalysisAgent can be instantiated."""
    try:
        agent = TrendAnalysisAgent()
        assert isinstance(agent, TrendAnalysisAgent), "Agent is not an instance of TrendAnalysisAgent"
    except Exception as e:
        pytest.fail(f"Failed to instantiate TrendAnalysisAgent: {e}")

def test_trend_analysis_agent_init_attributes():
    """Test case 5.1.2: Verify the description attribute is set correctly."""
    agent = TrendAnalysisAgent()
    expected_description = "Analyzes theme trends based on historical data and Z-scores."
    assert agent.description == expected_description, \
        f"Agent description '{agent.description}' does not match expected '{expected_description}'"

    # Initially, tools should be empty or None as it's commented out in __init__
    # Depending on google.adk.Agent's default behavior, it might be None or an empty list.
    # We'll assert it's not None and is empty if it's a list.
    assert agent.tools is not None, "Agent tools attribute should not be None"
    if isinstance(agent.tools, list):
        assert not agent.tools, "Agent tools list should be empty initially"

# --- Tests for TrendAnalysisAgent.process (TODO 5.3) ---

@pytest.fixture
def mock_context():
    """Provides a mock InvocationContext with a state dictionary."""
    ctx = MagicMock(spec=InvocationContext)
    ctx.state = {}
    return ctx

@pytest.fixture
def trend_agent():
    """Provides an instance of TrendAnalysisAgent."""
    return TrendAnalysisAgent()

@pytest.mark.asyncio
async def test_trend_agent_process_missing_state(trend_agent, mock_context):
    """Test case 5.3.1: Error when 'clustered_themes' is missing."""
    # Arrange: clustered_themes is not in state (default fixture)
    # Act
    result = await trend_agent.process(mock_context)
    # Assert
    assert "Error: 'clustered_themes' not found or invalid in state." in result

@pytest.mark.asyncio
async def test_trend_agent_process_invalid_state_type(trend_agent, mock_context):
    """Test case 5.3.2: Error when 'clustered_themes' is not a list."""
    # Arrange
    mock_context.state["clustered_themes"] = "not a list"
    # Act
    result = await trend_agent.process(mock_context)
    # Assert
    assert "Error: 'clustered_themes' not found or invalid in state." in result

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_calls_stats_tool(mock_calculate_trends_tool, trend_agent, mock_context):
    """Test case 5.3.3: Verify calculate_trends (stats_tool.func) is called."""
    # Arrange
    clustered_data = [{"theme": "A", "mentions": 10}]
    mock_context.state["clustered_themes"] = clustered_data
    # Mock the .func attribute of the mocked tool instance
    mock_calculate_trends_tool.func = MagicMock(return_value=[{"theme": "A", "mentions": 10, "z_score": 1.0}])
    # Ensure the agent uses the (now potentially mocked) class attribute
    trend_agent.stats_tool = mock_calculate_trends_tool

    # Act
    await trend_agent.process(mock_context)

    # Assert
    # Assert that the .func attribute of the mocked tool was called
    mock_calculate_trends_tool.func.assert_called_once_with(clustered_data)

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_stats_tool_exception(mock_calculate_trends_tool, trend_agent, mock_context):
    """Test case 5.3.4: Handle exception during calculate_trends call."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": "A", "mentions": 10}]
    # Mock the .func attribute to raise an exception
    mock_calculate_trends_tool.func = MagicMock(side_effect=Exception("Tool Error"))
    trend_agent.stats_tool = mock_calculate_trends_tool

    # Act
    result = await trend_agent.process(mock_context)

    # Assert
    assert "Error during trend analysis: Tool Error" in result
    mock_calculate_trends_tool.func.assert_called_once() # Verify func was called

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_sorts_by_zscore(mock_calculate_trends_tool, trend_agent, mock_context):
    """Test case 5.3.5: Verify results are sorted by z_score descending."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": "A"}, {"theme": "B"}, {"theme": "C"}] # Dummy input
    # Simulate calculate_trends returning unsorted z-scores
    mock_return = [
        {"theme": "A", "mentions": 10, "z_score": 1.5},
        {"theme": "B", "mentions": 30, "z_score": 3.0},
        {"theme": "C", "mentions": 5, "z_score": 0.5},
    ]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool

    # Act
    await trend_agent.process(mock_context)

    # Assert
    saved_results = mock_context.state.get("trend_results")
    assert saved_results is not None
    assert len(saved_results) == 3
    assert saved_results[0]["theme"] == "B" # Highest z_score
    assert saved_results[1]["theme"] == "A"
    assert saved_results[2]["theme"] == "C" # Lowest z_score

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.os.getenv")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_selects_top_n(mock_calculate_trends_tool, mock_getenv, trend_agent, mock_context):
    """Test case 5.3.6: Select top N themes based on TREND_TOP_N env var."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": f"{i}"} for i in range(5)] # Dummy input
    # Simulate calculate_trends returning 5 themes sorted by z_score
    mock_return = [
        {"theme": "B", "z_score": 5.0}, {"theme": "A", "z_score": 4.0},
        {"theme": "D", "z_score": 3.0}, {"theme": "C", "z_score": 2.0},
        {"theme": "E", "z_score": 1.0},
    ]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool
    mock_getenv.return_value = "3" # Set TREND_TOP_N to 3

    # Act
    await trend_agent.process(mock_context)

    # Assert
    saved_results = mock_context.state.get("trend_results")
    assert saved_results is not None
    assert len(saved_results) == 3
    assert [t["theme"] for t in saved_results] == ["B", "A", "D"]
    mock_getenv.assert_called_with("TREND_TOP_N") # Verify env var was checked without default

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.os.getenv")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_selects_top_n_default(mock_calculate_trends_tool, mock_getenv, trend_agent, mock_context):
    """Test case 5.3.7: Select top N themes using default when env var is not set."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": f"{i}"} for i in range(25)] # Dummy input
    # Simulate calculate_trends returning 25 themes sorted by z_score
    mock_return = [{"theme": f"{i}", "z_score": 25.0 - i} for i in range(25)]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool
    mock_getenv.return_value = None # Simulate env var not set

    # Act
    await trend_agent.process(mock_context)

    # Assert
    saved_results = mock_context.state.get("trend_results")
    assert saved_results is not None
    assert len(saved_results) == 20 # Default top N is 20
    assert [t["theme"] for t in saved_results] == [f"{i}" for i in range(20)]
    mock_getenv.assert_called_with("TREND_TOP_N") # Verify env var was checked without default

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.os.getenv")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.logger") # Patch logger to check warnings
async def test_trend_agent_process_selects_top_n_invalid(mock_logger, mock_calculate_trends_tool, mock_getenv, trend_agent, mock_context):
    """Test case 5.3.8: Select top N using default when env var is invalid."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": f"{i}"} for i in range(25)] # Dummy input
    mock_return = [{"theme": f"{i}", "z_score": 25.0 - i} for i in range(25)]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool

    # Test with non-numeric value
    mock_getenv.return_value = "abc"
    await trend_agent.process(mock_context)
    saved_results_abc = mock_context.state.get("trend_results")
    assert len(saved_results_abc) == 20 # Default
    mock_logger.warning.assert_called_with("Invalid TREND_TOP_N value: 'abc'. Using default 20.") # Updated message

    # Reset mock logger calls for next check
    mock_logger.reset_mock()
    # Reset state for the next part of the test
    mock_context.state = {"clustered_themes": [{"theme": f"{i}"} for i in range(25)]}

    # Test with negative value
    mock_getenv.return_value = "-5"
    # Need to ensure the agent instance uses the mocked tool for this call too
    trend_agent.stats_tool = mock_calculate_trends_tool
    await trend_agent.process(mock_context)
    saved_results_neg = mock_context.state.get("trend_results")
    assert len(saved_results_neg) == 20 # Default
    mock_logger.warning.assert_called_with("TREND_TOP_N (-5) is not positive. Using default 20.") # Updated message


@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.os.getenv")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_adds_rank(mock_calculate_trends_tool, mock_getenv, trend_agent, mock_context):
    """Test case 5.3.9: Verify 'rank' is added correctly to top themes."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": f"{i}"} for i in range(3)] # Dummy input
    mock_return = [
        {"theme": "B", "z_score": 3.0}, {"theme": "A", "z_score": 2.0}, {"theme": "C", "z_score": 1.0}
    ]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool
    mock_getenv.return_value = "3" # Or let it default if more than 3 returned

    # Act
    await trend_agent.process(mock_context)

    # Assert
    saved_results = mock_context.state.get("trend_results")
    assert saved_results is not None
    assert len(saved_results) == 3
    assert saved_results[0]["rank"] == 1 and saved_results[0]["theme"] == "B"
    assert saved_results[1]["rank"] == 2 and saved_results[1]["theme"] == "A"
    assert saved_results[2]["rank"] == 3 and saved_results[2]["theme"] == "C"

@pytest.mark.asyncio
@patch("theme_news_agent.sub_agents.trend_analysis.agent.os.getenv")
@patch("theme_news_agent.sub_agents.trend_analysis.agent.calculate_trends_tool")
async def test_trend_agent_process_saves_state_and_returns_success(mock_calculate_trends_tool, mock_getenv, trend_agent, mock_context):
    """Test case 5.3.10: Verify final state saving and success message."""
    # Arrange
    mock_context.state["clustered_themes"] = [{"theme": f"{i}"} for i in range(5)] # Dummy input
    mock_return = [{"theme": f"{i}", "z_score": 5.0 - i} for i in range(5)]
    mock_calculate_trends_tool.func = MagicMock(return_value=mock_return)
    trend_agent.stats_tool = mock_calculate_trends_tool
    mock_getenv.return_value = "5" # Select top 5

    # Act
    result_message = await trend_agent.process(mock_context)

    # Assert
    # Check state was saved
    saved_results = mock_context.state.get("trend_results")
    assert saved_results is not None
    assert len(saved_results) == 5
    # Verify the structure and rank of the first element as a sample check
    assert saved_results[0] == {"theme": "0", "z_score": 5.0, "rank": 1}
    # Check success message
    assert "Trend analysis complete. Top 5 trends identified and saved." in result_message 