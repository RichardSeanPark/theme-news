import pytest
from pydantic import ValidationError
from datetime import datetime, timezone, timedelta
import logging

# 테스트 대상 모델 임포트
from theme_news_agent.sub_agents.data_collection.models import ArticleData, CollectedData

# --- ArticleData 테스트 --- #

def test_article_data_creation_success():
    """2.7.1: 정상 데이터로 ArticleData 생성 성공 테스트"""
    data = {
        "title": "Test Title",
        "content": "Test Content",
        "source": "Test Source",
        "published": "2024-01-01T12:00:00Z",
        "url": "https://example.com"
    }
    article = ArticleData(**data)
    assert article.title == "Test Title"
    assert article.content == "Test Content"
    assert article.source == "Test Source"
    assert isinstance(article.published, datetime)
    assert article.published == datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert str(article.url) == "https://example.com/"

def test_article_data_missing_required_fields():
    """2.7.2: ArticleData 필수 필드 누락 시 ValidationError 발생 테스트"""
    with pytest.raises(ValidationError, match='title'):
        ArticleData(source="Test Source")
    with pytest.raises(ValidationError, match='source'):
        ArticleData(title="Test Title")

def test_article_data_invalid_url():
    """2.7.3: ArticleData 잘못된 URL 형식 시 ValidationError 발생 테스트"""
    with pytest.raises(ValidationError, match='url'):
        ArticleData(title="T", source="S", url="htp://invalid")
    # None은 허용됨
    article = ArticleData(title="T", source="S", url=None)
    assert article.url is None

@pytest.mark.parametrize(
    "input_date, expected_datetime",
    [
        ("2024-01-01T12:00:00Z", datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)), # ISO 8601 Z
        ("2024-01-01T21:00:00+09:00", datetime(2024, 1, 1, 21, 0, 0, tzinfo=timezone(timedelta(seconds=32400)))), # ISO 8601 Offset
        (datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc), datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)), # Datetime object
        (None, None), # None value
    ]
)
def test_article_data_published_parsing_valid(input_date, expected_datetime):
    """2.7.4, 2.7.5, 2.7.6: ArticleData 유효한 published 날짜 파싱 테스트"""
    article = ArticleData(title="T", source="S", published=input_date)
    assert article.published == expected_datetime

@pytest.mark.parametrize(
    "invalid_date",
    [
        "invalid date string", # 잘못된 문자열
        "2024-13-01T12:00:00Z", # 잘못된 날짜 값
        1234567890, # 잘못된 타입 (int)
        [2024, 1, 1], # 잘못된 타입 (list)
    ]
)
def test_article_data_published_parsing_invalid(invalid_date, caplog):
    """2.7.7: ArticleData 잘못된 published 날짜 파싱 시 None 반환 및 경고 로그 테스트"""
    caplog.set_level(logging.WARNING)
    article = ArticleData(title="T", source="S", published=invalid_date)
    assert article.published is None
    assert "Could not parse date string" in caplog.text or "Unsupported type for published date" in caplog.text

# --- CollectedData 테스트 --- #

def test_collected_data_default_creation():
    """2.7.8: CollectedData 기본 인스턴스 생성 테스트"""
    collected_data = CollectedData()
    assert collected_data.newsapi_articles == []
    assert collected_data.nytimes_articles == []
    assert collected_data.naver_news == []
    assert collected_data.naver_blogs == []
    assert collected_data.naver_cafes == []
    assert collected_data.financial_trends == []
    assert collected_data.google_trends == []
    assert collected_data.naver_datalab_trends == []

def test_collected_data_add_data():
    """2.7.9: CollectedData 데이터 추가 및 확인 테스트"""
    article1 = ArticleData(title="News 1", source="NewsAPI")
    article2 = ArticleData(title="Blog 1", source="Naver Blog")
    collected_data = CollectedData(
        newsapi_articles=[article1],
        naver_blogs=[article2]
    )
    assert len(collected_data.newsapi_articles) == 1
    assert collected_data.newsapi_articles[0].title == "News 1"
    assert len(collected_data.naver_blogs) == 1
    assert collected_data.naver_blogs[0].title == "Blog 1"
    assert collected_data.nytimes_articles == [] # 다른 필드는 비어 있음

def test_collected_data_get_all_articles():
    """2.7.10: CollectedData get_all_articles 메서드 테스트"""
    article1 = ArticleData(title="News 1", source="NewsAPI")
    article2 = ArticleData(title="Blog 1", source="Naver Blog")
    article3 = ArticleData(title="Trend 1", source="Google Trends")
    collected_data = CollectedData(
        newsapi_articles=[article1],
        naver_blogs=[article2],
        google_trends=[article3]
    )
    all_articles = collected_data.get_all_articles()
    assert len(all_articles) == 3
    titles = {a.title for a in all_articles}
    assert titles == {"News 1", "Blog 1", "Trend 1"}

def test_collected_data_log_summary(caplog):
    """2.7.11: CollectedData log_summary 메서드 테스트"""
    caplog.set_level(logging.INFO)
    article1 = ArticleData(title="News 1", source="NewsAPI")
    article2 = ArticleData(title="Trend 1", source="Google Trends")
    collected_data = CollectedData(
        newsapi_articles=[article1],
        google_trends=[article2, article2] # 2개 추가
    )
    collected_data.log_summary()

    assert "Collected Data Summary:" in caplog.text
    assert "- NewsAPI: 1 articles" in caplog.text
    assert "- NYTimes: 0 articles" in caplog.text
    assert "- Naver News: 0 articles" in caplog.text
    assert "- Naver Blogs: 0 entries" in caplog.text
    assert "- Naver Cafes: 0 entries" in caplog.text
    assert "- Financial Trends: 0 tickers" in caplog.text
    assert "- Google Trends: 2 keywords" in caplog.text
    assert "- Naver DataLab: 0 keywords (Not Implemented)" in caplog.text
    assert "- Total Items: 3" in caplog.text 