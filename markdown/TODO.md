# LLM 트렌드 테마 추출 AI 에이전트 - 개발 TODO 리스트

이 문서는 설계 및 개발 계획 문서와 Google Agent Development Kit(ADK) 모범 사례를 기반으로 LLM 트렌드 테마 추출 AI 에이전트 개발에 필요한 단계별 작업을 상세히 설명합니다.

## 1단계: 프로젝트 설정 및 환경 구성

- [X] **1.1 프로젝트 디렉토리 구조 생성:**
    - [X] 메인 에이전트 디렉토리 생성: `theme_news_agent/` (ADK 규칙에 따라 하이픈 사용). # 단순 디렉토리 생성으로 testcase-guide.md 기반 테스트 불가
    - [X] 핵심 파이썬 패키지 디렉토리 생성: `theme_news_agent/` (밑줄 사용).
    - [X] `theme_news_agent/__init__.py` 생성.
    - [X] `theme_news_agent/agent.py` 생성 (마스터 에이전트용).
    - [X] `theme_news_agent/sub_agents/` 디렉토리 생성.
    - [X] `sub_agents/` 내부에 계획된 각 에이전트용 하위 디렉토리 생성:
        - [X] `data_collection/`
        - [X] `keyword_extraction/`
        - [X] `theme_clustering/`
        - [X] `trend_analysis/`
        - [X] `summary_generation/`
    - [X] 각 하위 에이전트 디렉토리 내부에 `agent.py`, `prompt.py` (LLM 에이전트용), `tools/` (도구 사용 에이전트용) 생성.
    - [X] `sub_agents/` 및 각 하위 에이전트 디렉토리에 `__init__.py` 파일 생성.
    - [X] `theme_news_agent/deployment/` 디렉토리 생성.
    - [X] `theme_news_agent/eval/` 디렉토리 생성.
    - [X] `theme_news_agent/tests/` 디렉토리 생성.

- [X] **1.2 의존성 관리 초기화:**
    - [X] `theme_news_agent/` 디렉토리로 이동.
    - [X] `poetry init` 실행하여 `pyproject.toml` 생성. 프로젝트 메타데이터(이름, 버전, 설명 등) 구성.
    - [X] `Dev_Plan.md` (섹션 7.2) 및 `Design.md` 기반 핵심 의존성을 `poetry add`를 사용하여 추가:
        - `google-adk` # ADK 프레임워크 (LLM 연결 포함)
        # - `google-generativeai` # google-adk가 내부적으로 관리하므로 명시적 추가 불필요
        - `requests`
        - `beautifulsoup4`
        - `playwright` # (선택적 크롤링용)
        - `newspaper3k` # (뉴스 본문 추출용 대체/보완)
        - `numpy`
        - `pandas` # (데이터 처리 및 분석용)
        - `pydantic` # (데이터 유효성 검사 및 모델링용)
        - `python-dotenv` # (.env 로딩용)
    - [X] `poetry add pytest --group dev` # 테스트용 의존성 추가
    - [X] `poetry install --with dev` 실행하여 모든 의존성 설치 및 `poetry.lock` 생성.

- [X] **1.3 환경 변수 구성:**
    - [X] ADK 퀵스타트 및 `Dev_Plan.md` 요구사항 기반으로 `theme_news_agent/.env.example` 생성. 다음 플레이스홀더 포함:
        - `# Gemini API Configuration`
        - `GOOGLE_API_KEY=` # (AI Studio Key)
        - `GOOGLE_GENAI_USE_VERTEXAI="False"` # (True로 변경 시 아래 설정 필요)
        - `VERTEX_AI_PROJECT_ID=`
        - `VERTEX_AI_LOCATION=`
        - `# News APIs`
        - `NEWS_API_KEY=` # (newsapi.org)
        - `NYT_API_KEY=` # (NYTimes API)
        - `# Naver Search APIs`
        - `NAVER_CLIENT_ID=`
        - `NAVER_CLIENT_SECRET=`
        - `# Agent Configuration`
        - `DATA_FETCH_PERIOD_HOURS=24` # 데이터 수집 기간 (시간 단위)
        - `TREND_TOP_N=20` # 트렌드 분석 상위 N개
        - `HISTORICAL_DATA_PATH="data/historical_themes.json"` # 과거 데이터 저장 경로
    - [X] `.env.example`을 복사하여 `theme_news_agent/.env` 생성.
    - [X] `.gitignore` 파일에 `.env` 및 민감 정보 파일 패턴 추가.

