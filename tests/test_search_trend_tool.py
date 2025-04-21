import pytest
from unittest.mock import patch, MagicMock
import logging
import pandas as pd # 모킹된 반환값 확인용

# 테스트 대상 모듈 임포트
from theme_news_agent.sub_agents.data_collection.tools import search_trend_tool

# --- 테스트 케이스 ---

# 2.5.1: fetch_google_trends 성공 테스트 (Live API)
def test_fetch_google_trends_success(caplog):
    """fetch_google_trends 실제 API 호출 테스트"""
    caplog.set_level(logging.INFO)

    try:
        # 한국 지역 테스트
        trends_kr = search_trend_tool.fetch_google_trends.func(region='KR')
        assert isinstance(trends_kr, list)
        assert "Fetching Google Trends daily trending searches for region: KR" in caplog.text
        print(f"Fetched {len(trends_kr)} KR trends.")
        if trends_kr:
            assert 'title' in trends_kr[0]
            assert trends_kr[0]['content'] is None
            assert trends_kr[0]['source'] == "Google Trends KR"
            assert 'published' in trends_kr[0]
            assert 'url' in trends_kr[0]
            assert trends_kr[0]['url'].endswith("&geo=KR")

        # 미국 지역 테스트 (선택적 추가)
        # caplog.clear() # 이전 로그 지우기
        # trends_us = search_trend_tool.fetch_google_trends.func(region='US')
        # assert isinstance(trends_us, list)
        # assert "Fetching Google Trends daily trending searches for region: US" in caplog.text
        # print(f"Fetched {len(trends_us)} US trends.")
        # if trends_us:
        #     assert trends_us[0]['source'] == "Google Trends US"

    except Exception as e:
        # 네트워크 오류 등 pytrends 관련 예외 발생 시 스킵 또는 실패 처리
        if "Max retries exceeded" in str(e) or "Connection Error" in str(e):
             pytest.skip(f"Network error during live Google Trends test: {e}")
        else:
            pytest.fail(f"Test failed unexpectedly during live Google Trends call: {e}")

# 2.5.2: pytrends 라이브러리 오류 시 처리 테스트 (모킹 사용)
@patch('pytrends.request.TrendReq.trending_searches')
def test_fetch_google_trends_pytrends_error(mock_trending_searches, caplog):
    """pytrends.trending_searches 호출 시 예외 발생 처리 테스트"""
    caplog.set_level(logging.ERROR)

    # trending_searches 호출 시 Exception 발생하도록 모킹
    mock_trending_searches.side_effect = Exception("Simulated pytrends error")

    trends = search_trend_tool.fetch_google_trends.func(region='KR')

    assert trends == []
    assert "Error fetching Google Trends for region KR: Simulated pytrends error" in caplog.text

# 2.5.3: fetch_naver_datalab_trends 플레이스홀더 테스트
def test_fetch_naver_datalab_trends_placeholder(caplog):
    """fetch_naver_datalab_trends 호출 시 빈 리스트 및 경고 로그 확인"""
    caplog.set_level(logging.WARNING)

    trends = search_trend_tool.fetch_naver_datalab_trends.func()

    assert trends == []
    assert "fetch_naver_datalab_trends_func is not implemented yet." in caplog.text 