import time
import logging
import validators
from newspaper import Article, ArticleException
from google.adk.tools import FunctionTool
import requests # requests 예외 처리 추가
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from typing import List, Dict, Any # typing 추가
# robots.txt 파싱을 위한 임포트 (선택적 구현 시)
# from urllib.parse import urlparse
# from urllib.robotparser import RobotFileParser

# Logging 설정
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO) # 주석 처리: 메인 에이전트나 외부에서 설정하도록 함
# 애플리케이션 레벨에서 한 번만 설정하는 것이 좋음

# --- 함수 정의 ---

DEFAULT_TIMEOUT = 10 # 초 단위
DEFAULT_WAIT_TIME = 1 # 초 단위, 요청 간 대기 시간

def _fetch_full_content_func(url: str) -> str | None: # 함수 이름 변경 (_ 추가)
    """
    주어진 URL에서 웹 페이지의 전체 내용을 추출합니다. (newspaper3k 사용)

    Args:
        url: 내용을 추출할 웹 페이지의 URL.

    Returns:
        추출된 기사 내용 (문자열) 또는 실패 시 None.
    """
    logger.info(f"Attempting to fetch static content from: {url}")

    if not isinstance(url, str) or not validators.url(url):
        logger.error(f"Invalid URL format or type provided: {url} (type: {type(url)})")
        return None

    try:
        article = Article(url, request_timeout=DEFAULT_TIMEOUT, follow_meta_refresh=True)
        article.download()
        article.parse()

        if not article.text:
            logger.warning(f"Could not extract main text content from URL: {url}")
            return None
        else:
            extracted_text = article.text
            logger.info(f"Successfully extracted static content from URL: {url} (length: {len(extracted_text)})")
            time.sleep(DEFAULT_WAIT_TIME)
            return extracted_text

    except ArticleException as e:
        logger.error(f"Newspaper3k error processing URL {url}: {e}")
        return None
    except requests.exceptions.RequestException as e: # requests 예외 처리 추가
        logger.error(f"Network error (requests) processing URL {url}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error processing URL {url}: {e}") # 스택 트레이스 포함
        return None

def _fetch_dynamic_content_func(url: str) -> str | None: # 함수 이름 변경 (_ 추가)
    """
    주어진 URL에서 JavaScript 렌더링 후의 웹 페이지 내용을 추출합니다. (Playwright 사용)

    Args:
        url: 내용을 추출할 웹 페이지의 URL.

    Returns:
        추출된 페이지 내용 (body 태그의 inner_text) 또는 실패 시 None.
    """
    logger.info(f"Attempting to fetch dynamic content from: {url}")

    if not isinstance(url, str) or not validators.url(url):
        logger.error(f"Invalid URL format or type provided: {url} (type: {type(url)})")
        return None

    content = None
    browser = None
    browser_closed_in_try = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) # headless 모드 사용
            page = browser.new_page()
            page.goto(url, timeout=DEFAULT_TIMEOUT * 1000 * 2)
            page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT * 1000)
            content = page.inner_text('body')
            browser.close()
            browser_closed_in_try = True

            if not content:
                logger.warning(f"Could not extract dynamic text content from URL: {url}")
                return None
            else:
                logger.info(f"Successfully extracted dynamic content from URL: {url} (length: {len(content)})")
                time.sleep(DEFAULT_WAIT_TIME)
                return content.strip()

    except PlaywrightTimeoutError as e:
        logger.error(f"Playwright timeout error processing URL {url}: {e}")
        return None
    except PlaywrightError as e:
        logger.error(f"Playwright error processing URL {url}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error processing URL {url} with Playwright: {e}")
        return None
    finally:
        if browser and not browser_closed_in_try and browser.is_connected():
            try:
                browser.close()
                logger.debug(f"Playwright browser explicitly closed for {url}")
            except Exception as e:
                logger.error(f"Error closing Playwright browser for {url}: {e}")

# --- WebCrawlingTool 클래스 정의 ---
class WebCrawlingTool:
    """
    웹 페이지 콘텐츠 추출 (정적/동적) 함수들을
    FunctionTool로 감싸 제공하는 클래스입니다.
    """
    def __init__(self):
        self.fetch_full_content = FunctionTool(func=_fetch_full_content_func)
        self.fetch_dynamic_content = FunctionTool(func=_fetch_dynamic_content_func)

# --- 기존 FunctionTool 인스턴스 생성 코드 제거 ---
# fetch_full_content = FunctionTool(func=fetch_full_content_func)
# fetch_dynamic_content = FunctionTool(func=fetch_dynamic_content_func)

# 아래 if __name__ == '__main__': 블록은 테스트용이므로 유지하거나 삭제 가능
if __name__ == '__main__':
    # 로깅 설정 (테스트 실행 시)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    test_urls = [
        "https://www.bbc.com/news/world-us-canada-57140431", # 예시 BBC 뉴스
        "https://httpbin.org/delay/5", # 5초 지연
        "https://invalid-url-that-does-not-exist-ksdjfhsdkjfhs.com", # 존재하지 않는 URL
        "this is not a url", # 잘못된 형식
        "https://www.google.com", # Google 메인
        "https://github.com/codelucas/newspaper", # Github 페이지
        "https://pdf-example-link.com/example.pdf", # PDF 링크 (처리 어려울 수 있음)
        "https://www.chosun.com/economy/auto/2024/06/03/2B64FNRX7BCV7P3L6M4H4RZCUA/" # JavaScript 기반 사이트 예시 (동적 필요)
    ]

    print("\n--- Testing fetch_full_content (newspaper3k) ---")
    for test_url in test_urls:
        print(f"\nTesting URL: {test_url}")
        result = _fetch_full_content_func(test_url)
        if result:
            print(f"Successfully fetched (static): {len(result)} characters")
            # print(result[:200] + "...") # 내용 일부 출력
        else:
            print("Failed to fetch (static).")

    print("\n--- Testing fetch_dynamic_content (Playwright) ---")
    for test_url in test_urls:
        print(f"\nTesting URL: {test_url}")
        result = _fetch_dynamic_content_func(test_url)
        if result:
            print(f"Successfully fetched (dynamic): {len(result)} characters")
            # print(result[:200] + "...") # 내용 일부 출력
        else:
            print("Failed to fetch (dynamic).") 