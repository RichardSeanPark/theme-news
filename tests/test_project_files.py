import os

def test_agent_readme_exists():
    """Test case 4.1.1: Check if theme_news_agent/README.md exists."""
    assert os.path.isfile("theme_news_agent/README.md"), "The file 'theme_news_agent/README.md' should exist." 