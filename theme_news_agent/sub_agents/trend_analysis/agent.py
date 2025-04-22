"""Trend Analysis Agent implementation."""

import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from google.adk import Agent
# from google.adk.runtime.context import InvocationContext # 이전 경로 주석 처리
from google.adk.agents.invocation_context import InvocationContext # 새로운 경로로 수정
from google.adk.tools.function_tool import FunctionTool # FunctionTool 임포트 추가

# Import the specific tool instance
from .tools.stats_tool import calculate_trends_tool

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TrendAnalysisAgent(Agent):
    """
    Agent responsible for analyzing clustered themes to identify trends
    by comparing current mention counts with historical data using Z-scores.
    """
    # stats_tool 속성 명시적 선언 (타입 힌트 포함)
    stats_tool: FunctionTool = calculate_trends_tool

    def __init__(self):
        """Initializes the TrendAnalysisAgent."""
        super().__init__(
            name="trend_analysis_agent",
            description="Analyzes theme trends based on historical data and Z-scores.",
            # tools=[calculate_trends_tool], # Agent 상속시 tools 등록 불필요, 직접 호출
        )
        # 클래스 변수로 선언했으므로 __init__에서 다시 할당할 필요 없음
        # self.stats_tool = calculate_trends_tool

    async def process(self, ctx: InvocationContext) -> str:
        """
        Processes the clustered themes to calculate Z-scores, rank trends,
        and prepares the results for the next agent.
        """
        logger.info("TrendAnalysisAgent process started.")

        # 1. Load clustered_themes from state
        clustered_themes = ctx.state.get("clustered_themes")
        if not clustered_themes or not isinstance(clustered_themes, list):
            msg = "Error: 'clustered_themes' not found or invalid in state."
            logger.error(msg)
            return msg

        logger.info(f"Loaded {len(clustered_themes)} clustered themes from state.")

        try:
            # 2. Call calculate_trends tool function directly
            # Since calculate_trends is synchronous, we call its underlying func
            # (Alternatively, if it were async, we might await self.stats_tool.run_async(...))
            # ADK Agent doesn't automatically run tools defined in __init__ like LlmAgent
            # We need to call the tool logic ourselves.
            logger.info("Calling calculate_trends tool...")
            themes_with_zscores = self.stats_tool.func(clustered_themes)
            logger.info(f"Calculated Z-scores for {len(themes_with_zscores)} themes.")

            # 3. Sort themes by Z-score (descending)
            # Handle potential non-numeric z_score defensively, although unlikely
            sorted_themes = sorted(
                [t for t in themes_with_zscores if isinstance(t.get('z_score'), (int, float))],
                key=lambda x: x.get('z_score', float('-inf')), # Default to -infinity if key missing
                reverse=True
            )
            logger.info("Sorted themes by Z-score.")

            # 4. Get top N trends from environment variable
            top_n = 20 # Start with default value
            top_n_str = os.getenv("TREND_TOP_N") # Get value without default first
            if top_n_str is not None: # Check if env var was actually set
                try:
                    temp_top_n = int(top_n_str)
                    if temp_top_n > 0:
                        top_n = temp_top_n # Use valid positive value from env var
                        logger.info(f"Using TREND_TOP_N={top_n} from environment variable.")
                    else:
                        logger.warning(f"TREND_TOP_N ({top_n_str}) is not positive. Using default {top_n}.")
                except ValueError:
                    logger.warning(f"Invalid TREND_TOP_N value: '{top_n_str}'. Using default {top_n}.")
            # else: logger.info(f"TREND_TOP_N not set. Using default {top_n}.") # Optional: Log default usage

            top_themes = sorted_themes[:top_n]
            logger.info(f"Selected top {len(top_themes)} themes based on TREND_TOP_N setting (resolved to {top_n}).")

            # 5. Add rank to themes
            ranked_themes = []
            for i, theme in enumerate(top_themes):
                theme['rank'] = i + 1
                ranked_themes.append(theme)
            logger.info("Added rank to top themes.")

            # 6. Save ranked_themes to state (Task 5.4)
            ctx.state["trend_results"] = ranked_themes
            logger.info("Saved ranked trend results to state.")

            return f"Trend analysis complete. Top {len(ranked_themes)} trends identified and saved."

        except Exception as e:
            logger.error(f"Error during trend analysis process: {e}", exc_info=True)
            return f"Error during trend analysis: {e}"
