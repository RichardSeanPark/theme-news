import subprocess
import os

def test_env_is_ignored():
    """Test case 3.2.1: Check if theme_news_agent/.env is ignored by git."""
    # Ensure the .env file exists for the check-ignore command to work properly
    env_path = "theme_news_agent/.env"
    if not os.path.exists(env_path):
        # Create a dummy .env file if it doesn't exist
        with open(env_path, 'w') as f:
            f.write("DUMMY_VAR=test")
            
    try:
        # Run git check-ignore. It should exit with 0 if the file is ignored.
        result = subprocess.run(["git", "check-ignore", env_path], capture_output=True, text=True, check=True)
        # Check if the output is the path itself
        assert result.stdout.strip() == env_path
    except subprocess.CalledProcessError as e:
        # If check=True and the command returns non-zero exit status, CalledProcessError is raised.
        # A non-zero exit status means the file is NOT ignored.
        assert False, f"git check-ignore failed for {env_path}. It might not be ignored. Error: {e}"
    except FileNotFoundError:
        assert False, "'git' command not found. Please ensure Git is installed and in PATH."
    except Exception as e:
        assert False, f"An unexpected error occurred: {e}"

def test_data_dir_is_ignored():
    """Test case 4.2.2: Check if theme_news_agent/data/ is ignored by git."""
    data_path = "theme_news_agent/data/"
    # Ensure the directory exists for check-ignore
    os.makedirs(data_path, exist_ok=True)
    # Create a dummy file inside for the check-ignore command (ignoring a dir needs a file)
    dummy_file_path = os.path.join(data_path, ".dummy")
    if not os.path.exists(dummy_file_path):
         with open(dummy_file_path, 'w') as f:
            f.write("dummy")

    try:
        # Run git check-ignore. It should exit with 0 if the path is ignored.
        result = subprocess.run(["git", "check-ignore", data_path], capture_output=True, text=True, check=True)
        # Check if the output is the path itself (Git 2.42+) or empty (older Git versions)
        # For directories, check-ignore might just exit 0 without output on older versions.
        # We primarily rely on the exit code (check=True handles this).
        # Optionally, check if the output matches the path if not empty.
        if result.stdout.strip():
             assert result.stdout.strip() == data_path
        # If stdout is empty, the check=True already verified it's ignored.
    except subprocess.CalledProcessError as e:
        assert False, f"git check-ignore failed for {data_path}. It might not be ignored. Error: {e}"
    except FileNotFoundError:
        assert False, "'git' command not found. Please ensure Git is installed and in PATH."
    except Exception as e:
        assert False, f"An unexpected error occurred: {e}"
    finally:
        # Clean up the dummy file
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)
