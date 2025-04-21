import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from google.adk.tools import FunctionTool
import logging
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# Logging 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- 함수 정의 ---

def fetch_trending_tickers_func() -> list[dict]:
    """
    Yahoo Finance 웹사이트에서 'Trending Tickers' 정보를 스크래핑하여 반환합니다.
    (https://finance.yahoo.com/trending-tickers)
    Playwright를 사용하여 동적 콘텐츠 로딩 후 스크래핑합니다.

    Returns:
        인기 티커 정보 딕셔너리 리스트. 각 딕셔너리는 다음 키를 포함:
        - title (str): 회사명
        - content (str): 티커 심볼
        - source (str): "Yahoo Finance Trending"
        - published (str): 데이터 수집 시각 (ISO 8601 형식)
        - url (str): 티커 상세 페이지 URL
    """
    url = "https://finance.yahoo.com/trending-tickers"
    trending_tickers_data = []
    collection_time = datetime.now(timezone.utc).isoformat() # 수집 시각 기록

    try:
        logger.info(f"Launching playwright browser...")
        with sync_playwright() as p:
            browser = p.chromium.launch() # 기본 브라우저 사용
            page = browser.new_page()
            logger.info(f"Navigating to: {url}")
            page.goto(url, timeout=30000) # 타임아웃 30초

            # 특정 섹션이 로드될 때까지 기다림 (스크래핑 안정성 향상)
            logger.info("Waiting for trending tickers section...")
            page.wait_for_selector('section[data-testid="trending-tickers"]', timeout=20000)

            logger.info("Parsing HTML content retrieved by Playwright...")
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')

            # --- 기존 BeautifulSoup 파싱 로직 유지 ---
            section = soup.find('section', {'data-testid': 'trending-tickers'})
            if not section:
                logger.warning("Could not find the trending tickers section with data-testid after page load.")
                browser.close()
                return []

            ticker_links = section.find_all('a', href=lambda href: href and '/quote/' in href)
            if not ticker_links:
                logger.warning("Found trending tickers section, but no ticker links inside after page load.")
                browser.close()
                return []

            logger.info(f"Found {len(ticker_links)} potential ticker links.")
            processed_symbols = set()

            for link in ticker_links:
                href = link.get('href')
                symbol_match = href.split('/quote/')[-1].split('?')[0]
                if symbol_match and symbol_match not in processed_symbols:
                    company_name = link.get('aria-label', link.text.strip()).replace("Symbol Lookup", "").strip()
                    if not company_name:
                        company_name = symbol_match

                    logger.debug(f"Processing Ticker: {symbol_match}, Name: {company_name}")
                    trending_tickers_data.append({
                        "title": company_name,
                        "content": symbol_match,
                        "source": "Yahoo Finance Trending",
                        "published": collection_time,
                        "url": f"https://finance.yahoo.com{href}" # 상세 URL 추가
                    })
                    processed_symbols.add(symbol_match)
            # ---------------------------------------

            browser.close()
            logger.info("Browser closed.")

    except PlaywrightError as e:
        # Playwright 관련 오류 (네트워크, 타임아웃 등 포함)
        logger.error(f"Playwright error fetching Yahoo Finance trending tickers: {e}")
    except Exception as e:
        # 일반 파싱 오류 등
        logger.error(f"Error parsing Yahoo Finance trending tickers: {e}")
        # Playwright 실행 중 오류 발생 시 브라우저가 열려있을 수 있으므로 방어적으로 close 시도
        if 'browser' in locals() and browser.is_connected():
            try:
                browser.close()
                logger.info("Browser closed after catching exception.")
            except Exception as close_e:
                logger.error(f"Error closing browser after exception: {close_e}")

    logger.info(f"Successfully fetched {len(trending_tickers_data)} trending tickers.")
    return trending_tickers_data

# --- FunctionTool 인스턴스 생성 ---
fetch_trending_tickers = FunctionTool(func=fetch_trending_tickers_func)

# TODO: 향후 ArticleData Pydantic 모델 정의 후 반환 타입 및 파싱 로직 수정 필요
# TODO: 스크래핑 안정성 강화 (선택자 변경 대응, 재시도 로직 등)
# TODO: Playwright 브라우저 바이너리 필요 여부 명시 (README 등) 