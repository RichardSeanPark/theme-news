"""Tests for the TrendAnalysisAgent class."""

import pytest
from theme_news_agent.sub_agents.trend_analysis.agent import TrendAnalysisAgent


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