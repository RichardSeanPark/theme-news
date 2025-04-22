# theme_news_agent/sub_agents/theme_clustering/prompt.py

# Design.md 섹션 4 (3) 및 Dev_Plan.md 섹션 5.3 참고하여 작성
# LLM에게 키워드 목록(언급량 포함)을 입력받아
# 의미적으로 유사/연관된 키워드를 그룹화하고 각 그룹에 이해하기 쉬운 테마 이름을 부여하도록 지시.
# 출력 형식은 반드시 JSON 배열: [{"theme": "...", "keywords": ["...", ...], "mentions": N}, ...]

CLUSTERING_PROMPT_TEMPLATE = """
당신은 대량의 키워드 데이터를 분석하여 숨겨진 주제(테마)를 발견하는 전문가입니다.
다음은 최근 수집된 주요 키워드와 각 키워드의 총 언급 횟수 목록입니다.

{keyword_data_str}

위 키워드 목록을 주의 깊게 분석하여, 의미적으로 서로 강하게 연관되거나 유사한 키워드들을 그룹화해주세요.
각 그룹(클러스터)에 대해 가장 핵심적인 내용을 나타내는 간결하고 이해하기 쉬운 테마 이름을 한국어로 부여해주세요.

결과는 반드시 다음 JSON 형식의 배열로만 반환해야 합니다. 다른 설명이나 부가 정보는 절대 포함하지 마세요.

[
  {{
    "theme": "첫 번째 테마 이름 (예: AI 기술 발전)",
    "keywords": ["관련 키워드1", "관련 키워드2", ...],
    "mentions": 해당 테마에 속한 모든 키워드의 총 언급 횟수 합계 (정수)
  }},
  {{
    "theme": "두 번째 테마 이름 (예: 전기차 시장 동향)",
    "keywords": ["관련 키워드 A", "관련 키워드 B", ...],
    "mentions": 해당 테마에 속한 모든 키워드의 총 언급 횟수 합계 (정수)
  }},
  ...
]

각 테마의 "mentions" 값은 해당 테마에 포함된 모든 키워드들의 언급 횟수를 합산한 정확한 정수 값이어야 합니다.
의미적으로 관련성이 낮은 키워드는 그룹에 포함시키지 않을 수 있습니다.
최대한 포괄적이면서도 의미 있는 테마들을 추출해주세요.
"""

def get_clustering_prompt(keyword_results: list[dict]) -> str:
    """
    키워드 빈도 결과 리스트를 입력받아 LLM 클러스터링 프롬프트 문자열을 생성합니다.

    Args:
        keyword_results: 키워드와 빈도 정보 딕셔너리 리스트.
                         예: [{"keyword": "AI", "frequency": {"total": 50, ...}}, ...]

    Returns:
        LLM에 전달될 완성된 프롬프트 문자열.
    """
    # 키워드 데이터를 "키워드 (언급횟수)" 형식의 문자열로 변환
    keyword_lines = []
    for item in keyword_results:
        keyword = item.get("keyword", "N/A")
        total_freq = item.get("frequency", {}).get("total", 0)
        keyword_lines.append(f"- {keyword} ({total_freq}회 언급)")

    keyword_data_str = "\n".join(keyword_lines)
    if not keyword_data_str:
        keyword_data_str = "분석할 키워드가 없습니다."

    return CLUSTERING_PROMPT_TEMPLATE.format(keyword_data_str=keyword_data_str)
