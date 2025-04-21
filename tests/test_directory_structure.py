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