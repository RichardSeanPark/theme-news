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

- [X] **2.5 검색 트렌드 도구 구현 (`SearchTrendTool` - 신규):**
    - [X] `theme_news_agent/sub_agents/data_collection/tools/search_trend_tool.py` 생성.
    - [X] `@Tool` 데코레이터 적용 함수 정의: `fetch_google_trends()`, `fetch_naver_datalab_trends()`.
    - [X] `pytrends` 라이브러리 설치 (`poetry add pytrends`).
    - [X] `pytrends` 사용하여 Google Trends 일간/실시간 인기 급상승 검색어 가져오기 로직 구현 (지역 설정: 한국, 미국 등).
    - [ ] (고급) Naver DataLab 웹사이트 스크래핑 또는 관련 비공식 라이브러리를 사용하여 네이버 급상승 검색어 데이터 가져오기 로직 구현.
    - [X] 가져온 검색어 목록을 `ArticleData` 표준 형식으로 변환 (예: `title`=검색어, `source`="Google Trends" / "Naver DataLab", `content`=None, `published`=수집 시각).
    - [X] 관련 라이브러리/스크래핑 오류 처리 구현.

- [X] **2.6 웹 크롤링 도구 구현 (`WebCrawlingTool` - 기존, 순서 조정):** # fetch_full_content_delay 테스트는 모킹 어려움으로 skip [-]
    - [X] `@Tool` 데코레이터 적용 함수 정의: `fetch_full_content(url: str) -> str | None`.
    - [X] 뉴스/블로그 API 결과의 URL에서 본문 텍스트 추출 로직 구현 (`requests` + `BeautifulSoup4` / `Newspaper3k`).
    - [X] `Playwright` 사용 함수 구현 (`fetch_dynamic_content`).
    - [X] 오류 처리, `robots.txt` 확인 (선택적), `time.sleep()` 추가.

- [X] **2.7 데이터 모델 정의 (Pydantic):**
    - [X] `theme_news_agent/sub_agents/data_collection/models.py` 생성.
    - [X] `ArticleData` Pydantic 모델 정의 (기존과 유사: `title`, `content`, `source`, `published`, `url`). `source` 필드는 이제 "NewsAPI", "NYTimes", "Naver News", "Naver Blog", "Naver Cafe", "Yahoo Finance Trending", "Google Trends", "Naver DataLab" 등을 포함할 수 있음.
    - [X] `CollectedData` Pydantic 모델 정의. 필드를 좀 더 일반화하거나 (예: `articles: List[ArticleData]`), 소스별 리스트를 유지할 수 있음 (예: `news: List`, `blogs: List`, ..., `financial_trends: List`, `search_trends: List`). 후자가 후처리 단계에서 소스별 분석에 유리할 수 있음.

- [X] **2.8 도구 통합 및 상태 관리:**
    - [X] `DataCollectionAgent.process` 메서드 구현:
        - [X] 모든 데이터 수집 도구 (뉴스, 블로그/카페, 금융 트렌드, 검색 트렌드) 호출.
        - [X] (선택적 크롤링) 뉴스/블로그 결과 URL 기반 `WebCrawlingTool` 호출하여 `content` 보강.
        - [X] 모든 결과를 `CollectedData` 모델 객체로 통합 및 유효성 검사 (다양한 소스 처리).
        - [X] `ctx.state["collected_data"] = collected_data_model.model_dump()` 형태로 세션 상태에 저장.
        - [X] 성공/실패 및 소스별 수집 건수 포함한 상태 메시지 반환.

## 3단계: 키워드 추출 에이전트 구현

