import pytest
from theme_news_agent.sub_agents.summary_generation.prompt import (
    get_summary_prompt,
    SUMMARY_PROMPT_TEMPLATE
)


# Test Case 6.2.1
def test_get_summary_prompt_normal_input():
    """Tests get_summary_prompt with a valid list of trend results."""
    test_data = [
        {'rank': 1, 'theme': 'AI 비서', 'z_score': 3.5},
        {'rank': 2, 'theme': '전기차 보조금', 'z_score': 2.10}
    ]
    expected_trend_str = (
        "- 순위 1: AI 비서 (Z-점수: 3.50)\n"
        "- 순위 2: 전기차 보조금 (Z-점수: 2.10)"
    )

    prompt = get_summary_prompt(test_data)

    assert isinstance(prompt, str)
    # Check if the basic structure is present
    assert "당신은 최신 트렌드 분석 결과를 바탕으로" in prompt
    assert "[상위 트렌드 테마 목록]" in prompt
    assert "[요청 사항]" in prompt
    assert "[뉴스 요약 보고서]" in prompt
    # Check if the formatted data is correctly included
    assert expected_trend_str in prompt
    # Check if the placeholder is replaced
    assert "{trend_data_str}" not in prompt


# Test Case 6.2.2
def test_get_summary_prompt_empty_input():
    """Tests get_summary_prompt with an empty list."""
    test_data = []
    expected_message = "분석된 트렌드 테마가 없습니다."

    prompt = get_summary_prompt(test_data)

    assert isinstance(prompt, str)
    assert expected_message in prompt
    # Ensure the rest of the prompt structure is still there
    assert "[상위 트렌드 테마 목록]" in prompt
    assert "[뉴스 요약 보고서]" in prompt
    assert "{trend_data_str}" not in prompt


# Test Case 6.2.3
def test_get_summary_prompt_malformed_keys():
    """Tests get_summary_prompt with missing keys in input dictionaries."""
    test_data = [
        {'rank': 1, 'z_score': 2.0}, # Missing 'theme'
        {'theme': '테마 B', 'z_score': 1.5}, # Missing 'rank'
        {'rank': 3, 'theme': '테마 C'} # Missing 'z_score'
    ]
    expected_results = [
        "- 순위 1: 알 수 없는 테마 (Z-점수: 2.00)",
        "- 순위 N/A: 테마 B (Z-점수: 1.50)",
        "- 순위 3: 테마 C (Z-점수: N/A)"
    ]

    prompt = get_summary_prompt(test_data)

    assert isinstance(prompt, str)
    for expected_line in expected_results:
        assert expected_line in prompt
    assert "{trend_data_str}" not in prompt


# Test Case 6.2.4
def test_get_summary_prompt_z_score_formatting():
    """Tests the formatting of z_score values (float, int, None, missing)."""
    test_data = [
        {'rank': 1, 'theme': 'Float Score', 'z_score': 3.14159},
        {'rank': 2, 'theme': 'Int Score', 'z_score': 5},
        {'rank': 3, 'theme': 'None Score', 'z_score': None},
        {'rank': 4, 'theme': 'Missing Score'},
        {'rank': 5, 'theme': 'String Score', 'z_score': 'invalid'}
    ]
    expected_z_formats = [
        "(Z-점수: 3.14)",
        "(Z-점수: 5.00)",
        "(Z-점수: N/A)",
        "(Z-점수: N/A)",
        "(Z-점수: N/A)"
    ]

    prompt = get_summary_prompt(test_data)

    assert isinstance(prompt, str)
    # Check each expected format appears in the prompt
    # This is a bit loose as order isn't strictly checked here, but good enough
    for z_format in expected_z_formats:
        assert z_format in prompt
    assert "{trend_data_str}" not in prompt


# Optional: Test for template formatting issues (if template might change)
# This requires modifying the template temporarily or mocking it
# def test_get_summary_prompt_template_error(mocker):
#     """Tests behavior when the template string is broken."""
#     mocker.patch(
#         'theme_news_agent.sub_agents.summary_generation.prompt.SUMMARY_PROMPT_TEMPLATE',
#         "잘못된 템플릿 {missing_key}"
#     )
#     test_data = [{'rank': 1, 'theme': 'A', 'z_score': 1.0}]
#     prompt = get_summary_prompt(test_data)
#     assert "Error: Could not generate the summary prompt" in prompt 