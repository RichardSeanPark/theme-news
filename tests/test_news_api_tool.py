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

# --- 테스트 케이스 --- 

# 2.2.1: fetch_newsapi_headlines 성공 테스트 (Live API)
def test_fetch_newsapi_headlines_success(monkeypatch):
    """fetch_newsapi_headlines 실제 API 호출 테스트"""
    # 유효한 API 키가 .env 또는 환경 변수에 설정되어 있어야 통과 가능
    # monkeypatch.setenv("NEWS_API_KEY", "YOUR_REAL_OR_VALID_TEST_KEY") # 필요시 설정
    api_key = news_api_tool.os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "dummy_newsapi_key":
        pytest.skip("NEWS_API_KEY not set or is dummy key, skipping live API test")

    # 함수 실행
    articles = news_api_tool.fetch_newsapi_headlines.func(country='kr')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)

# 2.2.2: fetch_nytimes_articles 성공 테스트 (Live API)
def test_fetch_nytimes_articles_success(monkeypatch):
    """fetch_nytimes_articles 실제 API 호출 테스트"""
    # 유효한 API 키가 .env 또는 환경 변수에 설정되어 있어야 통과 가능
    # monkeypatch.setenv("NYT_API_KEY", "YOUR_REAL_OR_VALID_TEST_KEY") # 필요시 설정
    api_key = news_api_tool.os.getenv("NYT_API_KEY")
    if not api_key or api_key == "dummy_nyt_key":
        pytest.skip("NYT_API_KEY not set or is dummy key, skipping live API test")

    # 함수 실행
    articles = news_api_tool.fetch_nytimes_articles.func(query='korea')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)

# 2.2.3: fetch_naver_news 성공 테스트 (Live API)
def test_fetch_naver_news_success(monkeypatch):
    """fetch_naver_news 실제 API 호출 테스트"""
    # 유효한 API 키가 .env 또는 환경 변수에 설정되어 있어야 통과 가능
    # monkeypatch.setenv("NAVER_CLIENT_ID", "YOUR_REAL_ID") # 필요시 설정
    # monkeypatch.setenv("NAVER_CLIENT_SECRET", "YOUR_REAL_SECRET") # 필요시 설정
    client_id = news_api_tool.os.getenv("NAVER_CLIENT_ID")
    client_secret = news_api_tool.os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or client_id == "dummy_naver_id" or \
       not client_secret or client_secret == "dummy_naver_secret":
        pytest.skip("Naver API keys not set or are dummy keys, skipping live API test")

    # 함수 실행
    articles = news_api_tool.fetch_naver_news.func(query='테스트')

    # 검증 (예외 없이 list 타입 반환 확인)
    assert isinstance(articles, list)
    # (선택적) HTML 태그 제거 확인 (결과가 있을 경우)
    if articles:
        assert '<b>' not in articles[0].get('title', '')
        assert '&quot;' not in articles[0].get('title', '')
        assert '<b>' not in articles[0].get('content', '')

# 2.2.4: API 키 누락 시 오류 처리 테스트 (변경 없음)
@pytest.mark.parametrize(
    "api_tool_instance, env_keys_to_remove",
    [
        (news_api_tool.fetch_newsapi_headlines, ["NEWS_API_KEY"]),
        (news_api_tool.fetch_nytimes_articles, ["NYT_API_KEY"]),
        (news_api_tool.fetch_naver_news, ["NAVER_CLIENT_ID", "NAVER_CLIENT_SECRET"])
    ]
)
def test_news_api_key_missing(monkeypatch, capsys, api_tool_instance, env_keys_to_remove):
    """각 API 함수가 키 누락 시 빈 리스트 반환 및 오류 출력하는지 테스트"""
    # 미리 다른 키들은 설정 (테스트 대상 키만 없는 상태 만들기)
    # 이 부분은 reset_env_vars fixture에서 처리하므로 중복 제거 가능
    # if "NEWS_API_KEY" not in env_keys_to_remove: monkeypatch.setenv("NEWS_API_KEY", "dummy")
    # ...

    # 테스트 대상 키 제거
    for key in env_keys_to_remove:
        monkeypatch.delenv(key, raising=False)

    if api_tool_instance.func.__name__ == "fetch_newsapi_headlines_func":
        result = api_tool_instance.func()
    else:
        # Naver API는 query 인수가 필수임
        query_arg = {'query': 'test'} if 'naver' in api_tool_instance.func.__name__ else {}
        result = api_tool_instance.func(**query_arg)

    assert result == []
    captured = capsys.readouterr()
    key_name_in_message = env_keys_to_remove[0]
    expected_message_part = "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET" if "NAVER" in key_name_in_message else key_name_in_message
    assert f"{expected_message_part} 환경 변수가 설정되지 않았습니다." in captured.out

# 2.2.5: API 호출 실패 시 오류 처리 테스트 (모킹 사용)
@pytest.mark.parametrize(
    "api_tool_instance, keys_to_set",
    [
        (news_api_tool.fetch_newsapi_headlines, {"NEWS_API_KEY": "dummy_key"}),
        (news_api_tool.fetch_nytimes_articles, {"NYT_API_KEY": "dummy_key"}),
        (news_api_tool.fetch_naver_news, {"NAVER_CLIENT_ID": "dummy_id", "NAVER_CLIENT_SECRET": "dummy_secret"})
    ]
)
def test_news_api_call_failure(mock_requests_get, monkeypatch, capsys, api_tool_instance, keys_to_set):
    """각 API 함수가 호출 실패 시 빈 리스트 반환 및 오류 출력하는지 테스트"""
    # 키 검사를 통과하도록 임시 키 설정
    for key, value in keys_to_set.items():
        monkeypatch.setenv(key, value)

    # requests.get 호출 시 RequestException 발생하도록 모킹
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")

    if api_tool_instance.func.__name__ == "fetch_newsapi_headlines_func":
        result = api_tool_instance.func()
    else:
        # Naver API는 query 인수가 필수임
        query_arg = {'query': 'test'} if 'naver' in api_tool_instance.func.__name__ else {}
        result = api_tool_instance.func(**query_arg)

    assert result == []
    captured = capsys.readouterr()
    assert "호출 오류" in captured.out # 표준 출력에 "호출 오류" 메시지 확인 