- [X] **1.4 기본 프로젝트 파일:**
    - [X] 에이전트 목적, 설정 방법, 실행 방법 등을 포함하는 상세 `theme_news_agent/README.md` 생성.
    - [X] 데이터 저장용 디렉토리 생성 (예: `theme_news_agent/data/`) 및 `.gitignore`에 추가 (필요시).

## 2단계: 데이터 수집 에이전트 구현

- [X] **2.1 `DataCollectionAgent` 정의:**
    - [X] `theme_news_agent/sub_agents/data_collection/agent.py`에 `DataCollectionAgent` 클래스 정의 (`google.adk.Agent` 상속).
    - [X] `__init__` 메서드에서 필요한 도구 (News, Blog/Cafe, **Financial Trend**, **Search Trend**, Crawling) 클래스 인스턴스화.

- [X] **2.2 뉴스 API 도구 구현 (`NewsApiTool`):**
    - [X] `theme_news_agent/sub_agents/data_collection/tools/news_api_tool.py` 생성.
    - [X] `@Tool` 데코레이터를 사용하여 함수 정의 (`fetch_newsapi_headlines`, `fetch_nytimes_articles`, `fetch_naver_news`).
    - [X] 각 함수에서 해당 API 호출 로직 구현:
        - NewsAPI: `https://newsapi.org/v2/top-headlines` (국가별) 또는 `/v2/everything` (키워드/날짜) 사용. `country=kr`, `country=us`, `category=general`, `from`/`to` 파라미터 활용. (트렌드 초기 신호 감지에 중요할 수 있음)
        - NYTimes API: `https://api.nytimes.com/svc/topstories/v2/...` 또는 `Article Search API` 사용. `begin_date`/`end_date` 파라미터 활용.
        - Naver News API: `https://openapi.naver.com/v1/search/news.json` 사용. `query` (다양한 일반/분야별 키워드 조합 사용 고려), `display=100`, `sort=date` 파라미터 활용. `X-Naver-Client-Id`/`Secret` 헤더 설정.
    - [X] 환경 변수에서 API 키 및 설정 로드 (API Key, Client ID/Secret, `DATA_FETCH_PERIOD_HOURS`).
    - [X] 각 API 응답(JSON)을 표준 Pydantic 모델 (`ArticleData`) 또는 딕셔너리 리스트로 파싱. `published` 필드는 일관된 형식(ISO 8601 권장)으로 변환.
    - [X] API 호출 시 `requests` 라이브러리 사용 및 타임아웃 설정, 응답 상태 코드 확인 등 기본 오류 처리 구현.

- [X] **2.3 블로그/카페 검색 API 도구 구현 (`BlogCafeApiTool`):**
    - [X] `theme_news_agent/sub_agents/data_collection/tools/blog_cafe_api_tool.py` 생성.
    - [X] `@Tool` 데코레이터를 사용하여 함수 정의 (`fetch_naver_blogs`, `fetch_naver_cafe_articles`).
    - [X] 각 함수에서 해당 API 호출 로직 구현:
        - Naver Blog API: `https://openapi.naver.com/v1/search/blog.json`. `query` (예: "오늘", "방법", "후기", "최신" 등 **다양한 일반 키워드 또는 이전 트렌드 기반 키워드를 순환/조합하여 사용**), `display=100`, `sort=date`.
        - Naver Cafe API: `https://openapi.naver.com/v1/search/cafearticle.json`. 상동.
    - [X] 환경 변수에서 Naver Client ID/Secret 로드.
    - [X] 결과를 `ArticleData` 표준 형식으로 파싱. `content`는 API의 `description` 사용. `published`는 `postdate` 또는 `description`에서 추출 시도. `source`는 "Naver Blog", "Naver Cafe" 등으로 구분.
    - [X] API 오류 처리 구현.

