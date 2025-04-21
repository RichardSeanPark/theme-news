import os
import toml

def test_pyproject_toml_exists():
    """Test case 2.1.1: Check if pyproject.toml exists in theme_news_agent/."""
    assert os.path.isfile("theme_news_agent/pyproject.toml"), "The file 'theme_news_agent/pyproject.toml' should exist."

def test_pyproject_toml_python_version():
    """Test case 2.1.1: Check if pyproject.toml has the correct Python version."""
    file_path = "theme_news_agent/pyproject.toml"
    assert os.path.isfile(file_path), f"File not found: {file_path}"
    
    try:
        data = toml.load(file_path)
        python_version = data.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python")
        assert python_version == "^3.13", f"Expected Python version ^3.13, but found {python_version}"
    except toml.TomlDecodeError:
        assert False, f"Failed to parse TOML file: {file_path}"
    except Exception as e:
        assert False, f"An error occurred: {e}" 