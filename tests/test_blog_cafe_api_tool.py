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

@pytest.fixture
def blog_cafe_api_tool_instance():
    """Provides an instance of BlogCafeApiTool for tests."""
    return blog_cafe_api_tool.BlogCafeApiTool()

# --- 테스트 케이스 --- 

# 2.3.1: fetch_naver_blogs 성공 테스트 (Live API)
def test_fetch_naver_blogs_success(blog_cafe_api_tool_instance):
    """fetch_naver_blogs 실제 API 호출 테스트 (환경 변수 사용)"""
    articles = blog_cafe_api_tool_instance.fetch_naver_blogs.func(query='테스트')
    assert isinstance(articles, list)

# 2.3.2: fetch_naver_cafe_articles 성공 테스트 (Live API)
def test_fetch_naver_cafe_articles_success(blog_cafe_api_tool_instance):
    """fetch_naver_cafe_articles 실제 API 호출 테스트 (환경 변수 사용)"""
    articles = blog_cafe_api_tool_instance.fetch_naver_cafe_articles.func(query='테스트')
    assert isinstance(articles, list)

# 2.3.3: API 키 누락 시 오류 처리 테스트 - 분리된 테스트
def test_naver_blog_key_missing(monkeypatch, capsys, blog_cafe_api_tool_instance):
    """fetch_naver_blogs 키 누락 테스트"""
    monkeypatch.delenv("NAVER_CLIENT_ID", raising=False)
    monkeypatch.delenv("NAVER_CLIENT_SECRET", raising=False)
    result = blog_cafe_api_tool_instance.fetch_naver_blogs.func(query='test')
    assert result == []
    captured = capsys.readouterr()
    assert "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET" in captured.out
    assert "(blog)" in captured.out # API 타입 명시 확인

def test_naver_cafe_key_missing(monkeypatch, capsys, blog_cafe_api_tool_instance):
    """fetch_naver_cafe_articles 키 누락 테스트"""
    monkeypatch.delenv("NAVER_CLIENT_ID", raising=False)
    monkeypatch.delenv("NAVER_CLIENT_SECRET", raising=False)
    result = blog_cafe_api_tool_instance.fetch_naver_cafe_articles.func(query='test')
    assert result == []
    captured = capsys.readouterr()
    assert "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET" in captured.out
    assert "(cafearticle)" in captured.out # API 타입 명시 확인

# 2.3.4: API 호출 실패 시 오류 처리 테스트 (모킹 사용) - 분리된 테스트
def test_naver_blog_call_failure(mock_requests_get, monkeypatch, capsys, blog_cafe_api_tool_instance):
    """fetch_naver_blogs 호출 실패 테스트"""
    monkeypatch.setenv("NAVER_CLIENT_ID", "dummy_id") # 키 검사 통과용
    monkeypatch.setenv("NAVER_CLIENT_SECRET", "dummy_secret")
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result = blog_cafe_api_tool_instance.fetch_naver_blogs.func(query='test')
    assert result == []
    captured = capsys.readouterr()
    assert "Naver Blog API 호출 오류" in captured.out

def test_naver_cafe_call_failure(mock_requests_get, monkeypatch, capsys, blog_cafe_api_tool_instance):
    """fetch_naver_cafe_articles 호출 실패 테스트"""
    monkeypatch.setenv("NAVER_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("NAVER_CLIENT_SECRET", "dummy_secret")
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test connection error")
    result = blog_cafe_api_tool_instance.fetch_naver_cafe_articles.func(query='test')
    assert result == []
    captured = capsys.readouterr()
    assert "Naver Cafearticle API 호출 오류" in captured.out 