- [X] **2.4 금융 트렌드 도구 구현 (`FinancialTrendTool` - 신규):**
    - [X] `theme_news_agent/sub_agents/data_collection/tools/financial_trend_tool.py` 생성.
    - [X] `@Tool` 데코레이터 적용 함수 정의: `fetch_trending_tickers()`.
    - [X] 웹 스크래핑 (`requests` + `playwright`) 또는 비공식 API를 사용하여 금융 정보 사이트(예: Yahoo Finance 'Trending Tickers')에서 현재 인기/거래량 급증 주식 티커 목록 가져오기 로직 구현.
    - [X] 스크래핑 시 HTML 구조 변경에 대비한 견고한 파싱 로직 및 오류 처리 구현.
    - [X] 파싱 결과(티커 심볼, 회사명 등)를 `ArticleData`와 유사한 표준 형식으로 변환 (예: `title`=회사명, `content`=티커 심볼, `source`="Yahoo Finance Trending", `published`=수집 시각).

- [ ] **2.5 검색 트렌드 도구 구현 (`SearchTrendTool` - 신규):**
    - [ ] `theme_news_agent/sub_agents/data_collection/tools/search_trend_tool.py` 생성.
    - [ ] `@Tool` 데코레이터 적용 함수 정의: `fetch_google_trends()`, `fetch_naver_datalab_trends()`.
    - [ ] `pytrends` 라이브러리 설치 (`poetry add pytrends`).
    - [ ] `pytrends` 사용하여 Google Trends 일간/실시간 인기 급상승 검색어 가져오기 로직 구현 (지역 설정: 한국, 미국 등).
    - [ ] (고급) Naver DataLab 웹사이트 스크래핑 또는 관련 비공식 라이브러리를 사용하여 네이버 급상승 검색어 데이터 가져오기 로직 구현.
    - [ ] 가져온 검색어 목록을 `ArticleData` 표준 형식으로 변환 (예: `title`=검색어, `source`="Google Trends" / "Naver DataLab", `content`=None, `published`=수집 시각).
    - [ ] 관련 라이브러리/스크래핑 오류 처리 구현.

- [ ] **2.6 웹 크롤링 도구 구현 (`WebCrawlingTool` - 기존, 순서 조정):**
    - [ ] `theme_news_agent/sub_agents/data_collection/tools/web_crawling_tool.py` 생성 (기존과 동일).
    - [ ] `@Tool` 데코레이터 적용 함수 정의: `fetch_full_content(url: str) -> str | None`.
    - [ ] 뉴스/블로그 API 결과의 URL에서 본문 텍스트 추출 로직 구현 (`requests` + `BeautifulSoup4` / `Newspaper3k`).
    - [ ] (고급) `Playwright` 사용 함수 구현 (`fetch_dynamic_content`).
    - [ ] 오류 처리, `robots.txt` 확인 (선택적), `time.sleep()` 추가.

- [ ] **2.7 데이터 모델 정의 (Pydantic):**
    - [ ] `theme_news_agent/sub_agents/data_collection/models.py` 생성.
    - [ ] `ArticleData` Pydantic 모델 정의 (기존과 유사: `title`, `content`, `source`, `published`, `url`). `source` 필드는 이제 "NewsAPI", "NYTimes", "Naver News", "Naver Blog", "Naver Cafe", "Yahoo Finance Trending", "Google Trends", "Naver DataLab" 등을 포함할 수 있음.
    - [ ] `CollectedData` Pydantic 모델 정의. 필드를 좀 더 일반화하거나 (예: `articles: List[ArticleData]`), 소스별 리스트를 유지할 수 있음 (예: `news: List`, `blogs: List`, ..., `financial_trends: List`, `search_trends: List`). 후자가 후처리 단계에서 소스별 분석에 유리할 수 있음.

