import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from google.adk.tools import FunctionTool
import logging # Logging 추가

# Logging 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- 함수 정의 ---

def fetch_trending_tickers_func() -> list[dict]:
    """
    Yahoo Finance 웹사이트에서 'Trending Tickers' 정보를 스크래핑하여 반환합니다.
    (https://finance.yahoo.com/trending-tickers)

    Returns:
        인기 티커 정보 딕셔너리 리스트. 각 딕셔너리는 다음 키를 포함:
        - title (str): 회사명
        - content (str): 티커 심볼
        - source (str): "Yahoo Finance Trending"
        - published (str): 데이터 수집 시각 (ISO 8601 형식)
        - url (None): 해당 없음
    """
    url = "https://finance.yahoo.com/trending-tickers"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    trending_tickers_data = []
    collection_time = datetime.now(timezone.utc).isoformat() # 수집 시각 기록

    try:
        logger.info(f"Fetching trending tickers from: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        logger.info("Parsing HTML content...")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Yahoo Finance 페이지 구조에 의존적. 변경 시 업데이트 필요.
        # 테이블이나 리스트를 찾습니다. (2024년 7월 기준 구조에 기반)
        # 예시: <section data-testid="trending-tickers"> 안에 <ul> 또는 <table> 형태
        # 더 구체적인 선택자 사용 시도 (예: section[data-testid="trending-tickers"] li a[data-symbol])

        # 1. 섹션 찾기 (더 안정적인 방법)
        section = soup.find('section', {'data-testid': 'trending-tickers'})
        if not section:
            logger.warning("Could not find the trending tickers section with data-testid.")
            # 대체 선택자 시도 (예: 클래스 이름 등)
            # table = soup.find('table', class_='...') # 클래스명은 실제 페이지 확인 후 기입
            # if not table:
            #     logger.error("Failed to find trending tickers table using known selectors.")
            #     return []
            return [] # 섹션을 못찾으면 빈 리스트 반환

        # 2. 섹션 내에서 티커 링크(<a> 태그) 찾기
        # <a> 태그의 href 속성에 /quote/SYMBOL? 형태가 포함된 것을 찾음
        ticker_links = section.find_all('a', href=lambda href: href and '/quote/' in href)

        if not ticker_links:
            logger.warning("Found trending tickers section, but no ticker links inside.")
            return []

        logger.info(f"Found {len(ticker_links)} potential ticker links.")

        processed_symbols = set() # 중복 티커 처리

        for link in ticker_links:
            href = link.get('href')
            # 티커 심볼 추출 (예: /quote/AAPL?p=AAPL -> AAPL)
            symbol_match = href.split('/quote/')[-1].split('?')[0]
            if symbol_match and symbol_match not in processed_symbols:
                # 회사명 추출 시도 (<a> 태그의 aria-label 또는 내부 text 활용)
                company_name = link.get('aria-label', link.text.strip())
                # 불필요한 텍스트 제거 (예: "Symbol Lookup")
                company_name = company_name.replace("Symbol Lookup", "").strip()

                if not company_name: # 가끔 이름이 비는 경우 발생
                    company_name = symbol_match # 이름 없으면 심볼로 대체

                logger.debug(f"Processing Ticker: {symbol_match}, Name: {company_name}")
                trending_tickers_data.append({
                    "title": company_name,
                    "content": symbol_match,
                    "source": "Yahoo Finance Trending",
                    "published": collection_time,
                    "url": f"https://finance.yahoo.com{href}" # 상세 URL 추가
                })
                processed_symbols.add(symbol_match)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Yahoo Finance trending tickers: {e}")
    except Exception as e:
        logger.error(f"Error parsing Yahoo Finance trending tickers: {e}")

    logger.info(f"Successfully fetched {len(trending_tickers_data)} trending tickers.")
    return trending_tickers_data

# --- FunctionTool 인스턴스 생성 ---
fetch_trending_tickers = FunctionTool(func=fetch_trending_tickers_func)

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요
# TODO: 스크래핑 안정성 강화 (선택자 변경 대응, 재시도 로직 등) 