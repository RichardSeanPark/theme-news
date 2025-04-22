import pytest
from unittest.mock import patch, MagicMock
# from google.adk import Context # 제거된 상태 유지
from google.adk.agents.invocation_context import InvocationContext # InvocationContext 임포트

# 테스트 대상 모듈 및 클래스 import
from theme_news_agent.sub_agents.data_collection.agent import DataCollectionAgent
from theme_news_agent.sub_agents.data_collection.models import ArticleData, CollectedData

# ArticleData fixture 생성 (딕셔너리 리스트 반환)
@pytest.fixture
def sample_article_data_dict(): # fixture 이름 변경
    return [
        {"title": "뉴스 제목 1", "content": "뉴스 내용 1", "source": "NewsAPI", "published": "2024-01-01T00:00:00Z", "url": "http://news.example.com/1"},
        {"title": "블로그 제목 1", "content": "블로그 내용 1", "source": "Naver Blog", "published": "2024-01-01T01:00:00Z", "url": "http://blog.example.com/1"},
        {"title": "카페 제목 1", "content": "카페 내용 1", "source": "Naver Cafe", "published": "2024-01-01T02:00:00Z", "url": "http://cafe.example.com/1"},
        {"title": "금융 트렌드 1", "content": "티커", "source": "Yahoo Finance Trending", "published": "2024-01-01T03:00:00Z", "url": None},
        {"title": "검색 트렌드 1", "content": None, "source": "Google Trends KR", "published": "2024-01-01T04:00:00Z", "url": None},
        # 추가 데이터 (소스별 구분 위해)
        {"title": "NYT 기사 1", "content": "NYT 내용 1", "source": "The New York Times", "published": "2024-01-02T00:00:00Z", "url": "http://nyt.example.com/1"},
        {"title": "Naver 뉴스 1", "content": "네이버 뉴스 내용 1", "source": "Naver News", "published": "Mon, 01 Jan 2024 09:00:00 +0900", "url": "http://navernews.example.com/1"},
    ]

