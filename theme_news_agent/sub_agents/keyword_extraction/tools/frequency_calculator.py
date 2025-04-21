import re
from typing import List, Dict, Any
from collections import Counter, defaultdict

# 데이터 모델 임포트 (경로 주의)
from theme_news_agent.sub_agents.data_collection.models import CollectedData, ArticleData

def calculate_keyword_frequencies(keywords: List[str], collected_data: CollectedData) -> List[Dict[str, Any]]:
    """
    주어진 키워드 목록에 대해 CollectedData 내에서 출처별 빈도수를 계산합니다.

    Args:
        keywords: 빈도수를 계산할 키워드 문자열 리스트.
        collected_data: 다양한 출처의 ArticleData를 포함하는 CollectedData 객체.

    Returns:
        각 키워드별 전체 및 출처별 빈도 정보를 포함하는 딕셔너리 리스트.
        예: [{ "keyword": "ai", "frequency": { "total": 15, "news": 5, "blogs": 3, "cafes": 2, "finance": 0, "search": 5 } }, ...]
    """
    keyword_frequency_data = []
    all_articles = collected_data.get_all_articles() # 모든 기사/데이터 가져오기

    # 소스 유형을 매핑하는 도우미 함수 또는 딕셔너리 (개선 가능)
    def get_source_category(source: str) -> str:
        source_lower = source.lower()
        if "newsapi" in source_lower or "nytimes" in source_lower or "naver news" in source_lower:
            return "news"
        elif "naver blog" in source_lower:
            return "blogs"
        elif "naver cafe" in source_lower:
            return "cafes"
        elif "finance" in source_lower: # 예: "Yahoo Finance Trending"
            return "finance"
        elif "trends" in source_lower: # 예: "Google Trends", "Naver DataLab"
            return "search"
        else:
            return "other" # 기타 또는 분류 불가

    for keyword in keywords:
        # 대소문자 구분 없이 키워드 검색을 위한 정규식 패턴 준비
        # 수정: 단어 경계를 Lookaround Assertion으로 변경 (?<!\w)keyword(?<!\w)
        # 특수문자 키워드는 re.escape 결과를 보고 추가 조정 필요 가능성 있음
        escaped_keyword = re.escape(keyword)
        # C++ 같은 경우 \bC\+\+\b 패턴은 +, 공백 조합 때문에 매치 어려움. 
        # 좀 더 복잡한 패턴이나 후처리가 필요할 수 있으나, 일단 lookaround로 시도.
        pattern = re.compile(r"(?<!\w)" + escaped_keyword + r"(?!\w)", re.IGNORECASE)
        
        frequency = defaultdict(int) # 출처별 빈도 (기본값 0)
        total_frequency = 0

        for article in all_articles:
            text_to_search = f"{article.title or ''} {article.content or ''}"
            matches = pattern.findall(text_to_search)
            count = len(matches)

            if count > 0:
                source_category = get_source_category(article.source or "unknown")
                frequency[source_category] += count
                total_frequency += count

        frequency["total"] = total_frequency

        # 결과 형식에 맞게 변환
        keyword_frequency_data.append({
            "keyword": keyword,
            "frequency": dict(frequency) # defaultdict를 일반 dict로 변환
        })

    return keyword_frequency_data 