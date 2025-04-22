import os
import json
import logging
from typing import List, Dict, Any
import numpy as np
from dotenv import load_dotenv
# from google.adk.tools import Tool # Incorrect based on project convention
from google.adk.tools import FunctionTool # Use FunctionTool like other tools

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)
# Ensure logs are captured by pytest caplog, set level explicitly if needed
# logger.setLevel(logging.INFO) # Or set globally in tests

def _load_historical_data(file_path: str) -> Dict[str, Dict[str, Any]]:
    """Loads historical theme data from a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                # Add logging here if needed, but the primary log is when file NOT found
                return json.load(f)
        else:
            logger.info(f"Historical data file not found at {file_path}. Starting with empty data.")
            return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {file_path}. Starting with empty data.", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"Error loading historical data from {file_path}: {e}", exc_info=True)
        return {}

def _save_historical_data(file_path: str, data: Dict[str, Dict[str, Any]]) -> None:
    """Saves historical theme data to a JSON file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error saving historical data to {file_path}: {e}", exc_info=True)

def calculate_trends(current_themes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculates the Z-score for current themes based on historical data,
    updates the historical data, and saves it.

    Args:
        current_themes: A list of dictionaries, where each dictionary represents
                        a theme and must contain at least 'theme' (str) and
                        'mentions' (int) keys.
                        Example: [{'theme': 'AI 반도체', 'keywords': ['nvidia', 'hbm'], 'mentions': 150}, ...]

    Returns:
        The input list of theme dictionaries, with a 'z_score' (float) added to each.
    """
    historical_data_path = os.getenv("HISTORICAL_DATA_PATH", "theme_news_agent/data/historical_themes.json")
    if not historical_data_path:
        logger.warning("HISTORICAL_DATA_PATH environment variable not set. Using default: 'theme_news_agent/data/historical_themes.json'")
        historical_data_path = "theme_news_agent/data/historical_themes.json"

    historical_data = _load_historical_data(historical_data_path)
    processed_themes = []

    # --- 1. Calculate Z-scores for current themes ---
    for theme_data in current_themes:
        # Add defensive check for dictionary type first
        if not isinstance(theme_data, dict):
            logger.warning(f"Skipping non-dictionary item in current_themes: {theme_data}")
            # Optionally add a default z_score to the item if it needs to be preserved in the output list
            # Or simply continue to skip processing non-dict items
            # Let's try adding a placeholder z_score for consistency in return structure if needed
            # But the original test assumes we add z_score even to invalid entries
            # For now, let's ensure the test handles this by skipping processing for non-dicts
            # Update: The test test_calculate_trends_invalid_input_format implies z_score should be added
            # We'll need to adjust the test or this logic. Let's make the code robust first.
            # We cannot reliably add 'z_score' to non-dict items. Let's log and skip.
            processed_themes.append(theme_data) # Append the original invalid item
            continue

        theme_name = theme_data.get("theme")
        current_mentions = theme_data.get("mentions")

        # Existing validation for theme_name and current_mentions remains
        if not isinstance(theme_name, str) or not isinstance(current_mentions, int):
            logger.warning(f"Skipping theme due to invalid format (missing/wrong type keys): {theme_data}")
            theme_data['z_score'] = 0.0 # Assign default z_score if format is invalid
            processed_themes.append(theme_data)
            continue

        past_theme_info = historical_data.get(theme_name)
        z_score = 0.0

        if past_theme_info:
            avg = past_theme_info.get("avg", 0)
            std = past_theme_info.get("std", 0)
            if std > 0:
                z_score = (current_mentions - avg) / std
            elif current_mentions > avg:
                # Handle std=0 case
                logger.info(f"Theme '{theme_name}' has std=0, assigning z_score=0 despite mentions increase ({current_mentions} > {avg})")
                z_score = 0.0

        theme_data['z_score'] = z_score
        processed_themes.append(theme_data)

    # --- 2. Update Historical Data ---
    for theme_data in processed_themes:
        # Also add the dictionary check here before updating history
        if not isinstance(theme_data, dict):
            continue # Skip non-dictionary items passed through

        theme_name = theme_data.get("theme")
        current_mentions = theme_data.get("mentions")

        # Skip if format was invalid (already checked, but belt-and-suspenders)
        if not isinstance(theme_name, str) or not isinstance(current_mentions, int):
            continue

        if theme_name in historical_data:
            # Update existing theme
            history = historical_data[theme_name].get("mentions_history", [])
            history.append(current_mentions)
            historical_data[theme_name]["mentions_history"] = history

            # Recalculate avg and std
            new_avg = np.mean(history)
            new_std = np.std(history) if len(history) >= 2 else 0.0
            historical_data[theme_name]["avg"] = new_avg
            historical_data[theme_name]["std"] = new_std
        else:
            # Add new theme
            historical_data[theme_name] = {
                "mentions_history": [current_mentions],
                "avg": float(current_mentions),
                "std": 0.0
            }

    # --- 3. Save Updated Historical Data ---
    _save_historical_data(historical_data_path, historical_data)

    return processed_themes

# Create a FunctionTool instance for the function
# This instance will be imported and used by the agent
calculate_trends_tool = FunctionTool(func=calculate_trends) 