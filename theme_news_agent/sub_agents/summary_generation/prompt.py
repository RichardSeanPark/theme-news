"""Defines the prompt for the Summary Generation Agent."""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Basic prompt template for summary generation
SUMMARY_PROMPT_TEMPLATE = """
당신은 최신 트렌드 분석 결과를 바탕으로 간결하고 통찰력 있는 뉴스 요약 보고서를 작성하는 AI 기자입니다.

다음은 최근 분석된 상위 트렌드 테마 목록입니다. 각 테마는 순위(rank)와 Z-점수(z_score)를 가지고 있으며, Z-점수가 높을수록 최근 언급량이 과거 평균에 비해 급증했음을 의미합니다.

[상위 트렌드 테마 목록]
{trend_data_str}

[요청 사항]
위 트렌드 테마 목록을 바탕으로 다음 요구사항에 맞춰 뉴스 요약 보고서를 작성해 주세요:
1.  **핵심 트렌드 요약:** 가장 주목할 만한 상위 1-3개 트렌드를 선정하고, 왜 이 테마들이 중요하거나 주목받는지 간략히 설명합니다.
2.  **주요 내용:** 전체적인 트렌드 흐름을 설명하고, 새롭게 등장하거나 급부상한 테마가 있다면 강조합니다.
3.  **형식:** 자연스러운 한국어 문장으로 작성하며, 뉴스 기사 스타일을 따릅니다.
4.  **분량:** 전체 보고서는 3-5 문장 내외로 간결하게 작성합니다.

[뉴스 요약 보고서]
"""

def get_summary_prompt(trend_results: List[Dict[str, Any]]) -> str:
    """
    Generates the final prompt string for the LLM based on the trend results.

    Args:
        trend_results: A list of dictionaries, where each dictionary represents
                       a ranked theme with at least 'rank', 'theme', and 'z_score'.

    Returns:
        The formatted prompt string ready for the LLM.
    """
    if not trend_results:
        logger.warning("No trend results provided for summary generation.")
        # Return a modified prompt indicating no data, or handle as error upstream?
        # For now, let's format it so the LLM knows there's nothing to summarize.
        trend_data_str = "분석된 트렌드 테마가 없습니다."
    else:
        formatted_trends = []
        for theme_data in trend_results:
            try:
                rank = theme_data.get('rank', 'N/A')
                theme = theme_data.get('theme', '알 수 없는 테마')
                # Format z_score to 2 decimal places if it exists and is a number
                z_score_raw = theme_data.get('z_score')
                if isinstance(z_score_raw, (int, float)):
                    z_score_str = f"{z_score_raw:.2f}"
                else:
                    z_score_str = "N/A"

                formatted_trends.append(
                    f"- 순위 {rank}: {theme} (Z-점수: {z_score_str})"
                )
            except Exception as e:
                logger.error(f"Error formatting theme data: {theme_data}. Error: {e}")
                formatted_trends.append(f"- (오류: 데이터 포맷팅 실패)")

        trend_data_str = "\n".join(formatted_trends)

    # Populate the template
    try:
        final_prompt = SUMMARY_PROMPT_TEMPLATE.format(trend_data_str=trend_data_str)
        return final_prompt
    except KeyError as e:
        logger.error(f"Error formatting summary prompt template. Missing key: {e}")
        # Return a fallback prompt or raise an exception
        return "Error: Could not generate the summary prompt due to a template issue."