- [ ] **2.8 도구 통합 및 상태 관리:**
    - [ ] `DataCollectionAgent.process` 메서드 구현:
        - 모든 데이터 수집 도구 (뉴스, 블로그/카페, 금융 트렌드, 검색 트렌드) 호출.
        - (선택적 크롤링) 뉴스/블로그 결과 URL 기반 `WebCrawlingTool` 호출하여 `content` 보강.
        - 모든 결과를 `CollectedData` 모델 객체로 통합 및 유효성 검사 (다양한 소스 처리).
        - `ctx.state["collected_data"] = collected_data_model.model_dump()` 형태로 세션 상태에 저장.
        - 성공/실패 및 소스별 수집 건수 포함한 상태 메시지 반환.

## 3단계: 키워드 추출 에이전트 구현

- [ ] **3.1 `KeywordExtractionAgent` 정의:**
    - [ ] `theme_news_agent/sub_agents/keyword_extraction/agent.py`에 `KeywordExtractionAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [ ] `__init__`에서 `model` (예: 'gemini-1.5-flash-latest'), `description`, `instruction` 설정.

- [ ] **3.2 추출 프롬프트 정의:**
    - [ ] `theme_news_agent/sub_agents/keyword_extraction/prompt.py`에 프롬프트 문자열 또는 함수 정의 (`get_extraction_prompt`).
    - [ ] `Design.md` 섹션 4 (1) 및 `Dev_Plan.md` 섹션 5.2 참고하여 프롬프트 작성. LLM에게 입력 텍스트(제목+요약)에서 주요 키워드/엔티티(인물, 조직, 이벤트, 제품, 기술, 주제 명사구 등) 추출 지시.
    - [ ] 출력 형식을 명확히 지정: **반드시 JSON 형식의 키워드 문자열 리스트로 반환**하도록 요구. 예: `["키워드1", "키워드2", ...]`.

- [ ] **3.3 에이전트 로직 구현:**
    - [ ] `KeywordExtractionAgent.process` 메서드 구현:
        - `ctx.state.get("collected_data")` 로드.
        - LLM 입력 생성: 다양한 소스의 `title` 및 `content` 필드를 적절히 조합/선택하여 LLM 입력 구성. (예: 검색어 자체를 중요한 입력으로 간주).
        - `self.generate_content` 또는 유사 메서드 호출하여 LLM 실행.
        - LLM 응답 파싱: 반환된 문자열이 유효한 JSON 리스트인지 확인하고 파싱. 파싱 실패 시 재시도 또는 오류 처리.

- [ ] **3.4 키워드 빈도 계산 도구/함수 구현:**
    - [ ] `theme_news_agent/sub_agents/keyword_extraction/tools/frequency_calculator.py` (또는 agent.py 내 함수) 생성.
    - [ ] 함수 정의: `calculate_keyword_frequencies(keywords: List[str], collected_data: CollectedData) -> List[Dict]`.
    - [ ] 로직:
        - 입력 `keywords` 리스트의 각 키워드에 대해, `collected_data`의 모든 문서(`title` + `content`)에서 등장 횟수 계산 (대소문자 구분 없이).
        - 출처별 빈도 계산 시, 이제 금융 트렌드, 검색 트렌드 소스도 포함하여 집계.
        - 결과 형식: `[{ "keyword": "...", "frequency": { "total": N, "news": N, "blogs": N, "cafes": N, "finance": N, "search": N } }, ...]`.

- [ ] **3.5 상태 관리:**
    - [ ] `KeywordExtractionAgent.process`에서 빈도 계산 함수 호출.
    - [ ] 계산된 빈도 정보 포함 결과를 세션 상태에 저장: `ctx.state["keyword_results"] = keyword_frequency_data`.

## 4단계: 테마 클러스터링 에이전트 구현

- [ ] **4.1 `ThemeClusteringAgent` 정의:**
    - [ ] `theme_news_agent/sub_agents/theme_clustering/agent.py`에 `ThemeClusteringAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [ ] `__init__`에서 모델, 설명, 지침 설정.

