import pytest
import requests
# 모킹 관련 임포트 추가
from unittest.mock import patch, MagicMock

# 테스트 대상 모듈 임포트
# conftest.py에서 sys.path 설정이 되어 있다고 가정
from theme_news_agent.sub_agents.data_collection.tools import news_api_tool

# --- Fixtures --- 
# mock_requests_get fixture 복원
@pytest.fixture
def mock_requests_get():
    """requests.get 함수를 모킹하는 fixture"""
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture(autouse=True)
def reset_env_vars(monkeypatch):
    """각 테스트 전에 환경 변수를 초기화 (None으로 설정)"""
    # 기본 더미 키 설정 (실제 테스트 시 .env 파일에 유효한 키 필요할 수 있음)
    monkeypatch.setenv("NEWS_API_KEY", "dummy_newsapi_key")
    monkeypatch.setenv("NYT_API_KEY", "dummy_nyt_key")
    monkeypatch.setenv("NAVER_CLIENT_ID", "dummy_naver_id")
    monkeypatch.setenv("NAVER_CLIENT_SECRET", "dummy_naver_secret")
    yield

# set_default_env_vars fixture는 reset_env_vars와 중복되므로 제거 가능
# @pytest.fixture(autouse=True)
# def set_default_env_vars(monkeypatch):
#     ...
#     yield

@pytest.fixture
def news_api_tool_instance():
    """Provides an instance of NewsApiTool for tests."""
    return news_api_tool.NewsApiTool()

# --- 테스트 케이스 --- 

# 2.2.1: fetch_newsapi_headlines 성공 테스트 (Live API)
def test_fetch_newsapi_headlines_success(monkeypatch, news_api_tool_instance):
    """fetch_newsapi_headlines 실제 API 호출 테스트"""
    api_key = news_api_tool.os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "dummy_newsapi_key":
        pytest.skip("NEWS_API_KEY not set or is dummy key, skipping live API test")

    # 함수 실행
    articles = news_api_tool_instance.fetch_newsapi_headlines.func(country='kr')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)

# 2.2.2: fetch_nytimes_articles 성공 테스트 (Live API)
def test_fetch_nytimes_articles_success(monkeypatch, news_api_tool_instance):
    """fetch_nytimes_articles 실제 API 호출 테스트"""
    api_key = news_api_tool.os.getenv("NYT_API_KEY")
    if not api_key or api_key == "dummy_nyt_key":
        pytest.skip("NYT_API_KEY not set or is dummy key, skipping live API test")

    # 함수 실행
    articles = news_api_tool_instance.fetch_nytimes_articles.func(query='korea')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)

# 2.2.3: fetch_naver_news 성공 테스트 (Live API)
def test_fetch_naver_news_success(monkeypatch, news_api_tool_instance):
    """fetch_naver_news 실제 API 호출 테스트"""
    client_id = news_api_tool.os.getenv("NAVER_CLIENT_ID")
    client_secret = news_api_tool.os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or client_id == "dummy_naver_id" or \
       not client_secret or client_secret == "dummy_naver_secret":
        pytest.skip("Naver API keys not set or are dummy keys, skipping live API test")

    # 함수 실행
    articles = news_api_tool_instance.fetch_naver_news.func(query='테스트')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)
    # (선택적) HTML 태그 제거 확인 (결과가 있을 경우)
    if articles:
        assert '<b>' not in articles[0].get('title', '')
        assert '&quot;' not in articles[0].get('title', '')
        assert '<b>' not in articles[0].get('content', '')

# 2.2.4: API 키 누락 시 오류 처리 테스트
# Parametrize approach needs significant change due to class structure.
# Let's test each function separately for key missing scenario.

def test_newsapi_key_missing(monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_newsapi_headlines when NEWS_API_KEY is missing."""
    monkeypatch.delenv("NEWS_API_KEY", raising=False)
    result = news_api_tool_instance.fetch_newsapi_headlines.func()
    assert result == []
    captured = capsys.readouterr()
    assert "NEWS_API_KEY 환경 변수가 설정되지 않았습니다." in captured.out

def test_nytimes_key_missing(monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_nytimes_articles when NYT_API_KEY is missing."""
    monkeypatch.delenv("NYT_API_KEY", raising=False)
    result = news_api_tool_instance.fetch_nytimes_articles.func() # query default exists
    assert result == []
    captured = capsys.readouterr()
    assert "NYT_API_KEY 환경 변수가 설정되지 않았습니다." in captured.out

def test_naver_keys_missing(monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_naver_news when Naver keys are missing."""
    monkeypatch.delenv("NAVER_CLIENT_ID", raising=False)
    monkeypatch.delenv("NAVER_CLIENT_SECRET", raising=False)
    result = news_api_tool_instance.fetch_naver_news.func(query='test') # query is required
    assert result == []
    captured = capsys.readouterr()
    assert "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경 변수가 설정되지 않았습니다." in captured.out

# 2.2.5: API 호출 실패 시 오류 처리 테스트 (모킹 사용)
# Similar refactoring: test each function separately for call failure.

def test_newsapi_call_failure(mock_requests_get, monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_newsapi_headlines call failure handling."""
    monkeypatch.setenv("NEWS_API_KEY", "dummy_key") # Ensure key check passes
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result = news_api_tool_instance.fetch_newsapi_headlines.func()
    assert result == []
    captured = capsys.readouterr()
    assert "NewsAPI 호출 오류" in captured.out

def test_nytimes_call_failure(mock_requests_get, monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_nytimes_articles call failure handling."""
    monkeypatch.setenv("NYT_API_KEY", "dummy_key")
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result = news_api_tool_instance.fetch_nytimes_articles.func()
    assert result == []
    captured = capsys.readouterr()
    assert "NYTimes API 호출 오류" in captured.out

def test_naver_call_failure(mock_requests_get, monkeypatch, capsys, news_api_tool_instance):
    """Tests fetch_naver_news call failure handling."""
    monkeypatch.setenv("NAVER_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("NAVER_CLIENT_SECRET", "dummy_secret")
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result = news_api_tool_instance.fetch_naver_news.func(query='test')
    assert result == []
    captured = capsys.readouterr()
    assert "Naver News API 호출 오류" in captured.out

# Remove the old parametrize decorators and functions
# @pytest.mark.parametrize(...)
# def test_news_api_key_missing(...): ...
# @pytest.mark.parametrize(...)
# def test_news_api_call_failure(...): ... 