from pytrends.request import TrendReq
import pandas as pd
import requests # URL 인코딩 위해 추가
from datetime import datetime, timezone
from google.adk.tools import FunctionTool
import logging
from typing import List, Dict, Any # typing 추가

# Logging 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- 함수 정의 ---

def _fetch_google_trends_func(region: str = 'KR') -> list[dict]: # 함수 이름 변경 (_ 추가)
    """
    Google Trends에서 특정 지역의 일간 인기 급상승 검색어를 가져옵니다.
    (pytrends 라이브러리 사용)

    Args:
        region (str): 트렌드를 가져올 지역 코드 (예: 'KR' - 한국, 'US' - 미국). 기본값은 'KR'.

    Returns:
        인기 검색어 정보 딕셔너리 리스트. 각 딕셔너리는 다음 키를 포함:
        - title (str): 인기 검색어
        - content (None): 해당 없음
        - source (str): "Google Trends [지역코드]"
        - published (str): 데이터 수집 시각 (ISO 8601 형식)
        - url (str): 해당 검색어의 Google Trends URL
    """
    pytrends = TrendReq(hl='en-US', tz=360) # language 설정 명시
    trending_searches_data = []
    collection_time = datetime.now(timezone.utc).isoformat()

    try:
        logger.info(f"Fetching Google Trends daily trending searches for region: {region}")
        # 일간 인기 급상승 검색어 가져오기
        daily_trends_df = pytrends.trending_searches(pn=region.lower()) # 지역코드 소문자 사용

        if isinstance(daily_trends_df, pd.DataFrame) and not daily_trends_df.empty:
            logger.info(f"Successfully fetched {len(daily_trends_df)} trending searches.")
            for term in daily_trends_df[0].tolist(): # 첫 번째 컬럼이 검색어
                # Google Trends URL 생성 (간단 버전)
                term_encoded = requests.utils.quote(term)
                google_trends_url = f"https://trends.google.com/trends/explore?q={term_encoded}&geo={region}"

                trending_searches_data.append({
                    "title": term,
                    "content": None,
                    "source": f"Google Trends {region.upper()}",
                    "published": collection_time,
                    "url": google_trends_url
                })
        else:
            logger.warning(f"No daily trending searches found for region: {region}")

    except Exception as e:
        # pytrends 라이브러리 관련 오류 또는 네트워크 오류 등
        logger.error(f"Error fetching Google Trends for region {region}: {e}", exc_info=True) # 상세 오류 추가

    return trending_searches_data

def _fetch_naver_datalab_trends_func() -> list[dict]: # 함수 이름 변경 (_ 추가)
    """
    (구현 예정) Naver DataLab 또는 관련 API를 사용하여 네이버 급상승 검색어를 가져옵니다.
    현재는 빈 리스트를 반환합니다.
    """
    logger.warning("fetch_naver_datalab_trends_func is not implemented yet.")
    return []


# --- SearchTrendTool 클래스 정의 ---
class SearchTrendTool:
    """
    검색 트렌드 (Google Trends, Naver DataLab) 함수들을
    FunctionTool로 감싸 제공하는 클래스입니다.
    """
    def __init__(self):
        self.fetch_google_trends = FunctionTool(func=_fetch_google_trends_func)
        self.fetch_naver_datalab_trends = FunctionTool(func=_fetch_naver_datalab_trends_func)

    # 편의 메서드
    def fetch_all_trends(self, google_region: str = 'KR') -> List[Dict[str, Any]]:
        all_trends = []
        all_trends.extend(self.fetch_google_trends(region=google_region))
        all_trends.extend(self.fetch_naver_datalab_trends()) # 아직 구현 안됨
        return all_trends

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요
# TODO: fetch_naver_datalab_trends_func 구현 (스크래핑 또는 비공식 API 사용)
# TODO: pytrends 오류 처리 세분화 (예: 네트워크 오류, API 제한 등) 