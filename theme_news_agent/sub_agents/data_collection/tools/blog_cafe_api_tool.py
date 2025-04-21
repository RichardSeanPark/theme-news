import os
import requests
from datetime import datetime
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import re # For HTML tag removal
from typing import List, Dict, Any # typing 추가

# .env 파일 로드 (필요시)
load_dotenv()

# --- Helper 함수 ---

def _clean_html(raw_html: str) -> str:
    """간단한 HTML 태그 제거"""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    # 알려진 HTML 엔티티 수동 처리 (필요에 따라 추가)
    cleantext = cleantext.replace('&quot;', '"')
    cleantext = cleantext.replace('&amp;', '&')
    cleantext = cleantext.replace('&lt;', '<')
    cleantext = cleantext.replace('&gt;', '>')
    cleantext = cleantext.replace('&nbsp;', ' ')
    return cleantext

def _parse_naver_datetime(datetime_str: str) -> str | None:
    """Naver API 날짜 형식(RFC 1123 or YYYYMMDD)을 ISO 8601 형식으로 변환 시도"""
    if not datetime_str:
        return None
    try:
        # RFC 1123 형식 시도 (pubDate)
        dt_object = datetime.strptime(datetime_str, '%a, %d %b %Y %H:%M:%S %z')
        return dt_object.isoformat()
    except ValueError:
        try:
            # YYYYMMDD 형식 시도 (postdate)
            dt_object = datetime.strptime(datetime_str, '%Y%m%d')
            return dt_object.isoformat() # 시간 정보는 없으므로 자정으로 표시될 수 있음
        except ValueError:
            print(f"경고: 날짜 형식 변환 실패 - {datetime_str}")
            return None # 두 형식 모두 실패 시 None 반환

def _fetch_naver_search_api(api_type: str, query: str, display: int = 100, sort: str = 'date') -> list[dict]:
    """Naver 검색 API (블로그/카페) 호출 및 결과 파싱 공통 로직"""
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(f"오류: NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경 변수가 설정되지 않았습니다. ({api_type})")
        return []

    base_url = f"https://openapi.naver.com/v1/search/{api_type}.json"
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
        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        for item in items:
            title = _clean_html(item.get("title", ""))
            description = _clean_html(item.get("description", ""))
            source_name = f"{item.get('cafename')} ({item.get('cafeurl')})" if api_type == 'cafearticle' else item.get('bloggername', 'Naver Blog')
            # 네이버 문서 기준 Blog는 postdate (YYYYMMDD), Cafe는 pubDate (RFC1123) 사용
            date_field = "postdate" if api_type == 'blog' else "pubDate"
            published_iso = _parse_naver_datetime(item.get(date_field))

            articles_data.append({
                "title": title,
                "content": description,
                "source": source_name,
                "published": published_iso,
                "url": item.get("link")
            })
    except requests.exceptions.RequestException as e:
        print(f"Naver {api_type.capitalize()} API 호출 오류: {e}")
    except Exception as e:
        print(f"Naver {api_type.capitalize()} 데이터 처리 오류: {e}")
    return articles_data

# --- 함수 정의 (기존과 동일하게 유지, 실제 호출은 클래스 메서드 통해) ---
def _fetch_naver_blogs_func(query: str = "후기", display: int = 100, sort: str = 'date') -> list[dict]: # 기본 query 변경
    """
    Naver 검색 API (블로그)를 사용하여 특정 쿼리로 블로그 포스트를 검색합니다.
    (https://developers.naver.com/docs/serviceapi/search/blog/Blog.md#%EB%B8% 블로그)
    Args:
        query: 검색할 키워드 (예: "오늘", "방법", "후기", "최신" 등).
        display: 결과 개수 (최대 100).
        sort: 정렬 옵션 ('sim': 유사도순, 'date': 날짜순).
    Returns:
        블로그 포스트 정보 딕셔너리 리스트. 형식은 ArticleData와 유사.
    """
    return _fetch_naver_search_api('blog', query, display, sort)

def _fetch_naver_cafe_articles_func(query: str = "정보", display: int = 100, sort: str = 'date') -> list[dict]: # 기본 query 변경
    """
    Naver 검색 API (카페)를 사용하여 특정 쿼리로 카페 글을 검색합니다.
    (https://developers.naver.com/docs/serviceapi/search/cafearticle/Cafearticle.md#%EC%B9%B4%ED%8E%98%EA%B8%80)
    Args:
        query: 검색할 키워드.
        display: 결과 개수 (최대 100).
        sort: 정렬 옵션 ('sim': 유사도순, 'date': 날짜순).
    Returns:
        카페 글 정보 딕셔너리 리스트. 형식은 ArticleData와 유사.
    """
    # 카페 API 문서 상 'date' 정렬은 지원하지 않음 명시. 'sim'이 기본값.
    return _fetch_naver_search_api('cafearticle', query, display, sort)


# --- BlogCafeApiTool 클래스 정의 ---
class BlogCafeApiTool:
    """
    네이버 블로그 및 카페 검색 API 함수들을 FunctionTool로 감싸 제공하는 클래스입니다.
    """
    def __init__(self):
        self.fetch_naver_blogs = FunctionTool(func=_fetch_naver_blogs_func)
        self.fetch_naver_cafe_articles = FunctionTool(func=_fetch_naver_cafe_articles_func)

    # 편의 메서드 (Agent에서 사용할 수 있음)
    def fetch_all_blogs_cafes(self, blog_query: str = "후기", cafe_query: str = "정보") -> List[Dict[str, Any]]:
        all_results = []
        all_results.extend(self.fetch_naver_blogs(query=blog_query))
        all_results.extend(self.fetch_naver_cafe_articles(query=cafe_query))
        return all_results

# --- 기존 FunctionTool 인스턴스 생성 코드 제거 ---
# fetch_naver_blogs = FunctionTool(func=fetch_naver_blogs_func)
# fetch_naver_cafe_articles = FunctionTool(func=fetch_naver_cafe_articles_func)

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요
# TODO: published 필드 파싱 확인 (블로그는 postdate, 카페는 pubDate 가 맞는지?) - 네이버 문서에는 Blog, Cafe 모두 pubDate로 되어 있음. 현재 코드는 postdate 우선 시도.
# TODO: news_api_tool.py 와 공통 헬퍼 함수 (_clean_html, _parse_naver_datetime 등) 분리 고려 