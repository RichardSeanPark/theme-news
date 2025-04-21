import os
import requests
import inspect
from datetime import datetime, timedelta
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
from typing import List, Dict, Any # typing 추가
# from ..models import ArticleData # ArticleData 임포트는 agent.py에서 처리하므로 여기서는 제거하거나 주석처리 (순환참조 방지)

# .env 파일 로드 (한 번만 실행)
load_dotenv()

# --- Helper 함수 ---
def get_date_range() -> tuple[str, str]:
    """설정된 기간 전부터 현재까지의 날짜 범위를 ISO 형식 문자열로 반환합니다."""
    period_hours = int(os.getenv("DATA_FETCH_PERIOD_HOURS", 24)) # 함수 호출 시 로드
    now = datetime.now()
    past = now - timedelta(hours=period_hours)
    to_date_str = now.strftime('%Y-%m-%d')
    from_date_str = past.strftime('%Y-%m-%d')
    return from_date_str, to_date_str

# --- API 호출 함수 (클래스 내부로 이동 고려 또는 이대로 두고 클래스에서 호출) ---
# (함수 정의는 기존과 동일하게 유지)
def _fetch_newsapi_headlines_func(country: str = 'kr', category: str = 'general', page_size: int = 100) -> list[dict]:
    """
    NewsAPI (newsapi.org)를 사용하여 특정 국가의 최신 헤드라인 뉴스를 가져옵니다.
    (https://newsapi.org/docs/endpoints/top-headlines)

    Args:
        country: 뉴스를 가져올 국가 코드 (예: 'kr', 'us').
        category: 가져올 뉴스 카테고리 (예: 'general', 'business', 'technology').
        page_size: 가져올 최대 기사 수.

    Returns:
        뉴스 기사 정보 딕셔너리 리스트.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("오류: NEWS_API_KEY 환경 변수가 설정되지 않았습니다.")
        return []
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category,
        'pageSize': page_size,
    }
    articles_data = []
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            for article in data.get("articles", []):
                articles_data.append({
                    "title": article.get("title"),
                    "content": article.get("description"),
                    "source": article.get("source", {}).get("name", "NewsAPI"),
                    "published": article.get("publishedAt"),
                    "url": article.get("url")
                })
    except requests.exceptions.RequestException as e:
        print(f"NewsAPI 호출 오류: {e}")
    except Exception as e:
        print(f"NewsAPI 데이터 처리 오류: {e}")
    return articles_data

def _fetch_nytimes_articles_func(query: str = 'korea', page_size: int = 10) -> list[dict]:
    """
    New York Times Article Search API를 사용하여 특정 쿼리로 기사를 검색합니다.
    (https://developer.nytimes.com/docs/articlesearch-product/1/routes/articlesearch.json/get)

    Args:
        query: 검색할 키워드.
        page_size: 가져올 최대 기사 수 (API 페이징 고려).

    Returns:
        뉴스 기사 정보 딕셔너리 리스트.
    """
    api_key = os.getenv("NYT_API_KEY")
    if not api_key:
        print("오류: NYT_API_KEY 환경 변수가 설정되지 않았습니다.")
        return []
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    from_date, to_date = get_date_range()
    begin_date = from_date.replace('-', '')
    end_date = to_date.replace('-', '')
    params = {
        'api-key': api_key,
        'q': query,
        'begin_date': begin_date,
        'end_date': end_date,
        'sort': 'newest',
        'page': 0
    }
    articles_data = []
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "OK":
            docs_to_fetch = data.get("response", {}).get("docs", [])[:page_size]
            for doc in docs_to_fetch:
                articles_data.append({
                    "title": doc.get("headline", {}).get("main"),
                    "content": doc.get("snippet"),
                    "source": doc.get("source", "The New York Times"),
                    "published": doc.get("pub_date"),
                    "url": doc.get("web_url")
                })
    except requests.exceptions.RequestException as e:
        print(f"NYTimes API 호출 오류: {e}")
    except Exception as e:
        print(f"NYTimes 데이터 처리 오류: {e}")
    return articles_data

def _fetch_naver_news_func(query: str = "IT", display: int = 100, sort: str = 'date') -> list[dict]: # 기본 query 변경
    """
    Naver 검색 API (뉴스)를 사용하여 특정 쿼리로 뉴스를 검색합니다.
    (https://developers.naver.com/docs/serviceapi/search/news/News.md#%EB%89%B4%EC%8A%A4)

    Args:
        query: 검색할 키워드.
        display: 결과 개수.
        sort: 정렬 옵션.

    Returns:
        뉴스 기사 정보 딕셔너리 리스트.
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("오류: NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경 변수가 설정되지 않았습니다.")
        return []
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
    }
    params = {
        'query': query,
        'display': display,
        'sort': sort,
    }
    articles_data = []
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            title = item.get("title", "").replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            description = item.get("description", "").replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            articles_data.append({
                "title": title,
                "content": description,
                "source": "Naver News", # 출처 명시
                "published": item.get("pubDate"),
                "url": item.get("link")
            })
    except requests.exceptions.RequestException as e:
        print(f"Naver News API 호출 오류: {e}")
    except Exception as e:
        print(f"Naver News 데이터 처리 오류: {e}")
    return articles_data

# --- NewsApiTool 클래스 정의 ---
class NewsApiTool:
    """
    뉴스 관련 API 호출 함수들을 FunctionTool로 감싸 제공하는 클래스입니다.
    DataCollectionAgent에서 이 클래스를 인스턴스화하여 사용합니다.
    """
    def __init__(self):
        # 각 함수를 FunctionTool로 래핑하여 인스턴스 변수로 저장
        # 각 FunctionTool의 name과 description은 ADK에서 자동으로 함수 이름과 독스트링을 사용합니다.
        self.fetch_newsapi_headlines = FunctionTool(func=_fetch_newsapi_headlines_func)
        self.fetch_nytimes_articles = FunctionTool(func=_fetch_nytimes_articles_func)
        self.fetch_naver_news = FunctionTool(func=_fetch_naver_news_func)

    # 각 FunctionTool을 직접 호출할 수 있는 메서드 추가 (테스트 및 Agent에서의 사용 편의성)
    # 반환 타입을 ArticleData 리스트로 변경 (실제로는 Pydantic 모델 사용 권장)
    def fetch_all_news(self) -> List[Dict[str, Any]]: # 예시: 모든 뉴스 소스 호출 메서드
        all_news = []
        all_news.extend(self.fetch_newsapi_headlines()) # FunctionTool 인스턴스 직접 호출
        all_news.extend(self.fetch_nytimes_articles())
        all_news.extend(self.fetch_naver_news(query="IT")) # 기본 쿼리 사용 예시
        # TODO: 실제 ArticleData 모델로 변환하는 로직 추가
        return all_news

# --- 기존 FunctionTool 인스턴스 생성 코드는 클래스 외부에서는 제거 ---
# fetch_newsapi_headlines = FunctionTool(func=fetch_newsapi_headlines_func)
# fetch_nytimes_articles = FunctionTool(func=fetch_nytimes_articles_func)
# fetch_naver_news = FunctionTool(func=fetch_naver_news_func)

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요
# -> ArticleData 모델은 agent.py에서 관리하므로 여기서는 dict 리스트 반환 유지

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요 