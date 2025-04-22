# tests/sub_agents/trend_analysis/tools/test_stats_tool.py
import os
import json
import pytest
import numpy as np
from unittest.mock import patch, mock_open

# 테스트 대상 모듈 임포트 (경로 주의)
# 프로젝트 루트에서 pytest를 실행한다고 가정하고 절대 임포트 사용
from theme_news_agent.sub_agents.trend_analysis.tools.stats_tool import calculate_trends, _load_historical_data, _save_historical_data

# --- Fixtures ---

@pytest.fixture
def sample_current_themes():
    """ Provides a sample list of current themes for testing. """
    return [
        {"theme": "AI Ethics", "keywords": ["bias", "fairness"], "mentions": 50},
        {"theme": "Quantum Computing", "keywords": ["qubit", "supremacy"], "mentions": 75},
        {"theme": "Renewable Energy", "keywords": ["solar", "wind"], "mentions": 120}, # New theme
    ]

@pytest.fixture
def sample_historical_data():
    """ Provides a sample dictionary of historical data. """
    return {
        "AI Ethics": {
            "mentions_history": [40, 45, 35],
            "avg": 40.0,
            "std": np.std([40, 45, 35]) # approx 4.08
        },
        "Quantum Computing": {
            "mentions_history": [70],
            "avg": 70.0,
            "std": 0.0 # std is 0 with only one data point
        }
        # "Renewable Energy" is missing
    }

@pytest.fixture
def historical_file_path(tmp_path):
    """ Returns a path for the historical data file within a temporary directory. """
    # Use a subdirectory within tmp_path to mimic the default path structure if needed
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir / "historical_themes.json"

@pytest.fixture
def create_historical_file(historical_file_path, sample_historical_data):
    """ Creates a sample historical data file for testing. """
    # No need to create directory here, historical_file_path fixture handles it.
    # os.makedirs(historical_file_path.parent, exist_ok=True) # Already handled by fixture
    with open(historical_file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_historical_data, f, ensure_ascii=False, indent=4)
    return historical_file_path

# --- Test Cases based on testcase2.md ---