- [ ] **4.2 클러스터링 프롬프트 정의:**
    - [ ] `theme_news_agent/sub_agents/theme_clustering/prompt.py`에 프롬프트 정의 (`get_clustering_prompt`).
    - [ ] `Design.md` 섹션 4 (3) 및 `Dev_Plan.md` 섹션 5.3 참고하여 프롬프트 작성. 입력으로 키워드 목록(언급량 포함)을 받고, 의미적으로 유사/연관된 키워드를 그룹화하고 각 그룹에 이해하기 쉬운 테마 이름을 부여하도록 지시.
    - [ ] 출력 형식을 명확히 지정: **반드시 `Design.md` 섹션 4 (3)의 예시와 같은 JSON 형식의 배열로 반환**하도록 요구. `[{"theme": "...", "keywords": ["...", ...], "mentions": N}, ...]`.

- [ ] **4.3 에이전트 로직 구현:**
    - [ ] `ThemeClusteringAgent.process` 메서드 구현:
        - `ctx.state.get("keyword_results")`로 이전 단계 결과 로드.
        - LLM 프롬프트 입력 형식에 맞게 키워드 데이터 포맷 (예: 문자열로 변환).
        - LLM 호출.
        - LLM 응답이 유효한 JSON 배열인지 확인하고 파싱. 각 항목의 `mentions` 값은 입력 빈도의 합계와 일치하는지 검증 (선택 사항, LLM이 계산하도록 둘 수도 있음). 오류 처리 구현.

- [ ] **4.4 상태 관리:**
    - [ ] 파싱된 클러스터링 결과를 세션 상태에 저장: `ctx.state["clustered_themes"] = clustered_theme_data`.

## 5단계: 트렌드 분석 에이전트 구현

- [ ] **5.1 `TrendAnalysisAgent` 정의:**
    - [ ] `theme_news_agent/sub_agents/trend_analysis/agent.py`에 `TrendAnalysisAgent` 클래스 정의 (`google.adk.Agent` 상속).
    - [ ] `__init__`에서 통계 분석 도구 인스턴스화.

- [ ] **5.2 통계 분석 도구 구현 (`StatisticalAnalysisTool`):**
    - [ ] `theme_news_agent/sub_agents/trend_analysis/tools/stats_tool.py` 생성.
    - [ ] `@Tool` 데코레이터 적용 함수 정의: `calculate_trends(current_themes: List[Dict]) -> List[Dict]`.
    - [ ] **과거 데이터 관리:**
        - 함수 내에서 과거 데이터 로드 로직 구현 (환경 변수 `HISTORICAL_DATA_PATH` 사용). 파일 없으면 빈 데이터로 시작. JSON 형식 사용.
        - 과거 데이터 구조 정의 (예: `{ "테마명": {"mentions_history": [과거 언급량 리스트], "avg": 평균, "std": 표준편차} }`).
    - [ ] **Z-점수 계산:**
        - `current_themes`의 각 테마에 대해:
            - 과거 데이터에서 해당 테마의 `avg`, `std` 조회.
            - `z = (current_mentions - avg) / std` 계산. (과거 데이터 없거나 std=0일 경우 z=0 또는 다른 값으로 처리).
        - 계산된 z-점수를 현재 테마 데이터에 추가.
    - [ ] **과거 데이터 업데이트:**
        - 현재 테마 언급량을 과거 데이터의 `mentions_history`에 추가.
        - 업데이트된 `mentions_history로 새로운 `avg`, `std` 계산 및 저장.
        - 변경된 과거 데이터를 파일에 다시 저장.
        - 변경된 과거 데이터를 파일에 다시 저장.
    - [ ] Z-점수가 추가된 테마 리스트 반환.

- [ ] **5.3 에이전트 로직 구현:**
    - [ ] `TrendAnalysisAgent.process` 메서드 구현:
        - `ctx.state.get("clustered_themes")` 로드.
        - `StatisticalAnalysisTool.calculate_trends` 호출하여 Z-점수 계산 및 데이터 업데이트.
        - 반환된 테마 리스트를 Z-점수 기준 내림차순 정렬.
        - 환경 변수 `TREND_TOP_N` 값에 따라 상위 N개 테마 선택.
        - 각 테마 딕셔너리에 'rank' 키 추가 (1부터 N까지).

- [ ] **5.4 상태 관리:**
    - [ ] 최종 순위가 매겨진 상위 트렌드 테마 목록을 세션 상태에 저장: `ctx.state["trend_results"] = ranked_themes`.

## 6단계: 요약 생성 에이전트 구현

- [ ] **6.1 `SummaryGenerationAgent` 정의:**
    - [ ] `theme_news_agent/sub_agents/summary_generation/agent.py`에 `SummaryGenerationAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [ ] `__init__`에서 모델, 설명, 지침 설정.

