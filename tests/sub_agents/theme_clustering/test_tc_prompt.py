# tests/sub_agents/theme_clustering/test_prompt.py
import pytest
from theme_news_agent.sub_agents.theme_clustering.prompt import (
    CLUSTERING_PROMPT_TEMPLATE,
    get_clustering_prompt
)

def test_clustering_prompt_template_content():
    """
    테스트 케이스 4.2.1: CLUSTERING_PROMPT_TEMPLATE 상수 확인
    """
    assert isinstance(CLUSTERING_PROMPT_TEMPLATE, str)
    assert "JSON 형식의 배열" in CLUSTERING_PROMPT_TEMPLATE
    assert '"theme":' in CLUSTERING_PROMPT_TEMPLATE
    assert '"keywords":' in CLUSTERING_PROMPT_TEMPLATE
    assert '"mentions":' in CLUSTERING_PROMPT_TEMPLATE
    assert "{keyword_data_str}" in CLUSTERING_PROMPT_TEMPLATE

def test_get_clustering_prompt_normal_input():
    """
    테스트 케이스 4.2.2: get_clustering_prompt 함수 - 정상 입력 테스트
    """
    test_keywords = [
        {"keyword": "AI", "frequency": {"total": 50}},
        {"keyword": "ML", "frequency": {"total": 30}},
        {"keyword": "딥러닝", "frequency": {"total": 25}}
    ]
    expected_data_str = "- AI (50회 언급)\n- ML (30회 언급)\n- 딥러닝 (25회 언급)"

    prompt = get_clustering_prompt(test_keywords)

    assert isinstance(prompt, str)
    assert expected_data_str in prompt
    # Check if base template structure is preserved (e.g., initial instruction)
    assert "당신은 대량의 키워드 데이터를 분석하여" in prompt
    assert "JSON 형식의 배열로만 반환해야 합니다" in prompt

def test_get_clustering_prompt_empty_input():
    """
    테스트 케이스 4.2.3: get_clustering_prompt 함수 - 빈 입력 테스트
    """
    test_keywords = []
    expected_data_str = "분석할 키워드가 없습니다."

    prompt = get_clustering_prompt(test_keywords)

    assert isinstance(prompt, str)
    assert expected_data_str in prompt
    # Check if base template structure is preserved
    assert "당신은 대량의 키워드 데이터를 분석하여" in prompt
    assert "JSON 형식의 배열로만 반환해야 합니다" in prompt
    assert "{keyword_data_str}" not in prompt # Placeholder should be replaced

def test_get_clustering_prompt_malformed_input():
    """
    테스트 케이스 4.2.4: get_clustering_prompt 함수 - 비정상 키 입력 테스트
    """
    test_keywords = [
        {"keyword": "AI"}, # frequency or total missing
        {"frequency": {"total": 30}}, # keyword missing
        {}, # both missing
        {"keyword": "Valid", "frequency": {}} # total missing
    ]
    # Expected output using defaults "N/A" and 0
    expected_lines = [
        "- AI (0회 언급)",
        "- N/A (30회 언급)",
        "- N/A (0회 언급)",
        "- Valid (0회 언급)"
    ]
    expected_data_str = "\n".join(expected_lines)

    try:
        prompt = get_clustering_prompt(test_keywords)
        assert isinstance(prompt, str)
        assert expected_data_str in prompt
        # Check if base template structure is preserved
        assert "당신은 대량의 키워드 데이터를 분석하여" in prompt
    except Exception as e:
        pytest.fail(f"get_clustering_prompt 함수가 비정상 입력 처리 중 예외 발생: {e}") 