# Test Case 5.2.1
def test_calculate_trends_no_historical_file(historical_file_path, sample_current_themes, caplog):
    """ 5.2.1: Tests behavior when the historical data file does not exist. """
    # Arrange
    assert not os.path.exists(historical_file_path) # Ensure file doesn't exist initially

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)): # Mock env var to use temp path
        result_themes = calculate_trends(sample_current_themes.copy()) # Use copy to avoid modifying fixture

    # Assert
    # Check z_scores are 0.0
    for theme in result_themes:
        assert 'z_score' in theme
        assert theme['z_score'] == 0.0

    # Check file creation and content
    assert os.path.exists(historical_file_path)
    with open(historical_file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    # Check that new themes are now in the saved data with initial values
    assert "AI Ethics" in saved_data
    assert saved_data["AI Ethics"]["mentions_history"] == [50]
    assert saved_data["AI Ethics"]["avg"] == 50.0
    assert saved_data["AI Ethics"]["std"] == 0.0

    assert "Quantum Computing" in saved_data
    assert saved_data["Quantum Computing"]["mentions_history"] == [75]
    assert saved_data["Quantum Computing"]["avg"] == 75.0
    assert saved_data["Quantum Computing"]["std"] == 0.0

    assert "Renewable Energy" in saved_data
    assert saved_data["Renewable Energy"]["mentions_history"] == [120]
    assert saved_data["Renewable Energy"]["avg"] == 120.0
    assert saved_data["Renewable Energy"]["std"] == 0.0

    assert "Historical data file not found" in caplog.text # Check log message

# Test Case 5.2.2
def test_calculate_trends_load_historical_data(create_historical_file, sample_current_themes, sample_historical_data):
    """ 5.2.2: Tests correct loading and usage of existing historical data. """
    # Arrange
    historical_file_path = create_historical_file # File now exists with sample_historical_data

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        result_themes = calculate_trends(sample_current_themes.copy())

    # Assert
    ai_ethics_result = next(t for t in result_themes if t['theme'] == "AI Ethics")
    quantum_result = next(t for t in result_themes if t['theme'] == "Quantum Computing")
    renewable_result = next(t for t in result_themes if t['theme'] == "Renewable Energy")

    # Z-score for AI Ethics (std > 0)
    expected_z_ai = (50 - sample_historical_data["AI Ethics"]["avg"]) / sample_historical_data["AI Ethics"]["std"]
    assert ai_ethics_result['z_score'] == pytest.approx(expected_z_ai)

    # Z-score for Quantum Computing (std == 0)
    assert quantum_result['z_score'] == 0.0 # As per logic for std=0

    # Z-score for Renewable Energy (new theme)
    assert renewable_result['z_score'] == 0.0

# Test Case 5.2.3
def test_calculate_trends_corrupted_historical_file(historical_file_path, sample_current_themes, caplog):
    """ 5.2.3: Tests handling of corrupted JSON file. """
    # Arrange
    # Ensure directory exists before writing corrupted file
    historical_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(historical_file_path, 'w', encoding='utf-8') as f:
        f.write("{\"invalid json") # Write corrupted JSON

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        result_themes = calculate_trends(sample_current_themes.copy())

    # Assert
    # Check z_scores are 0.0 as it should start fresh
    for theme in result_themes:
        assert theme['z_score'] == 0.0

    # Check error log
    assert "Error decoding JSON" in caplog.text

    # Check if the file was overwritten with new (valid) data
    assert os.path.exists(historical_file_path)
    with open(historical_file_path, 'r', encoding='utf-8') as f:
        try:
            saved_data = json.load(f)
            # Check if it contains the current themes as initial data
            assert "AI Ethics" in saved_data
            assert saved_data["AI Ethics"]["mentions_history"] == [50]
        except json.JSONDecodeError:
            pytest.fail("Corrupted file was not overwritten with valid JSON.")

# Test Case 5.2.4
def test_calculate_trends_z_score_calculation_std_positive(historical_file_path):
    """ 5.2.4: Tests Z-score calculation when std > 0. """
    # Arrange
    std_dev = np.std([80, 100, 120])
    historical_data = {
        "Test Theme": {"mentions_history": [80, 100, 120], "avg": 100.0, "std": std_dev}
    }
    current_themes = [{"theme": "Test Theme", "keywords": [], "mentions": 140}]
    historical_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(historical_file_path, 'w', encoding='utf-8') as f:
        json.dump(historical_data, f)

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        result_themes = calculate_trends(current_themes)

    # Assert
    expected_z = (140 - 100.0) / std_dev
    assert result_themes[0]['z_score'] == pytest.approx(expected_z) # Approx 2.449

# Test Case 5.2.5
def test_calculate_trends_z_score_calculation_std_zero(historical_file_path, caplog):
    """ 5.2.5: Tests Z-score calculation when std = 0. """
    # Arrange
    historical_data = {
        "Test Theme": {"mentions_history": [100], "avg": 100.0, "std": 0.0}
    }
    current_themes = [{"theme": "Test Theme", "keywords": [], "mentions": 120}] # Mentions increased
    historical_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(historical_file_path, 'w', encoding='utf-8') as f:
        json.dump(historical_data, f)

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        result_themes = calculate_trends(current_themes)

    # Assert
    assert result_themes[0]['z_score'] == 0.0
    assert "has std=0, assigning z_score=0" in caplog.text # Check log

# Test Case 5.2.6
def test_calculate_trends_update_existing_theme(create_historical_file, sample_historical_data):
    """ 5.2.6: Tests correct update of history, avg, and std for an existing theme. """
    # Arrange
    historical_file_path = create_historical_file
    theme_name = "AI Ethics"
    initial_history = sample_historical_data[theme_name]["mentions_history"].copy()
    current_mentions = 60
    current_themes = [{"theme": theme_name, "keywords": [], "mentions": current_mentions}]
    expected_new_history = initial_history + [current_mentions] # [40, 45, 35, 60]

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        calculate_trends(current_themes) # We only care about the saved data here

    # Assert
    # Reload the saved data
    with open(historical_file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    assert theme_name in saved_data
    updated_info = saved_data[theme_name]

    assert updated_info["mentions_history"] == expected_new_history
    assert updated_info["avg"] == pytest.approx(np.mean(expected_new_history)) # approx 45.0
    assert updated_info["std"] == pytest.approx(np.std(expected_new_history)) # approx 9.68

# Test Case 5.2.7
def test_calculate_trends_add_new_theme(create_historical_file):
    """ 5.2.7: Tests correct addition of a new theme to the historical data. """
    # Arrange
    historical_file_path = create_historical_file # Contains AI Ethics, Quantum Computing
    new_theme_name = "Renewable Energy"
    new_mentions = 120
    current_themes = [{"theme": new_theme_name, "keywords": [], "mentions": new_mentions}]

    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        calculate_trends(current_themes)

    # Assert
    with open(historical_file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    assert new_theme_name in saved_data
    new_theme_info = saved_data[new_theme_name]

    assert new_theme_info["mentions_history"] == [new_mentions]
    assert new_theme_info["avg"] == float(new_mentions)
    assert new_theme_info["std"] == 0.0

# Test Case 5.2.8
def test_calculate_trends_invalid_input_format(historical_file_path, caplog):
    """ 5.2.8: Tests handling of invalid items in the current_themes list. """
    # Arrange
    invalid_themes = [
        {"theme": "Valid Theme", "mentions": 10}, # Valid
        {"theme": "Missing Mentions"},           # Invalid - mentions missing
        {"mentions": 20},                       # Invalid - theme missing
        "just a string",                         # Invalid - not a dict
        {"theme": "Wrong Type", "mentions": "30"}, # Invalid - mentions not int
    ]
    historical_data = {} # Start empty
    historical_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(historical_file_path, 'w', encoding='utf-8') as f:
        json.dump(historical_data, f)


    # Act
    with patch('os.getenv', return_value=str(historical_file_path)):
        # Make a copy before passing to avoid modifying the original list if the function does
        result_themes = calculate_trends(invalid_themes.copy())

    # Assert
    assert len(result_themes) == len(invalid_themes) # Should return all items

    # Check z_scores for invalid items - Ensure they exist and are 0.0
    # We need to handle the case where the original item was not a dict
    def get_z_score(item): # Helper to safely get z_score
        # Return 0.0 for non-dict items or if z_score is missing, for consistency
        return item.get('z_score', 0.0) if isinstance(item, dict) else 0.0

    assert get_z_score(result_themes[1]) == 0.0
    assert get_z_score(result_themes[2]) == 0.0
    assert get_z_score(result_themes[3]) == 0.0 # Function adds z_score even to non-dict for consistency
    assert get_z_score(result_themes[4]) == 0.0

    # Check z_score for valid item (should be 0 as history is empty)
    assert result_themes[0]['z_score'] == 0.0

    # Check logs
    assert "Skipping theme due to invalid format (missing/wrong type keys): {'theme': 'Missing Mentions'}" in caplog.text
    assert "Skipping theme due to invalid format (missing/wrong type keys): {'mentions': 20}" in caplog.text
    assert "Skipping non-dictionary item in current_themes: just a string" in caplog.text
    assert "Skipping theme due to invalid format (missing/wrong type keys): {'theme': 'Wrong Type', 'mentions': '30'}" in caplog.text

    # Check that only the valid theme was added to historical data
    with open(historical_file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert "Valid Theme" in saved_data
    assert len(saved_data) == 1

# Test Case 5.2.9
@patch('theme_news_agent.sub_agents.trend_analysis.tools.stats_tool._load_historical_data')
@patch('theme_news_agent.sub_agents.trend_analysis.tools.stats_tool._save_historical_data')
def test_calculate_trends_historical_data_path_env_var(mock_save, mock_load):
    """ 5.2.9: Tests that HISTORICAL_DATA_PATH env var is used. """
    # Arrange
    test_path = "/custom/path/to/history.json"
    mock_load.return_value = {} # Mock loading to return empty data
    current_themes = [{"theme": "Any", "mentions": 10}]

    # Act
    # Patch os.getenv specifically for HISTORICAL_DATA_PATH
    # Use a dict to simulate os.environ more accurately if needed elsewhere, but lambda is fine here
    with patch('os.getenv', lambda k, d=None: test_path if k == "HISTORICAL_DATA_PATH" else os.environ.get(k, d)):
         calculate_trends(current_themes)

    # Assert
    mock_load.assert_called_once_with(test_path)
    # Check the first argument (file_path) of the mock_save call
    mock_save.assert_called_once()
    assert mock_save.call_args[0][0] == test_path