- [ ] **6.2 요약 프롬프트 정의:**
    - [ ] `theme_news_agent/sub_agents/summary_generation/prompt.py`에 프롬프트 정의 (`get_summary_prompt`).
    - [ ] `Design.md` 섹션 4 (5) 및 `Dev_Plan.md` 섹션 5.5 참고하여 프롬프트 작성. 입력으로 *단일* 테마 정보(테마명, 관련 키워드, 언급량 및 출처별 비중)를 받고, 해당 테마가 왜 화제가 되었는지 1-2 문장으로 요약하도록 지시.
    - [ ] 출력은 **요약 문장 문자열**만 반환하도록 요구.

- [ ] **6.3 에이전트 로직 구현:**
    - [ ] `SummaryGenerationAgent.process` 메서드 구현:
        - `ctx.state.get("trend_results")` 로드.
        - 상위 N개 테마 리스트를 반복:
            - 각 테마 정보를 프롬프트 입력 형식에 맞게 포맷. (언급량 상세 정보 포함)
            - LLM 호출하여 요약 생성.
            - LLM 응답(요약 문자열) 파싱 및 정리 (줄바꿈 제거 등).
            - 해당 테마 딕셔너리에 'summary' 키로 생성된 요약 추가.
        - 모든 테마에 요약이 추가된 리스트 준비.

- [ ] **6.4 상태 관리:**
    - [ ] 요약이 포함된 최종 결과 리스트를 세션 상태에 저장: `ctx.state["final_summary"] = final_results`.

## 7단계: 마스터 에이전트 및 워크플로우 구현

- [ ] **7.1 `MasterAgent` (워크플로우 오케스트레이터) 정의:**
    - [ ] `theme_news_agent/agent.py` 파일 수정.
    - [ ] 모든 하위 에이전트 클래스 임포트 (`from .sub_agents.data_collection.agent import DataCollectionAgent` 등).
    - [ ] 각 하위 에이전트 클래스의 인스턴스 생성.
    - [ ] `google.adk.agents.SequentialAgent` 사용하여 워크플로우 정의:
      ```python
      workflow_agent = SequentialAgent(
          name="ThemeNewsWorkflow",
          description="뉴스, 블로그, 카페 등에서 언급량 급증 테마를 추출하고 요약하는 워크플로우",
          agents=[
              data_collection_agent_instance,
              keyword_extraction_agent_instance,
              theme_clustering_agent_instance,
              trend_analysis_agent_instance,
              summary_generation_agent_instance
          ]
      )
      # ADK가 인식하도록 root_agent 변수에 할당 (또는 다른 이름 사용 시 __init__.py에서 노출)
      root_agent = workflow_agent 
      ```
    - [ ] `theme_news_agent/__init__.py`에서 `root_agent` 노출 확인: `from .agent import root_agent`.

- [ ] **7.2 최종 출력 처리 구현:**
    - [ ] 최종 결과를 처리하기 위한 별도 로직 추가 (선택 사항): `SequentialAgent`를 감싸는 커스텀 `MasterAgent`를 만들거나, `SequentialAgent`의 `after_agent_callback` 등을 활용.
    - [ ] 최종 결과(`ctx.state["final_summary"]`)를 가져와 콘솔 출력 형식으로 포맷하는 함수 구현 (`Design.md` 섹션 5 참조). 순위, 테마명, 언급량(총합, 출처별), 요약 포함.
    - [ ] 최종 결과를 JSON 출력 형식으로 포맷하는 함수 구현 (`Design.md` 섹션 5, `Dev_Plan.md` 섹션 6.1 참조). 필요한 모든 필드 포함.
    - [ ] 에이전트 실행 결과 반환 방식 결정:
        - `adk run` 사용 시: 최종 처리 단계에서 콘솔에 출력.
        - `adk web` 또는 프로그래밍 방식 호출 시: 가공된 JSON 문자열이나 객체를 반환하도록 `process` 메서드 수정.