# 테스트 클래스 정의
class TestDataCollectionAgent:

    # 2.8.1: 모든 데이터 수집 도구 호출 및 결과 통합 테스트
    @patch('theme_news_agent.sub_agents.data_collection.agent.NewsApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.BlogCafeApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.FinancialTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.SearchTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.WebCrawlingTool')
    def test_data_collection_process_integration(
        self, MockWebCrawlingTool, MockSearchTrendTool, MockFinancialTrendTool, MockBlogCafeApiTool, MockNewsApiTool, sample_article_data_dict # fixture 이름 변경
    ):
        # Arrange: 모킹 설정 (딕셔너리 반환)
        mock_news_api = MockNewsApiTool.return_value
        mock_news_api.fetch_newsapi_headlines.return_value = [sample_article_data_dict[0]] # NewsAPI 데이터
        mock_news_api.fetch_nytimes_articles.return_value = [sample_article_data_dict[5]] # NYT 데이터
        mock_news_api.fetch_naver_news.return_value = [sample_article_data_dict[6]] # Naver News 데이터

        mock_blog_cafe_api = MockBlogCafeApiTool.return_value
        mock_blog_cafe_api.fetch_naver_blogs.return_value = [sample_article_data_dict[1]] # Naver Blog 데이터
        mock_blog_cafe_api.fetch_naver_cafe_articles.return_value = [sample_article_data_dict[2]] # Naver Cafe 데이터

        mock_financial_tool = MockFinancialTrendTool.return_value
        mock_financial_tool.fetch_trending_tickers.return_value = [sample_article_data_dict[3]] # Financial 데이터

        mock_search_tool = MockSearchTrendTool.return_value
        mock_search_tool.fetch_google_trends.return_value = [sample_article_data_dict[4]] # Google Trends 데이터
        mock_search_tool.fetch_naver_datalab_trends.return_value = [] # Naver DataLab (미구현)

        agent = DataCollectionAgent()
        # ctx = Context() # 제거된 상태 유지
        ctx = MagicMock(spec=InvocationContext) # MagicMock에 spec 추가하여 타입 힌트 제공
        ctx.state = {} # state를 딕셔너리로 초기화

        # Act: process 메서드 호출
        result_message = agent.process(ctx)

        # Assert: 도구 호출 확인
        mock_news_api.fetch_newsapi_headlines.assert_called_once()
        mock_news_api.fetch_nytimes_articles.assert_called_once()
        mock_news_api.fetch_naver_news.assert_called_once()
        mock_blog_cafe_api.fetch_naver_blogs.assert_called_once()
        mock_blog_cafe_api.fetch_naver_cafe_articles.assert_called_once()
        mock_financial_tool.fetch_trending_tickers.assert_called_once()
        mock_search_tool.fetch_google_trends.assert_called_once()
        mock_search_tool.fetch_naver_datalab_trends.assert_called_once()

        # Assert: 상태 저장 확인
        assert "collected_data" in ctx.state
        collected_data = ctx.state["collected_data"]

        # CollectedData 모델 구조 및 내용 확인
        loaded_data = CollectedData(**collected_data)
        assert len(loaded_data.newsapi_articles) == 1
        assert len(loaded_data.nytimes_articles) == 1
        assert len(loaded_data.naver_news) == 1
        assert len(loaded_data.naver_blogs) == 1
        assert len(loaded_data.naver_cafes) == 1
        assert len(loaded_data.financial_trends) == 1
        assert len(loaded_data.google_trends) == 1
        assert len(loaded_data.naver_datalab_trends) == 0

        # 데이터 내용 샘플 확인 (title) - 속성 접근으로 변경
        assert loaded_data.newsapi_articles[0].title == "뉴스 제목 1"
        assert loaded_data.nytimes_articles[0].title == "NYT 기사 1"
        assert loaded_data.naver_news[0].title == "Naver 뉴스 1"
        assert loaded_data.naver_blogs[0].title == "블로그 제목 1"
        assert loaded_data.naver_cafes[0].title == "카페 제목 1"
        assert loaded_data.financial_trends[0].title == "금융 트렌드 1"
        assert loaded_data.google_trends[0].title == "검색 트렌드 1"

        # Assert: 결과 메시지 확인 (소스별 건수)
        assert "데이터 수집 완료." in result_message
        assert "NewsAPI: 1건" in result_message
        assert "NYTimes: 1건" in result_message
        assert "NaverNews: 1건" in result_message
        assert "NaverBlog: 1건" in result_message
        assert "NaverCafe: 1건" in result_message
        assert "Financial: 1건" in result_message
        assert "GoogleTrends: 1건" in result_message
        assert "NaverDataLab: 0건" in result_message
        assert "오류 발생" not in result_message

    # 2.8.2: 개별 도구 호출 시 오류 처리 테스트
    @patch('theme_news_agent.sub_agents.data_collection.agent.NewsApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.BlogCafeApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.FinancialTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.SearchTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.WebCrawlingTool')
    def test_data_collection_process_error_handling(
        self, MockWebCrawlingTool, MockSearchTrendTool, MockFinancialTrendTool, MockBlogCafeApiTool, MockNewsApiTool, sample_article_data_dict
    ):
        # Arrange: NewsAPI 헤드라인 호출 시 오류 발생 모킹
        mock_news_api = MockNewsApiTool.return_value
        mock_news_api.fetch_newsapi_headlines.side_effect = Exception("NewsAPI Headline Error")
        mock_news_api.fetch_nytimes_articles.return_value = [sample_article_data_dict[5]] # 정상
        mock_news_api.fetch_naver_news.return_value = [sample_article_data_dict[6]] # 정상

        # Arrange: 다른 도구들은 정상 작동 모킹
        mock_blog_cafe_api = MockBlogCafeApiTool.return_value
        mock_blog_cafe_api.fetch_naver_blogs.return_value = [sample_article_data_dict[1]]
        mock_blog_cafe_api.fetch_naver_cafe_articles.return_value = [sample_article_data_dict[2]]

        mock_financial_tool = MockFinancialTrendTool.return_value
        mock_financial_tool.fetch_trending_tickers.return_value = [sample_article_data_dict[3]]

        mock_search_tool = MockSearchTrendTool.return_value
        mock_search_tool.fetch_google_trends.return_value = [sample_article_data_dict[4]]
        mock_search_tool.fetch_naver_datalab_trends.return_value = []

        agent = DataCollectionAgent()
        # ctx = Context() # 제거된 상태 유지
        ctx = MagicMock(spec=InvocationContext) # MagicMock에 spec 추가
        ctx.state = {} # state를 딕셔너리로 초기화

        # Act
        result_message = agent.process(ctx)

        # Assert: 상태 저장 확인 (오류 발생한 소스 제외)
        assert "collected_data" in ctx.state
        collected_data = ctx.state["collected_data"]
        loaded_data = CollectedData(**collected_data)

        assert len(loaded_data.newsapi_articles) == 0 # 오류 발생, 0건이어야 함
        assert len(loaded_data.nytimes_articles) == 1
        assert len(loaded_data.naver_news) == 1
        assert len(loaded_data.naver_blogs) == 1
        assert len(loaded_data.naver_cafes) == 1
        assert len(loaded_data.financial_trends) == 1
        assert len(loaded_data.google_trends) == 1

        # Assert: 결과 메시지 확인 (오류 정보 포함)
        assert "데이터 수집 완료." in result_message
        assert "NewsAPI: 0건" in result_message
        assert "NYTimes: 1건" in result_message
        # ... 다른 소스 건수 확인 ...
        assert "오류 발생: newsapi: NewsAPI 헤드라인 수집 오류: NewsAPI Headline Error" in result_message

    # 2.8.3: 선택적 웹 크롤링 로직 테스트 (크롤링 로직 활성화 시)
    @patch('theme_news_agent.sub_agents.data_collection.agent.NewsApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.BlogCafeApiTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.FinancialTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.SearchTrendTool')
    @patch('theme_news_agent.sub_agents.data_collection.agent.WebCrawlingTool')
    def test_data_collection_process_optional_crawling(
        self, MockWebCrawlingTool, MockSearchTrendTool, MockFinancialTrendTool, MockBlogCafeApiTool, MockNewsApiTool, sample_article_data_dict # fixture 사용하도록 수정
    ):
        # Arrange: 뉴스 데이터 모킹 (URL은 있고 content는 없음)
        mock_news_data_no_content = [
            # sample_article_data_dict에서 content가 None인 항목 생성 또는 수정
            {"title": "크롤링 대상 뉴스", "content": None, "source": "NewsAPI", "published": "2024-01-01T00:00:00Z", "url": "http://crawl.example.com"}
        ]
        mock_news_api = MockNewsApiTool.return_value
        mock_news_api.fetch_newsapi_headlines.return_value = mock_news_data_no_content
        mock_news_api.fetch_nytimes_articles.return_value = []
        mock_news_api.fetch_naver_news.return_value = []

        # Arrange: 다른 도구들은 빈 데이터 반환 모킹
        MockBlogCafeApiTool.return_value.fetch_naver_blogs.return_value = []
        MockBlogCafeApiTool.return_value.fetch_naver_cafe_articles.return_value = []
        MockFinancialTrendTool.return_value.fetch_trending_tickers.return_value = []
        MockSearchTrendTool.return_value.fetch_google_trends.return_value = []
        MockSearchTrendTool.return_value.fetch_naver_datalab_trends.return_value = []

        # Arrange: 웹 크롤링 도구 모킹
        mock_crawler = MockWebCrawlingTool.return_value
        mock_crawler.fetch_full_content.return_value = "크롤링된 본문 내용"

        agent = DataCollectionAgent()
        ctx = MagicMock(spec=InvocationContext)
        ctx.state = {}

        # Act
        agent.process(ctx)

        # Assert: 크롤러 호출 확인
        mock_crawler.fetch_full_content.assert_called_once_with(url="http://crawl.example.com") # url 인자 명시

        # Assert: 상태 저장 확인 (content 업데이트 확인)
        assert "collected_data" in ctx.state
        collected_data = ctx.state["collected_data"]
        loaded_data = CollectedData(**collected_data)

        assert len(loaded_data.newsapi_articles) == 1
        assert loaded_data.newsapi_articles[0].content == "크롤링된 본문 내용" # 객체 속성 접근 및 업데이트 확인 