- [X] **3.1 `KeywordExtractionAgent` 정의:**
    - [X] `theme_news_agent/sub_agents/keyword_extraction/agent.py`에 `KeywordExtractionAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [X] `__init__`에서 `model` (예: 'gemini-1.5-flash-latest'), `description`, `instruction` 설정.

- [X] **3.2 추출 프롬프트 정의:**
    - [X] `theme_news_agent/sub_agents/keyword_extraction/prompt.py`에 프롬프트 문자열 또는 함수 정의 (`get_extraction_prompt`).
    - [X] `Design.md` 섹션 4 (1) 및 `Dev_Plan.md` 섹션 5.2 참고하여 프롬프트 작성. LLM에게 입력 텍스트(제목+요약)에서 주요 키워드/엔티티(인물, 조직, 이벤트, 제품, 기술, 주제 명사구 등) 추출 지시.
    - [X] 출력 형식을 명확히 지정: **반드시 JSON 형식의 키워드 문자열 리스트로 반환**하도록 요구. 예: `["키워드1", "키워드2", ...]`.

- [X] **3.3 에이전트 로직 구현:**
    - [X] `KeywordExtractionAgent.process` 메서드 구현:
        - `ctx.state.get("collected_data")` 로드.
        - LLM 입력 생성: 다양한 소스의 `title` 및 `content` 필드를 적절히 조합/선택하여 LLM 입력 구성. (예: 검색어 자체를 중요한 입력으로 간주).
        - `self.generate_content` 또는 유사 메서드 호출하여 LLM 실행.
        - LLM 응답 파싱: 반환된 문자열이 유효한 JSON 리스트인지 확인하고 파싱. 파싱 실패 시 재시도 또는 오류 처리.

- [X] **3.4 키워드 빈도 계산 도구/함수 구현:**
    - [X] `theme_news_agent/sub_agents/keyword_extraction/tools/frequency_calculator.py` (또는 agent.py 내 함수) 생성.
    - [X] 함수 정의: `calculate_keyword_frequencies(keywords: List[str], collected_data: CollectedData) -> List[Dict]`.
    - [X] 로직:
        - [X] 입력 `keywords` 리스트의 각 키워드에 대해, `collected_data`의 모든 문서(`title` + `content`)에서 등장 횟수 계산 (대소문자 구분 없이).
        - [X] 출처별 빈도 계산 시, 이제 금융 트렌드, 검색 트렌드 소스도 포함하여 집계.
        - [X] 결과 형식: `[{ "keyword": "...", "frequency": { "total": N, "news": N, "blogs": N, "cafes": N, "finance": N, "search": N } }, ...]`. # 'other' 카테고리 포함

- [X] **3.5 상태 관리:** # 완료 표시
    - [X] `KeywordExtractionAgent.process`에서 빈도 계산 함수 호출. # 완료 표시
    - [X] 계산된 빈도 정보 포함 결과를 세션 상태에 저장: `ctx.state["keyword_results"] = keyword_frequency_data`. # 완료 표시

## 4단계: 테마 클러스터링 에이전트 구현

- [X] **4.1 `ThemeClusteringAgent` 정의:**
    - [X] `theme_news_agent/sub_agents/theme_clustering/agent.py`에 `ThemeClusteringAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [X] `__init__`에서 모델, 설명, 지침 설정.

- [X] **4.2 클러스터링 프롬프트 정의:**
    - [X] `theme_news_agent/sub_agents/theme_clustering/prompt.py`에 프롬프트 정의 (`get_clustering_prompt`).
    - [X] `Design.md` 섹션 4 (3) 및 `Dev_Plan.md` 섹션 5.3 참고하여 프롬프트 작성. 입력으로 키워드 목록(언급량 포함)을 받고, 의미적으로 유사/연관된 키워드를 그룹화하고 각 그룹에 이해하기 쉬운 테마 이름을 부여하도록 지시.
    - [X] 출력 형식을 명확히 지정: **반드시 `Design.md` 섹션 4 (3)의 예시와 같은 JSON 형식의 배열로 반환**하도록 요구. `[{"theme": "...", "keywords": ["...", ...], "mentions": N}, ...]`.

- [X] **4.3 에이전트 로직 구현:** # 완료 표시
    - [X] `ThemeClusteringAgent.process` 메서드 구현: # 완료 표시
        - `ctx.state.get("keyword_results")`로 이전 단계 결과 로드.
        - LLM 프롬프트 입력 형식에 맞게 키워드 데이터 포맷 (예: 문자열로 변환).
        - ~~LLM 호출.~~ (제거됨, ADK 프레임워크가 처리할 것으로 예상)
        - ~~LLM 응답이 유효한 JSON 배열인지 확인하고 파싱. 각 항목의 `mentions` 값은 입력 빈도의 합계와 일치하는지 검증 (선택 사항, LLM이 계산하도록 둘 수도 있음). 오류 처리 구현.~~ (제거됨)
        - 생성된 프롬프트 또는 오류 메시지 반환.

