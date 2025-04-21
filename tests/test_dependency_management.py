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

def test_core_dependencies_exist():
    """Test case 2.1.2: Check if core dependencies are listed in pyproject.toml."""
    file_path = "theme_news_agent/pyproject.toml"
    assert os.path.isfile(file_path), f"File not found: {file_path}"
    
    core_deps = [
        "google-adk",
        "requests",
        "beautifulsoup4",
        "playwright",
        "newspaper3k",
        "numpy",
        "pandas",
        "pydantic",
        "python-dotenv"
    ]
    
    try:
        data = toml.load(file_path)
        dependencies = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        missing_deps = [dep for dep in core_deps if dep not in dependencies]
        assert not missing_deps, f"Core dependencies missing in pyproject.toml: {', '.join(missing_deps)}"
    except toml.TomlDecodeError:
        assert False, f"Failed to parse TOML file: {file_path}"
    except Exception as e:
        assert False, f"An error occurred: {e}"

def test_pytest_dev_dependency_exists():
    """Test case 2.1.3: Check if pytest is listed as a dev dependency."""
    file_path = "theme_news_agent/pyproject.toml"
    assert os.path.isfile(file_path), f"File not found: {file_path}"
    
    try:
        data = toml.load(file_path)
        dev_dependencies = data.get("tool", {}).get("poetry", {}).get("group", {}).get("dev", {}).get("dependencies", {})
        assert "pytest" in dev_dependencies, "pytest not found in [tool.poetry.group.dev.dependencies]"
    except toml.TomlDecodeError:
        assert False, f"Failed to parse TOML file: {file_path}"
    except Exception as e:
        assert False, f"An error occurred: {e}"

def test_poetry_lock_exists():
    """Test case 2.1.4: Check if poetry.lock exists in theme_news_agent/."""
    assert os.path.isfile("theme_news_agent/poetry.lock"), "The file 'theme_news_agent/poetry.lock' should exist."

def test_env_example_exists():
    """Test case 3.1.1: Check if .env.example exists in theme_news_agent/."""
    assert os.path.isfile("theme_news_agent/.env.example"), "The file 'theme_news_agent/.env.example' should exist." 