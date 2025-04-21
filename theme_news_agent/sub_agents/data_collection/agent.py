from google.adk import Agent
from google.adk.agents.invocation_context import InvocationContext
from typing import List, Dict, Any, Optional # Optional 추가
import logging # 로거 추가
# from .tools.news_api_tool import NewsApiTool  # 주석 해제 필요
# from .tools.blog_cafe_api_tool import BlogCafeApiTool # 주석 해제 필요
# from .tools.financial_trend_tool import FinancialTrendTool # 주석 해제 필요
# from .tools.search_trend_tool import SearchTrendTool # 주석 해제 필요
# from .tools.web_crawling_tool import WebCrawlingTool # 주석 해제 필요
# from .models import CollectedData # 주석 해제 필요

# 필요한 도구 및 모델 import (주석 해제)
from .tools.news_api_tool import NewsApiTool
from .tools.blog_cafe_api_tool import BlogCafeApiTool
from .tools.financial_trend_tool import FinancialTrendTool
from .tools.search_trend_tool import SearchTrendTool
from .tools.web_crawling_tool import WebCrawlingTool # 선택적 크롤링 위해 import 유지
from .models import CollectedData, ArticleData # CollectedData 및 ArticleData import

# 로거 설정 (agent.py 내에서도 사용 가능하도록)
logger = logging.getLogger(__name__)
# 기본 로깅 레벨 설정 (필요시 조정)
# logging.basicConfig(level=logging.INFO) # 애플리케이션 레벨에서 설정 권장

