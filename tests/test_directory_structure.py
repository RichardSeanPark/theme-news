import os

def test_theme_news_agent_directory_exists():
    """Test case 1.1.1: Check if the theme_news_agent directory exists."""
    assert os.path.isdir("theme_news_agent"), "The directory 'theme_news_agent/' should exist."

def test_package_directory_exists():
    """Test case 1.1.2: Check if core package files/dirs exist directly in theme_news_agent."""
    assert os.path.isfile("theme_news_agent/__init__.py"), "The file 'theme_news_agent/__init__.py' should exist."
    assert os.path.isfile("theme_news_agent/agent.py"), "The file 'theme_news_agent/agent.py' should exist."
    assert os.path.isdir("theme_news_agent/sub_agents"), "The directory 'theme_news_agent/sub_agents/' should exist."

def test_init_file_exists():
    """Test case 1.1.3: Check if the __init__.py file exists in the package directory (now root)."""
    assert os.path.isfile("theme_news_agent/__init__.py"), "The file 'theme_news_agent/__init__.py' should exist."

def test_agent_file_exists():
    """Test case 1.1.4: Check if the agent.py file exists in the package directory (now root)."""
    assert os.path.isfile("theme_news_agent/agent.py"), "The file 'theme_news_agent/agent.py' should exist."

def test_sub_agents_directory_exists():
    """Test case 1.1.5: Check if the sub_agents directory exists in the package directory (now root)."""
    assert os.path.isdir("theme_news_agent/sub_agents"), "The directory 'theme_news_agent/sub_agents/' should exist."

def test_specific_sub_agent_directories_exist():
    """Test case 1.1.6: Check if specific sub-agent directories exist."""
    base_path = "theme_news_agent/sub_agents"
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

def test_sub_agent_internal_structure_exists():
    """Test case 1.1.7: Check if required files/dirs exist inside sub-agent directories."""
    base_path = "theme_news_agent/sub_agents"
    structure = {
        "data_collection": [("agent.py", os.path.isfile), ("tools", os.path.isdir)],
        "keyword_extraction": [("agent.py", os.path.isfile), ("prompt.py", os.path.isfile)],
        "theme_clustering": [("agent.py", os.path.isfile), ("prompt.py", os.path.isfile)],
        "trend_analysis": [("agent.py", os.path.isfile), ("tools", os.path.isdir)],
        "summary_generation": [("agent.py", os.path.isfile), ("prompt.py", os.path.isfile)],
    }

    for sub_agent, items in structure.items():
        for item_name, check_func in items:
            path = os.path.join(base_path, sub_agent, item_name)
            assert check_func(path), f"The item '{path}' should exist and be of the correct type."

def test_sub_agent_init_files_exist():
    """Test case 1.1.8: Check if __init__.py files exist in sub_agents and its subdirectories."""
    base_path = "theme_news_agent/sub_agents"
    # Check __init__.py in sub_agents itself
    init_path = os.path.join(base_path, "__init__.py")
    assert os.path.isfile(init_path), f"The file '{init_path}' should exist."

    # Check __init__.py in each sub-agent directory
    sub_agent_dirs = [
        "data_collection",
        "keyword_extraction",
        "theme_clustering",
        "trend_analysis",
        "summary_generation"
    ]
    for dir_name in sub_agent_dirs:
        init_path = os.path.join(base_path, dir_name, "__init__.py")
        assert os.path.isfile(init_path), f"The file '{init_path}' should exist."

def test_deployment_directory_exists():
    """Test case 1.1.9: Check if the deployment directory exists."""
    assert os.path.isdir("theme_news_agent/deployment"), "The directory 'theme_news_agent/deployment/' should exist."

def test_eval_directory_exists():
    """Test case 1.1.10: Check if the eval directory exists."""
    assert os.path.isdir("theme_news_agent/eval"), "The directory 'theme_news_agent/eval/' should exist."

def test_tests_directory_exists():
    """Test case 1.1.11: Check if the tests directory exists at the project root."""
    assert os.path.isdir("tests"), "The directory 'tests/' should exist at the project root."

def test_data_directory_exists():
    """Test case 4.2.1: Check if the data directory exists inside theme_news_agent."""
    assert os.path.isdir("theme_news_agent/data"), "The directory 'theme_news_agent/data/' should exist." 