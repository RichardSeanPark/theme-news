import time
import logging
import validators
from newspaper import Article, ArticleException
from google.adk.tools import FunctionTool
import requests # requests 예외 처리 추가
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
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

def fetch_full_content_func(url: str) -> str | None:
    """
    주어진 URL에서 웹 페이지의 전체 내용을 추출합니다. (newspaper3k 사용)

    Args:
        url: 내용을 추출할 웹 페이지의 URL.

    Returns:
        추출된 기사 내용 (문자열) 또는 실패 시 None.
    """
    # logger.debug(f\"DEBUG: Entering fetch_full_content_func for URL: {url}\") # INFO 레벨로 변경
    logger.info(f"Attempting to fetch static content from: {url}")


    # robots.txt 확인 (선택적)
    # try:
    #     parsed_url = urlparse(url)
    #     robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    #     rp = RobotFileParser()
    #     rp.set_url(robots_url)
    #     rp.read()
    #     if not rp.can_fetch("*", url):
    #         logger.warning(f"Crawling disallowed by robots.txt for URL: {url}")
    #         return None
    # except Exception as e:
    #     logger.warning(f"Could not parse or check robots.txt for {url}: {e}")
    #     # robots.txt 확인 실패 시 일단 진행 (정책에 따라 결정)

    if not isinstance(url, str) or not validators.url(url):
        # logger.error(f\"Invalid URL provided: {url}\")
        # 변경: 상세 오류 로깅
        logger.error(f"Invalid URL format or type provided: {url} (type: {type(url)})")
        # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with None due to invalid URL.\")
        return None

    try:
        # logger.debug(f\"DEBUG: Attempting to create Article object for URL: {url}\")
        # newspaper3k 설정 추가 (타임아웃 등)
        article = Article(url, request_timeout=DEFAULT_TIMEOUT, follow_meta_refresh=True)
        # article = Article(url)
        # logger.debug(f\"DEBUG: Article object created for URL: {url}\")

        # 기사 다운로드 및 파싱
        # logger.debug(f\"DEBUG: Attempting article.download() for URL: {url}\")
        article.download()
        # logger.debug(f\"DEBUG: article.download() completed for URL: {url}\")

        # logger.debug(f\"DEBUG: Attempting article.parse() for URL: {url}\")
        article.parse()
        # logger.debug(f\"DEBUG: article.parse() completed for URL: {url}\")

        # 추출된 내용 반환
        # logger.debug(f\"DEBUG: Checking extracted article.text for URL: {url}\")
        if not article.text:
            logger.warning(f"Could not extract main text content from URL: {url}")
            # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with None because article.text is empty.\")
            return None
        else:
            extracted_text = article.text
            logger.info(f"Successfully extracted static content from URL: {url} (length: {len(extracted_text)})")
            # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with extracted content.\")
            # return article.text
            # 변경: 길이 제한 등의 후처리 가능성 고려하여 변수 사용
            # 요청 간 지연 추가
            time.sleep(DEFAULT_WAIT_TIME)
            return extracted_text

    except ArticleException as e:
        # logger.error(f\"Newspaper3k ArticleException processing URL {url}: {e}\")
        # 변경: 상세 오류 로깅
        logger.error(f"Newspaper3k error processing URL {url}: {e}")
        # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with None due to ArticleException.\")
        return None
    except requests.exceptions.RequestException as e: # requests 예외 처리 추가
        logger.error(f"Network error (requests) processing URL {url}: {e}")
        # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with None due to requests.exceptions.RequestException.\")
        return None
    except Exception as e:
        # logger.error(f\"Unexpected error fetching content from {url}: {e}\", exc_info=True)
        # 변경: 스택 트레이스 포함 로깅
        logger.exception(f"Unexpected error processing URL {url}: {e}") # 스택 트레이스 포함
        # logger.debug(f\"DEBUG: Exiting fetch_full_content_func with None due to unexpected exception.\")
        return None

