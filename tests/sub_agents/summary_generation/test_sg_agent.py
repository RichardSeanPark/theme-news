import pytest
from theme_news_agent.sub_agents.summary_generation.agent import SummaryGenerationAgent

def test_summary_generation_agent_creation():
    """
    Test Case 6.1.1: SummaryGenerationAgent 객체 생성 확인
    Checks if an instance of SummaryGenerationAgent can be created successfully.
    """
    try:
        agent = SummaryGenerationAgent()
        assert isinstance(agent, SummaryGenerationAgent), \
            "Agent creation failed or returned wrong type."
    except Exception as e:
        pytest.fail(f"SummaryGenerationAgent creation failed with exception: {e}")

def test_summary_generation_agent_init_attributes():
    """
    Test Case 6.1.2: __init__ 속성 확인
    Checks if the instance attributes (name, description, model, instruction)
    are set correctly during initialization, using default values.
    """
    agent = SummaryGenerationAgent()

    # Check default values
    assert agent.name == "summary_generator", \
        f"Expected name 'summary_generator', but got '{agent.name}'"
    assert agent.description == "Generates a news report summary based on trend analysis results.", \
        f"Expected description did not match, got '{agent.description}'"
    assert agent.model == "gemini-1.5-flash-latest", \
        f"Expected default model 'gemini-1.5-flash-latest', but got '{agent.model}'"
    assert agent.instruction == "", \
        f"Expected default instruction '', but got '{agent.instruction}'"

    # Check if attributes can be overridden
    custom_model = "test-model"
    custom_name = "custom_summary"
    custom_desc = "Custom description"
    custom_instruction = "Custom instruction"
    agent_custom = SummaryGenerationAgent(
        model=custom_model,
        name=custom_name,
        description=custom_desc,
        instruction=custom_instruction
    )
    assert agent_custom.name == custom_name, \
        f"Expected custom name '{custom_name}', but got '{agent_custom.name}'"
    assert agent_custom.description == custom_desc, \
        f"Expected custom description '{custom_desc}', but got '{agent_custom.description}'"
    assert agent_custom.model == custom_model, \
        f"Expected custom model '{custom_model}', but got '{agent_custom.model}'"
    assert agent_custom.instruction == custom_instruction, \
        f"Expected custom instruction '{custom_instruction}', but got '{agent_custom.instruction}'" 