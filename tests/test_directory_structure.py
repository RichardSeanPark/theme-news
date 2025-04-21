import os

def test_theme_news_agent_directory_exists():
    """Test case 1.1.1: Check if the theme_news_agent directory exists."""
    assert os.path.isdir("theme_news_agent"), "The directory 'theme_news_agent/' should exist."

def test_package_directory_exists():
    """Test case 1.1.2: Check if the package directory theme_news_agent/theme_news_agent exists."""
    assert os.path.isdir("theme_news_agent/theme_news_agent"), "The directory 'theme_news_agent/theme_news_agent/' should exist."

def test_init_file_exists():
    """Test case 1.1.3: Check if the __init__.py file exists in the package directory."""
    assert os.path.isfile("theme_news_agent/theme_news_agent/__init__.py"), "The file 'theme_news_agent/theme_news_agent/__init__.py' should exist."

def test_agent_file_exists():
    """Test case 1.1.4: Check if the agent.py file exists in the package directory."""
    assert os.path.isfile("theme_news_agent/theme_news_agent/agent.py"), "The file 'theme_news_agent/theme_news_agent/agent.py' should exist."

def test_sub_agents_directory_exists():
    """Test case 1.1.5: Check if the sub_agents directory exists in the package directory."""
    assert os.path.isdir("theme_news_agent/theme_news_agent/sub_agents"), "The directory 'theme_news_agent/theme_news_agent/sub_agents/' should exist."

def test_specific_sub_agent_directories_exist():
    """Test case 1.1.6: Check if specific sub-agent directories exist."""
    base_path = "theme_news_agent/theme_news_agent/sub_agents"
    sub_agent_dirs = [
        "data_collection",
        "keyword_extraction",
        "theme_clustering",
        "trend_analysis",
        "summary_generation"
    ]
    for dir_name in sub_agent_dirs:
        path = os.path.join(base_path, dir_name)
        assert os.path.isdir(path), f"The directory '{path}' should exist." 