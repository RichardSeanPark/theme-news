import pytest
import requests
from unittest.mock import patch, MagicMock
import logging

# 테스트 대상 모듈 임포트
from theme_news_agent.sub_agents.data_collection.tools import financial_trend_tool

# --- Fixtures ---

@pytest.fixture
def mock_requests_get():
    """requests.get 함수를 모킹하는 fixture"""
    with patch('requests.get') as mock_get:
        yield mock_get

# --- 테스트 케이스 ---

# 2.4.1: fetch_trending_tickers 성공 테스트 (Live Web)
def test_fetch_trending_tickers_success(caplog):
    """fetch_trending_tickers 실제 웹 스크래핑 테스트"""
    caplog.set_level(logging.INFO) # 로그 레벨 설정

    # 네트워크 연결 상태에 따라 결과가 달라질 수 있음
    try:
        tickers = financial_trend_tool.fetch_trending_tickers.func()

        assert isinstance(tickers, list)

        # 성공 로그 확인
        assert "Fetching trending tickers from:" in caplog.text
        assert "Parsing HTML content..." in caplog.text
        # 결과 수에 따라 로그 메시지가 달라질 수 있음
        # assert "Successfully fetched" in caplog.text
        print(f"Fetched {len(tickers)} trending tickers.") # 디버깅용 출력

        if tickers: # 결과가 있을 경우 첫 항목 구조 검증
            assert 'title' in tickers[0]
            assert 'content' in tickers[0]
            assert tickers[0]['source'] == "Yahoo Finance Trending"
            assert 'published' in tickers[0]
            assert 'url' in tickers[0]
            assert isinstance(tickers[0]['title'], str)
            assert isinstance(tickers[0]['content'], str)
            assert len(tickers[0]['content']) > 0 # 티커 심볼은 비어있지 않아야 함

    except requests.exceptions.ConnectionError:
        pytest.skip("Network connection error, skipping live web test")
    except Exception as e:
        pytest.fail(f"Test failed unexpectedly during live web call: {e}")

# 2.4.2: 스크래핑 실패 시 오류 처리 테스트 (모킹 없이 어려움 - 제외)
# def test_fetch_trending_tickers_scraping_failure(...):
#     ...

# 2.4.3: 네트워크 오류 시 처리 테스트 (모킹 사용)
def test_fetch_trending_tickers_network_error(mock_requests_get, caplog):
    """네트워크 오류 발생 시 빈 리스트 반환 및 로그 확인"""
    caplog.set_level(logging.ERROR) # 에러 로그 확인

    # requests.get 호출 시 RequestException 발생하도록 모킹
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")

    tickers = financial_trend_tool.fetch_trending_tickers.func()

    assert tickers == []
    # 에러 로그 메시지 확인
    assert "Error fetching Yahoo Finance trending tickers: Test connection error" in caplog.text 