# TODO: Playwright를 사용한 동적 콘텐츠 처리 함수 구현 (fetch_dynamic_content)
def fetch_dynamic_content_func(url: str) -> str | None:
    """
    주어진 URL에서 JavaScript 렌더링 후의 웹 페이지 내용을 추출합니다. (Playwright 사용)

    Args:
        url: 내용을 추출할 웹 페이지의 URL.

    Returns:
        추출된 페이지 내용 (body 태그의 inner_text) 또는 실패 시 None.
    """
    logger.info(f"Attempting to fetch dynamic content from: {url}")

    # robots.txt 확인 (선택적) - 위와 동일 로직 적용 가능

    if not isinstance(url, str) or not validators.url(url):
        logger.error(f"Invalid URL format or type provided: {url} (type: {type(url)})")
        return None

    content = None
    browser = None # finally에서 사용하기 위해 초기화
    browser_closed_in_try = False # try 블록 내에서 닫혔는지 확인하는 플래그
    try:
        with sync_playwright() as p:
            # try: # Chromium 브라우저 설치 확인 (필요시)
            #     p.chromium.install()
            # except Exception as e:
            #      logger.error(f"Failed to install playwright browser: {e}")
            #      # 필요시 에러 핸들링 또는 사용자에게 안내

            browser = p.chromium.launch()
            page = browser.new_page()
            # 페이지 로드 타임아웃 설정 (기본 30초)
            page.goto(url, timeout=DEFAULT_TIMEOUT * 1000 * 2) # newspaper보다 길게 설정
            # JavaScript 실행을 기다리는 시간 (필요에 따라 조정)
            page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT * 1000)

            # 페이지 본문 내용 추출 (innerText 사용)
            content = page.inner_text('body')
            browser.close()
            browser_closed_in_try = True # 성공적으로 닫힘 플래그 설정

            if not content:
                logger.warning(f"Could not extract dynamic text content from URL: {url}")
                return None
            else:
                logger.info(f"Successfully extracted dynamic content from URL: {url} (length: {len(content)})")
                # 요청 간 지연 추가
                time.sleep(DEFAULT_WAIT_TIME)
                return content.strip() # 앞뒤 공백 제거

    except PlaywrightTimeoutError as e:
        logger.error(f"Playwright timeout error processing URL {url}: {e}")
        return None
    except PlaywrightError as e: # Playwright 관련 일반 오류
        logger.error(f"Playwright error processing URL {url}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error processing URL {url} with Playwright: {e}")
        return None
    finally:
        # 브라우저 객체가 성공적으로 생성되었으면 닫기
        if browser:
            try:
                # try 블록에서 닫히지 않았고, 여전히 연결 상태라면 닫기
                if not browser_closed_in_try and browser.is_connected():
                    browser.close()
                    logger.debug(f"Playwright browser explicitly closed for {url}")
                else:
                    logger.debug(f"Playwright browser already closed or closed in try block for {url}")
            except Exception as e:
                logger.error(f"Error closing Playwright browser for {url}: {e}")


# --- FunctionTool 인스턴스 생성 ---
fetch_full_content = FunctionTool(func=fetch_full_content_func)
fetch_dynamic_content = FunctionTool(func=fetch_dynamic_content_func)

# 예시 사용법 (테스트용)
if __name__ == '__main__':
    # 로깅 설정 (테스트 실행 시)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') # INFO로 변경

    test_urls = [
        "https://www.bbc.com/news/world-us-canada-57140431", # 예시 BBC 뉴스
        "https://httpbin.org/delay/5", # 5초 지연
        "https://invalid-url-that-does-not-exist-ksdjfhsdkjfhs.com", # 존재하지 않는 URL
        "this is not a url", # 잘못된 형식
        "https://www.google.com", # Google 메인
        "https://github.com/codelucas/newspaper", # Github 페이지
        "https://pdf-example-link.com/example.pdf", # PDF 링크 (처리 어려울 수 있음)
        # "https://www.chosun.com/economy/auto/2024/06/03/2B64FNRX7BCV7P3L6M4H4RZCUA/" # JavaScript 기반 사이트 예시 (동적 필요)
    ]

    print("\n--- Testing fetch_full_content (newspaper3k) ---")
    for url in test_urls:
        print(f"--- Testing URL: {url} ---")
        content = fetch_full_content.func(url)
        if content:
            print(f"Successfully fetched content (first 100 chars): {content[:100]}...")
        else:
            print("Failed to fetch content.")
        print("-" * 20)

    print("\n--- Testing fetch_dynamic_content (Playwright) ---")
    dynamic_test_urls = [
        "https://www.google.com/search?q=playwright", # Google 검색 결과 (JS 필요)
        "https://naver.com" # Naver 메인 (JS 필요)
    ]
    for url in dynamic_test_urls:
        print(f"--- Testing URL: {url} ---")
        content = fetch_dynamic_content.func(url)
        if content:
            print(f"Successfully fetched dynamic content (first 100 chars): {content[:100]}...")
        else:
            print("Failed to fetch dynamic content.")
        print("-" * 20) 