## 8단계: 테스트 및 평가

- [ ] **8.1 단위 테스트:**
    - [ ] `theme_news_agent/tests/` 디렉토리에 `test_*.py` 파일 생성.
    - [ ] `pytest` 및 `unittest.mock` 사용하여 도구 함수 단위 테스트 작성 (API 호출 모킹, 데이터 파싱 검증, 계산 로직 검증).
    - [ ] 각 에이전트의 `process` 메서드 기본 흐름 테스트 (상태 로딩/저장, 도구/LLM 호출 모킹).
    - [ ] `poetry run pytest tests/` 명령어로 테스트 실행. `README.md`에 명령어 추가.

- [ ] **8.2 통합 / 평가 테스트:**
    - [ ] `theme_news_agent/eval/` 디렉토리에 `.test.json` 파일 생성. 각 파일은 하나의 완전한 시나리오 포함 (초기 입력 -> 최종 예상 출력 구조).
    - [ ] ADK 문서 참고하여 평가 스크립트(`eval/run_eval.py`) 작성. 스크립트는 `adk run`을 프로그래밍 방식으로 호출하거나 에이전트를 직접 로드하여 실행하고, 실제 출력과 `.test.json`의 예상 출력을 비교 (JSON 구조, 주요 필드 값 등).
    - [ ] `README.md`에 평가 스크립트 실행 방법 추가.

- [ ] **8.3 수동 테스트 (ADK CLI / 웹 UI):**
    - [ ] `adk run theme_news_agent/` 명령어로 CLI에서 실행 테스트. 다양한 입력 시나리오 테스트. (경로는 프로젝트 구조에 따라 조정 필요)
    - [ ] `adk web theme_news_agent/` 명령어로 웹 UI 실행. 브라우저에서 에이전트 선택 후 상호작용 테스트. (경로는 프로젝트 구조에 따라 조정 필요)

## 9단계: 문서화 및 개선

- [ ] **9.1 README 업데이트:**
    - [ ] `theme_news_agent/README.md` 상세 내용 업데이트.
    - [ ] 포함 내용: 프로젝트 목적, 아키텍처(Mermaid 다이어그램 포함 가능), 필요한 모든 API 키 및 환경 변수 설명, 설치 (`poetry install`), 로컬 실행(CLI, Web UI), 테스트 실행, 평가 실행 방법, 예시 입출력.

- [ ] **9.2 코드 정리 및 리팩토링:**
    - [ ] 전체 코드 검토: 가독성, PEP 8 준수, 불필요한 주석 제거, 의미 있는 변수/함수명 사용.
    - [ ] 오류 처리 강화: API 호출 실패, LLM 응답 오류, 데이터 파싱 실패 등 다양한 예외 상황 처리 개선.
    - [ ] 로깅 추가: 주요 단계 진행 상황, 오류 발생 시 로깅 (`logging` 모듈 사용).
    - [ ] 설정 값 관리 개선 (예: 하드코딩된 값 -> 환경 변수 또는 설정 파일).

## 10단계: 배포 (선택적 초기 단계)

- [ ] **10.1 Docker화 (선택 사항):**
    - [ ] `theme_news_agent/` 루트에 `Dockerfile` 생성. Python 환경 설정, 의존성 설치, 에이전트 실행 명령어 포함.
- [ ] **10.2 배포 스크립트 (선택 사항):**
    - [ ] `theme_news_agent/deployment/`에 배포 대상 플랫폼(Cloud Run, Vertex AI 등)에 맞는 스크립트 템플릿 작성 (`gcloud run deploy`, `adk deploy` 등 사용).

---
이 TODO 목록은 상세한 경로를 제공합니다. 개발 중 `Design.md`, `Dev_Plan.md` 및 ADK 문서를 자주 참조하십시오. 행운을 빕니다! 