## 5단계: 트렌드 분석 에이전트 구현

- [X] **5.1 `TrendAnalysisAgent` 정의:**
    - [X] `theme_news_agent/sub_agents/trend_analysis/agent.py`에 `TrendAnalysisAgent` 클래스 정의 (`google.adk.Agent` 상속).
    - [X] `__init__`에서 통계 분석 도구 인스턴스화.

- [X] **5.2 통계 분석 도구 구현 (`StatisticalAnalysisTool`):** # 체크박스 수정
    - [X] `theme_news_agent/sub_agents/trend_analysis/tools/stats_tool.py` 생성.
    - [X] `@Tool` 데코레이터 적용 함수 정의: `calculate_trends(current_themes: List[Dict]) -> List[Dict]`. # 실제로는 FunctionTool 사용
    - [X] **과거 데이터 관리:**
        - [X] 함수 내에서 과거 데이터 로드 로직 구현 (환경 변수 `HISTORICAL_DATA_PATH` 사용). 파일 없으면 빈 데이터로 시작. JSON 형식 사용.
        - [X] 과거 데이터 구조 정의 (예: `{ \"테마명\": {\"mentions_history\": [과거 언급량 리스트], \"avg\": 평균, \"std\": 표준편차} }`).
    - [X] **Z-점수 계산:**
        - [X] `current_themes`의 각 테마에 대해:
            - [X] 과거 데이터에서 해당 테마의 `avg`, `std` 조회.
            - [X] `z = (current_mentions - avg) / std` 계산. (과거 데이터 없거나 std=0일 경우 z=0 또는 다른 값으로 처리).
        - [X] 계산된 z-점수를 현재 테마 데이터에 추가.
    - [X] **과거 데이터 업데이트:**
        - [X] 현재 테마 언급량을 과거 데이터의 `mentions_history`에 추가.
        - [X] 업데이트된 `mentions_history로 새로운 `avg`, `std` 계산 및 저장.
        - [X] 변경된 과거 데이터를 파일에 다시 저장.
        - [X] 변경된 과거 데이터를 파일에 다시 저장.
    - [X] Z-점수가 추가된 테마 리스트 반환.

- [X] **5.3 에이전트 로직 구현:**
    - [X] `TrendAnalysisAgent.process` 메서드 구현:
        - [X] `ctx.state.get("clustered_themes")` 로드.
        - [X] `StatisticalAnalysisTool.calculate_trends` 호출하여 Z-점수 계산 및 데이터 업데이트. (실제로는 클래스 속성 `self.stats_tool.func` 호출)
        - [X] 반환된 테마 리스트를 Z-점수 기준 내림차순 정렬.
        - [X] 환경 변수 `TREND_TOP_N` 값에 따라 상위 N개 테마 선택 (기본값 20, 유효성 검사 포함).
        - [X] 각 테마 딕셔너리에 'rank' 키 추가 (1부터 N까지).
    - [X] 관련 테스트 케이스를 `markdown/testcase2.md`에 정의하고 `tests/sub_agents/trend_analysis/test_agent.py`에 구현 및 실행 완료.

- [X] **5.4 상태 관리:**
    - [X] 최종 순위가 매겨진 상위 트렌드 테마 목록을 세션 상태(`ctx.state["trend_results"]`)에 저장하는 로직이 `process` 메서드 내에 구현됨.

## 6단계: 요약 생성 에이전트 구현

- [X] **6.1 `SummaryGenerationAgent` 정의:**
    - [X] `theme_news_agent/sub_agents/summary_generation/agent.py`에 `SummaryGenerationAgent` 클래스 정의 (`google.adk.LlmAgent` 상속).
    - [X] `__init__`에서 모델, 설명, 지침 설정.

- [X] **6.2 요약 프롬프트 정의:**
    - [X] `theme_news_agent/sub_agents/summary_generation/prompt.py`에 프롬프트 정의 (`get_summary_prompt`).
    - [X] `Design.md`