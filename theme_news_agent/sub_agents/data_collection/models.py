from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ArticleData(BaseModel):
    """다양한 소스에서 수집된 개별 데이터 항목(기사, 블로그 글, 검색어 등)을 표준화하기 위한 모델"""
    title: str = Field(..., description="항목의 제목 (예: 기사 제목, 블로그 제목, 검색어)")
    content: Optional[str] = Field(None, description="항목의 본문 내용 또는 요약 (가능한 경우)")
    source: str = Field(..., description="데이터 출처 (예: 'NewsAPI', 'NYTimes', 'Naver News', 'Naver Blog', 'Naver Cafe', 'Yahoo Finance Trending', 'Google Trends', 'Naver DataLab')")
    published: Optional[datetime] = Field(None, description="항목 발행 또는 수집 시각 (ISO 8601 형식 권장)")
    url: Optional[HttpUrl] = Field(None, description="항목의 원본 URL (가능한 경우)")

    @field_validator('published', mode='before')
    def parse_published_date(cls, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # 다양한 형식의 날짜 문자열 파싱 시도
                # 예: ISO 8601, RFC 1123 (웹 표준), 특정 API 형식 등
                # 여기서는 간단하게 ISO 8601만 처리 (필요시 확장)
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                logger.warning(f"Could not parse date string: {value}. Returning None.")
                return None
        logger.warning(f"Unsupported type for published date: {type(value)}. Returning None.")
        return None

    # content 필드 길이 로깅 (디버깅 목적)
    # @field_validator('content')
    # def log_content_length(cls, value):
    #     if value:
    #         logger.debug(f"ArticleData content length: {len(value)}")
    #     return value

class CollectedData(BaseModel):
    """DataCollectionAgent가 수집한 모든 데이터를 통합하여 담는 모델"""
    # 소스별 리스트 유지를 선택 (소스별 분석 용이)
    newsapi_articles: List[ArticleData] = Field(default_factory=list, description="NewsAPI에서 수집된 기사 목록")
    nytimes_articles: List[ArticleData] = Field(default_factory=list, description="NYTimes API에서 수집된 기사 목록")
    naver_news: List[ArticleData] = Field(default_factory=list, description="Naver News API에서 수집된 기사 목록")
    naver_blogs: List[ArticleData] = Field(default_factory=list, description="Naver Blog API에서 수집된 블로그 목록")
    naver_cafes: List[ArticleData] = Field(default_factory=list, description="Naver Cafe API에서 수집된 카페 글 목록")
    financial_trends: List[ArticleData] = Field(default_factory=list, description="Yahoo Finance 등에서 수집된 금융 트렌드 목록")
    google_trends: List[ArticleData] = Field(default_factory=list, description="Google Trends에서 수집된 검색어 목록")
    naver_datalab_trends: List[ArticleData] = Field(default_factory=list, description="Naver DataLab에서 수집된 검색어 목록 (미구현)")
    # 기타 다른 소스 추가 가능

    # 모든 데이터를 하나의 리스트로 반환하는 편의 메서드 (선택적)
    def get_all_articles(self) -> List[ArticleData]:
        """모든 소스의 데이터를 하나의 리스트로 결합하여 반환합니다."""
        all_articles = (
            self.newsapi_articles +
            self.nytimes_articles +
            self.naver_news +
            self.naver_blogs +
            self.naver_cafes +
            self.financial_trends +
            self.google_trends +
            self.naver_datalab_trends
        )
        return all_articles

    def log_summary(self):
        """수집된 데이터의 요약을 로깅합니다."""
        logger.info("Collected Data Summary:")
        logger.info(f"- NewsAPI: {len(self.newsapi_articles)} articles")
        logger.info(f"- NYTimes: {len(self.nytimes_articles)} articles")
        logger.info(f"- Naver News: {len(self.naver_news)} articles")
        logger.info(f"- Naver Blogs: {len(self.naver_blogs)} entries")
        logger.info(f"- Naver Cafes: {len(self.naver_cafes)} entries")
        logger.info(f"- Financial Trends: {len(self.financial_trends)} tickers")
        logger.info(f"- Google Trends: {len(self.google_trends)} keywords")
        logger.info(f"- Naver DataLab: {len(self.naver_datalab_trends)} keywords (Not Implemented)")
        total_items = len(self.get_all_articles())
        logger.info(f"- Total Items: {total_items}") 