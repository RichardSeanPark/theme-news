import pytest
import requests
from unittest.mock import patch, MagicMock # 모킹을 위해 추가

# 테스트 대상 모듈 임포트
from theme_news_agent.sub_agents.data_collection.tools import blog_cafe_api_tool

# --- Fixtures ---

@pytest.fixture
def mock_requests_get():
    """requests.get 함수를 모킹하는 fixture"""
    with patch('requests.get') as mock_get:
        yield mock_get

# --- 테스트 케이스 --- 

# 2.3.1: fetch_naver_blogs 성공 테스트 (Live API)
def test_fetch_naver_blogs_success():
    """fetch_naver_blogs 실제 API 호출 테스트 (환경 변수 사용)"""
    articles = blog_cafe_api_tool.fetch_naver_blogs.func(query='테스트')

    assert isinstance(articles, list)

# 2.3.2: fetch_naver_cafe_articles 성공 테스트 (Live API)
def test_fetch_naver_cafe_articles_success():
    """fetch_naver_cafe_articles 실제 API 호출 테스트 (환경 변수 사용)"""
    articles = blog_cafe_api_tool.fetch_naver_cafe_articles.func(query='테스트')

    assert isinstance(articles, list)

# 2.3.3: API 키 누락 시 오류 처리 테스트
@pytest.mark.parametrize(
    "keys_to_remove",
    [["NAVER_CLIENT_ID"], ["NAVER_CLIENT_SECRET"]]
)
def test_blog_cafe_api_key_missing(monkeypatch, capsys, keys_to_remove):
    """Naver 키 누락 시 빈 리스트 반환 및 오류 출력 테스트"""
    initial_values = {}
    for key in keys_to_remove:
        initial_values[key] = blog_cafe_api_tool.os.getenv(key)
        monkeypatch.delenv(key, raising=False)

    try:
        # 블로그 테스트
        result_blog = blog_cafe_api_tool.fetch_naver_blogs.func(query='test')
        assert result_blog == []
        captured_blog = capsys.readouterr() # 이전 출력 초기화
        assert "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET" in captured_blog.out
        assert "(blog)" in captured_blog.out # API 타입 명시 확인

        # 카페 테스트
        result_cafe = blog_cafe_api_tool.fetch_naver_cafe_articles.func(query='test')
        assert result_cafe == []
        captured_cafe = capsys.readouterr()
        assert "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET" in captured_cafe.out
        assert "(cafearticle)" in captured_cafe.out # API 타입 명시 확인
    finally:
        # 테스트 후 원래 환경 변수 값 복원 (다른 테스트 영향 방지)
        for key, value in initial_values.items():
            if value is not None:
                monkeypatch.setenv(key, value)
            else:
                # 원래 없던 변수면 다시 제거
                monkeypatch.delenv(key, raising=False)

# 2.3.4: API 호출 실패 시 오류 처리 테스트 (모킹 사용)
def test_blog_cafe_api_call_failure(mock_requests_get, monkeypatch, capsys):
    """Naver API 호출 실패 시 빈 리스트 반환 및 오류 출력 테스트"""
    # 실제 키가 있어도 모킹으로 실패를 시뮬레이션하므로 monkeypatch 필요

    # requests.get 호출 시 RequestException 발생하도록 모킹
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")

    # 블로그 테스트
    result_blog = blog_cafe_api_tool.fetch_naver_blogs.func(query='test')
    assert result_blog == []
    captured_blog = capsys.readouterr() # 이전 출력 초기화
    assert "Naver Blog API 호출 오류" in captured_blog.out

    # 카페 테스트
    # 모킹 객체 재사용 위해 side_effect 다시 설정 (동일 예외)
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result_cafe = blog_cafe_api_tool.fetch_naver_cafe_articles.func(query='test')
    assert result_cafe == []
    captured_cafe = capsys.readouterr()
    assert "Naver Cafearticle API 호출 오류" in captured_cafe.out 