class DataCollectionAgent(Agent):
    """
    다양한 소스에서 데이터를 수집하는 에이전트입니다.
    - 뉴스 API (NewsAPI, NYTimes, Naver)
    - 블로그/카페 API (Naver)
    - 금융 트렌드 (웹 스크래핑 또는 API)
    - 검색 트렌드 (Google Trends, Naver DataLab)
    - 웹 크롤링 (필요시)
    """
    # 각 도구 필드를 Optional 및 기본값 None으로 선언합니다.
    news_api_tool: Optional[NewsApiTool] = None
    blog_cafe_api_tool: Optional[BlogCafeApiTool] = None
    financial_trend_tool: Optional[FinancialTrendTool] = None
    search_trend_tool: Optional[SearchTrendTool] = None
    web_crawling_tool: Optional[WebCrawlingTool] = None

    def __init__(self, name: str = "DataCollector", description: str = "데이터 수집 에이전트") -> None:
        # super().__init__ 호출을 먼저 수행합니다.
        super().__init__(name=name, description=description)
        # super().__init__ 호출 후에 도구 인스턴스를 생성하고 할당합니다.
        self.news_api_tool = NewsApiTool()
        self.blog_cafe_api_tool = BlogCafeApiTool()
        self.financial_trend_tool = FinancialTrendTool()
        self.search_trend_tool = SearchTrendTool()
        self.web_crawling_tool = WebCrawlingTool()

    def process(self, ctx: InvocationContext) -> str:
        """
        데이터 수집 워크플로우를 실행하고 결과를 상태에 저장합니다.
        """
        # 데이터를 소스별로 저장할 딕셔너리 초기화
        source_data: Dict[str, List[Dict[str, Any]]] = {
            "newsapi": [],
            "nytimes": [],
            "naver_news": [],
            "naver_blogs": [],
            "naver_cafes": [],
            "financial": [],
            "google_trends": [],
            "naver_datalab": []
        }
        errors: Dict[str, str] = {}

        # 도구 사용 전 None 체크 추가 (방어적 코딩)
        if not self.news_api_tool or not self.blog_cafe_api_tool or \
           not self.financial_trend_tool or not self.search_trend_tool or \
           not self.web_crawling_tool:
            error_msg = "DataCollectionAgent의 도구 중 일부가 초기화되지 않았습니다."
            logger.error(error_msg)
            return f"오류: {error_msg}"

        try:
            # 뉴스 데이터 수집
            newsapi_results = self.news_api_tool.fetch_newsapi_headlines()
            source_data["newsapi"].extend(newsapi_results)
            logger.info(f"NewsAPI 헤드라인 수집 완료: {len(newsapi_results)}건")
        except Exception as e:
            logger.error(f"NewsAPI 헤드라인 수집 중 오류: {e}", exc_info=True)
            errors["newsapi"] = f"NewsAPI 헤드라인 수집 오류: {e}"

        try:
            nytimes_results = self.news_api_tool.fetch_nytimes_articles()
            source_data["nytimes"].extend(nytimes_results)
            logger.info(f"NYTimes 기사 수집 완료: {len(nytimes_results)}건")
        except Exception as e:
            logger.error(f"NYTimes 기사 수집 중 오류: {e}", exc_info=True)
            errors["nytimes"] = f"NYTimes 기사 수집 오류: {e}"

        try:
            naver_news_results = self.news_api_tool.fetch_naver_news()
            source_data["naver_news"].extend(naver_news_results)
            logger.info(f"Naver 뉴스 수집 완료: {len(naver_news_results)}건")
        except Exception as e:
            logger.error(f"Naver 뉴스 수집 중 오류: {e}", exc_info=True)
            errors["naver_news"] = f"Naver 뉴스 수집 오류: {e}"

        try:
            # 블로그/카페 데이터 수집
            naver_blogs_results = self.blog_cafe_api_tool.fetch_naver_blogs()
            source_data["naver_blogs"].extend(naver_blogs_results)
            logger.info(f"Naver 블로그 수집 완료: {len(naver_blogs_results)}건")
        except Exception as e:
            logger.error(f"Naver 블로그 수집 중 오류: {e}", exc_info=True)
            errors["naver_blogs"] = f"Naver 블로그 수집 오류: {e}"

        try:
            naver_cafes_results = self.blog_cafe_api_tool.fetch_naver_cafe_articles()
            source_data["naver_cafes"].extend(naver_cafes_results)
            logger.info(f"Naver 카페 수집 완료: {len(naver_cafes_results)}건")
        except Exception as e:
            logger.error(f"Naver 카페 수집 중 오류: {e}", exc_info=True)
            errors["naver_cafes"] = f"Naver 카페 수집 오류: {e}"

        try:
            # 금융 트렌드 데이터 수집
            financial_results = self.financial_trend_tool.fetch_trending_tickers()
            source_data["financial"].extend(financial_results)
            logger.info(f"금융 트렌드 수집 완료: {len(financial_results)}건")
        except Exception as e:
            logger.error(f"금융 트렌드 수집 중 오류: {e}", exc_info=True)
            errors["financial"] = f"금융 트렌드 수집 오류: {e}"

        try:
            # 검색 트렌드 데이터 수집
            google_trends_results = self.search_trend_tool.fetch_google_trends()
            source_data["google_trends"].extend(google_trends_results)
            logger.info(f"Google Trends 수집 완료: {len(google_trends_results)}건")
        except Exception as e:
            logger.error(f"Google Trends 수집 중 오류: {e}", exc_info=True)
            errors["google_trends"] = f"Google Trends 수집 오류: {e}"

        try:
            naver_datalab_results = self.search_trend_tool.fetch_naver_datalab_trends()
            source_data["naver_datalab"].extend(naver_datalab_results)
            logger.info(f"Naver DataLab 수집 완료: {len(naver_datalab_results)}건") # 미구현 상태
        except Exception as e:
            logger.error(f"Naver DataLab 수집 중 오류: {e}", exc_info=True)
            errors["naver_datalab"] = f"Naver DataLab 수집 오류: {e}"

        # --- (선택적 크롤링) 뉴스/블로그 결과 URL 기반 WebCrawlingTool 호출하여 content 보강 --- (주석 해제)
        logger.info("Starting optional web crawling for content enrichment...")
        crawlable_items = (
            source_data["newsapi"] + source_data["nytimes"] + source_data["naver_news"] +
            source_data["naver_blogs"] + source_data["naver_cafes"]
        )
        crawled_count = 0
        for item in crawlable_items:
            # URL이 있고 content가 비어있는 경우 (딕셔너리 접근)
            if item.get('url') and not item.get('content'):
                logger.debug(f"Attempting to crawl for content: {item.get('url')}")
                try:
                    # fetch_full_content 사용 (정적 콘텐츠 우선)
                    full_content = self.web_crawling_tool.fetch_full_content(url=item['url'])
                    if full_content:
                        item['content'] = full_content # 딕셔너리 직접 업데이트
                        crawled_count += 1
                        logger.debug(f"Successfully crawled and updated content for: {item.get('url')}")
                    else:
                        logger.warning(f"Crawling returned no content for: {item.get('url')}")
                    # TODO: 필요시 fetch_dynamic_content 사용 로직 추가
                except Exception as crawl_e:
                    logger.error(f"Error crawling {item.get('url')}: {crawl_e}", exc_info=True)
                    # 크롤링 실패는 전체 프로세스 중단시키지 않음
        logger.info(f"Optional web crawling finished. Enriched {crawled_count} items.")

        # 수집된 데이터를 CollectedData 모델로 통합
        # 각 도구 함수는 dict 리스트를 반환하므로 ArticleData로 변환 필요
        # TODO: ArticleData 유효성 검사 및 변환 강화
        def to_article_data_list(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            validated_list = []
            for item in data_list:
                try:
                    validated_article = ArticleData(**item)
                    # 유효성 검사 통과 시 모델 덤프 추가
                    validated_list.append(validated_article.model_dump())
                except Exception as pydantic_e:
                    # 유효성 검사 실패 시 경고 로깅
                    logger.warning(f"데이터 유효성 검사 실패: {item}. 오류: {pydantic_e}")
            return validated_list

        # CollectedData 모델 생성
        try:
            collected_data_model = CollectedData(
                newsapi_articles=to_article_data_list(source_data["newsapi"]),
                nytimes_articles=to_article_data_list(source_data["nytimes"]),
                naver_news=to_article_data_list(source_data["naver_news"]),
                naver_blogs=to_article_data_list(source_data["naver_blogs"]),
                naver_cafes=to_article_data_list(source_data["naver_cafes"]),
                financial_trends=to_article_data_list(source_data["financial"]),
                google_trends=to_article_data_list(source_data["google_trends"]),
                naver_datalab_trends=to_article_data_list(source_data["naver_datalab"])
            )
            # 상태 저장
            ctx.state["collected_data"] = collected_data_model.model_dump()
            # 결과 메시지 생성 (모델 필드 이름 사용)
            status_message = "데이터 수집 완료. "
            status_message += f"NewsAPI: {len(collected_data_model.newsapi_articles)}건, "
            status_message += f"NYTimes: {len(collected_data_model.nytimes_articles)}건, "
            status_message += f"NaverNews: {len(collected_data_model.naver_news)}건, "
            status_message += f"NaverBlog: {len(collected_data_model.naver_blogs)}건, "
            status_message += f"NaverCafe: {len(collected_data_model.naver_cafes)}건, "
            status_message += f"Financial: {len(collected_data_model.financial_trends)}건, "
            status_message += f"GoogleTrends: {len(collected_data_model.google_trends)}건, "
            status_message += f"NaverDataLab: {len(collected_data_model.naver_datalab_trends)}건."

        except Exception as model_e:
            logger.error(f"CollectedData 모델 생성 또는 상태 저장 중 오류: {model_e}", exc_info=True)
            errors["aggregation"] = f"데이터 통합 중 오류 발생: {model_e}"
            status_message = "데이터 수집 중 일부 데이터 통합 실패."
            # 상태 저장 실패 시 비우기 (선택적)
            if "collected_data" in ctx.state:
                del ctx.state["collected_data"]

        if errors:
            error_details = "; ".join([f"{k}: {v}" for k, v in errors.items()])
            status_message += f"\n오류 발생: {error_details}"
            logger.warning(f"데이터 수집 완료 (오류 포함): {error_details}")
        else:
            logger.info(status_message) # 성공 시 INFO 로그

        return status_message
