import pytest
# requests 는 더 이상 직접 사용하지 않음
# import requests
from unittest.mock import patch, MagicMock
import logging
from playwright.sync_api import Error as PlaywrightError # Playwright 에러 임포트

# 테스트 대상 모듈 임포트
from theme_news_agent.sub_agents.data_collection.tools import financial_trend_tool

# --- Fixtures ---

# mock_requests_get fixture는 더 이상 필요 없음
# @pytest.fixture
# def mock_requests_get():
#     ...

# --- 테스트 케이스 ---

# 2.4.1: fetch_trending_tickers 성공 테스트 (Live Web with Playwright)
@pytest.mark.slow # Playwright는 브라우저 실행으로 인해 느릴 수 있음
def test_fetch_trending_tickers_success(caplog):
    """fetch_trending_tickers 실제 웹 스크래핑 테스트 (Playwright 사용)
    주의: 이 테스트는 playwright 브라우저 바이너리가 설치되어 있어야 실행 가능합니다.
    (poetry run playwright install 또는 playwright install)
    """
    caplog.set_level(logging.INFO)

    # 네트워크 연결 상태 및 웹사이트 구조에 따라 결과가 달라질 수 있음
    try:
        tickers = financial_trend_tool.fetch_trending_tickers.func()

        assert isinstance(tickers, list)

        # 성공 로그 확인 (Playwright 관련 로그 추가)
        assert "Launching playwright browser..." in caplog.text
        assert "Navigating to:" in caplog.text
        assert "Waiting for trending tickers section..." in caplog.text
        assert "Parsing HTML content retrieved by Playwright..." in caplog.text
        assert "Browser closed." in caplog.text
        print(f"Fetched {len(tickers)} trending tickers.")

        if tickers:
            assert 'title' in tickers[0]
            assert 'content' in tickers[0]
            assert tickers[0]['source'] == "Yahoo Finance Trending"
            assert 'published' in tickers[0]
            assert 'url' in tickers[0]
            assert isinstance(tickers[0]['title'], str)
            assert isinstance(tickers[0]['content'], str)
            assert len(tickers[0]['content']) > 0

    except PlaywrightError as e:
        # Playwright 실행 관련 오류 (예: 바이너리 누락)
        pytest.fail(f"Playwright setup error: {e}. Did you run 'playwright install'?")
    except Exception as e:
        # 네트워크 오류 등 다른 예외는 스킵 처리 가능성 고려 (CI 환경 등)
        if "net::ERR_CONNECTION_REFUSED" in str(e) or "Timeout" in str(e):
             pytest.skip(f"Network/Timeout error during live web test: {e}")
        else:
            pytest.fail(f"Test failed unexpectedly during live web call: {e}")

# 2.4.2: 스크래핑 실패 시 오류 처리 테스트 (모킹 사용)
@patch('theme_news_agent.sub_agents.data_collection.tools.financial_trend_tool.BeautifulSoup') # BeautifulSoup 자체를 모킹
@patch('theme_news_agent.sub_agents.data_collection.tools.financial_trend_tool.sync_playwright') # Playwright도 모킹하여 실제 브라우저 실행 방지
def test_fetch_trending_tickers_scraping_failure_no_section(mock_playwright, mock_bs, caplog):
    """스크래핑 시 section을 찾지 못하는 경우 빈 리스트 반환 및 로그 확인"""
    caplog.set_level(logging.WARNING)

    # Playwright 관련 객체 모킹 설정 (실제 실행 방지)
    mock_context_manager = MagicMock()
    mock_playwright.return_value = mock_context_manager
    mock_p = MagicMock()
    mock_context_manager.__enter__.return_value = mock_p
    mock_browser = MagicMock()
    mock_p.chromium.launch.return_value = mock_browser
    mock_page = MagicMock()
    mock_browser.new_page.return_value = mock_page
    mock_page.content.return_value = "<html></html>" # 빈 HTML 반환 가정

    # BeautifulSoup 모킹 설정
    mock_soup_instance = MagicMock()
    mock_bs.return_value = mock_soup_instance
    # find 메서드가 section[data-testid="trending-tickers"] 를 찾을 때 None 반환하도록 설정
    mock_soup_instance.find.return_value = None

    tickers = financial_trend_tool.fetch_trending_tickers.func()

    assert tickers == []
    assert "Could not find the trending tickers section" in caplog.text
    # Playwright 관련 호출 확인 (goto, wait_for_selector 등)
    mock_page.goto.assert_called_once()
    mock_page.wait_for_selector.assert_called_once()
    mock_page.content.assert_called_once()
    # BeautifulSoup find 호출 확인
    mock_soup_instance.find.assert_called_once_with('section', {'data-testid': 'trending-tickers'})
    # find_all은 호출되지 않아야 함
    mock_soup_instance.find_all.assert_not_called()
    # 브라우저 종료 확인
    mock_browser.close.assert_called_once()

@patch('theme_news_agent.sub_agents.data_collection.tools.financial_trend_tool.BeautifulSoup')
@patch('theme_news_agent.sub_agents.data_collection.tools.financial_trend_tool.sync_playwright')
def test_fetch_trending_tickers_scraping_failure_no_links(mock_playwright, mock_bs, caplog):
    """스크래핑 시 section은 찾지만 link를 찾지 못하는 경우 빈 리스트 반환 및 로그 확인"""
    caplog.set_level(logging.WARNING)

    # Playwright 모킹 (위와 동일)
    mock_context_manager = MagicMock()
    mock_playwright.return_value = mock_context_manager
    mock_p = MagicMock()
    mock_context_manager.__enter__.return_value = mock_p
    mock_browser = MagicMock()
    mock_p.chromium.launch.return_value = mock_browser
    mock_page = MagicMock()
    mock_browser.new_page.return_value = mock_page
    mock_page.content.return_value = "<html><section data-testid='trending-tickers'></section></html>"

    # BeautifulSoup 모킹 설정
    mock_soup_instance = MagicMock()
    mock_bs.return_value = mock_soup_instance
    mock_section = MagicMock() # section 객체 모킹
    mock_soup_instance.find.return_value = mock_section
    # section 객체 내 find_all 메서드가 빈 리스트 반환하도록 설정
    mock_section.find_all.return_value = []

    tickers = financial_trend_tool.fetch_trending_tickers.func()

    assert tickers == []
    assert "Found trending tickers section, but no ticker links inside" in caplog.text
    mock_soup_instance.find.assert_called_once_with('section', {'data-testid': 'trending-tickers'})
    mock_section.find_all.assert_called_once()
    mock_browser.close.assert_called_once()

# 2.4.3: 네트워크 오류 시 처리 테스트 (Playwright 모킹)
@patch('playwright.sync_api._generated.Page.goto') # page.goto 메서드를 모킹
def test_fetch_trending_tickers_network_error(mock_goto, caplog):
    """Playwright 네트워크 오류 발생 시 빈 리스트 반환 및 로그 확인"""
    caplog.set_level(logging.ERROR)

    # page.goto 호출 시 PlaywrightError 발생하도록 설정
    mock_goto.side_effect = PlaywrightError("Test network error simulation")

    tickers = financial_trend_tool.fetch_trending_tickers.func()

    assert tickers == []
    # 에러 로그 메시지 확인 (Playwright 에러 메시지 확인)
    assert "Playwright error fetching Yahoo Finance trending tickers: Test network error simulation" in caplog.text 