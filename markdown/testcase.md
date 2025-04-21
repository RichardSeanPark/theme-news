# 테스트 케이스

## 1.1. 프로젝트 디렉토리 구조 생성

### 1.1.1. 메인 에이전트 디렉토리 생성: `theme_news_agent/`

- [X]
*   **테스트 케이스 ID:** `test_main_agent_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 메인 에이전트 디렉토리 `theme_news_agent/`가 프로젝트 루트에 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  프로젝트 루트에 `theme_news_agent/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/` 디렉토리가 존재합니다.

#### 1.1.2. 핵심 파이썬 패키지 디렉토리 생성: `theme_news_agent/`

- [X]
*   **테스트 케이스 ID:** `test_package_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 파이썬 패키지 파일들(`__init__.py`, `agent.py`, `sub_agents/`)이 `theme_news_agent/` 내부에 직접 위치하는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `__init__.py`, `agent.py`, `sub_agents/` 가 존재하는지 확인합니다.
*   **예상 결과:** `__init__.py`, `agent.py`, `sub_agents/` 가 `theme_news_agent/` 내부에 존재합니다.

#### 1.1.3. `__init__.py` 파일 생성: `theme_news_agent/__init__.py`

- [X]
*   **테스트 케이스 ID:** `test_init_file_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 `__init__.py` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/__init__.py` 파일이 존재합니다.

#### 1.1.4. `agent.py` 파일 생성: `theme_news_agent/agent.py`

- [X]
*   **테스트 케이스 ID:** `test_agent_file_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 마스터 에이전트용 `agent.py` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `agent.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/agent.py` 파일이 존재합니다.

#### 1.1.5. `sub_agents/` 디렉토리 생성: `theme_news_agent/sub_agents/`

- [X]
*   **테스트 케이스 ID:** `test_sub_agents_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 `sub_agents/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `sub_agents/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/sub_agents/` 디렉토리가 존재합니다.

#### 1.1.6. 개별 하위 에이전트 디렉토리 생성

- [X]
*   **테스트 케이스 ID:** `test_specific_sub_agent_directories_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `sub_agents/` 내부에 개별 에이전트(`data_collection`, `keyword_extraction`, `theme_clustering`, `trend_analysis`, `summary_generation`) 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/sub_agents/` 디렉토리 내부에 `data_collection/` 디렉토리가 존재하는지 확인합니다.
    2.  `theme_news_agent/sub_agents/` 디렉토리 내부에 `keyword_extraction/` 디렉토리가 존재하는지 확인합니다.
    3.  `theme_news_agent/sub_agents/` 디렉토리 내부에 `theme_clustering/` 디렉토리가 존재하는지 확인합니다.
    4.  `theme_news_agent/sub_agents/` 디렉토리 내부에 `trend_analysis/` 디렉토리가 존재하는지 확인합니다.
    5.  `theme_news_agent/sub_agents/` 디렉토리 내부에 `summary_generation/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** 모든 개별 하위 에이전트 디렉토리가 존재합니다.

#### 1.1.7. 하위 에이전트 내부 파일/디렉토리 생성

- [X]
*   **테스트 케이스 ID:** `test_sub_agent_internal_files_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 각 하위 에이전트 디렉토리 내부에 필요한 `agent.py`, `prompt.py`, `tools/`가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `data_collection` 디렉토리 내부에 `agent.py` 파일과 `tools/` 디렉토리가 존재하는지 확인합니다.
    2.  `keyword_extraction` 디렉토리 내부에 `agent.py`와 `prompt.py` 파일이 존재하는지 확인합니다.
    3.  `theme_clustering` 디렉토리 내부에 `agent.py`와 `prompt.py` 파일이 존재하는지 확인합니다.
    4.  `trend_analysis` 디렉토리 내부에 `agent.py` 파일과 `tools/` 디렉토리가 존재하는지 확인합니다.
    5.  `summary_generation` 디렉토리 내부에 `agent.py`와 `prompt.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** 모든 필요한 파일 및 디렉토리가 각 하위 에이전트 디렉토리 내에 존재합니다.

#### 1.1.8. 하위 에이전트 `__init__.py` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_sub_agent_init_files_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `sub_agents` 디렉토리와 모든 하위 에이전트 디렉토리 내부에 `__init__.py` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/sub_agents/__init__.py` 파일이 존재하는지 확인합니다.
    2.  `data_collection` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
    3.  `keyword_extraction` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
    4.  `theme_clustering` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
    5.  `trend_analysis` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
    6.  `summary_generation` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** 모든 필요한 `__init__.py` 파일이 존재합니다.

#### 1.1.9. `deployment/` 디렉토리 생성: `theme_news_agent/deployment/`

- [X]
*   **테스트 케이스 ID:** `test_deployment_directory_creation`
*   **우선순위:** 중간
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 내부에 `deployment/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `deployment/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/deployment/` 디렉토리가 존재합니다.

#### 1.1.10. `eval/` 디렉토리 생성: `theme_news_agent/eval/`

- [X]
*   **테스트 케이스 ID:** `test_eval_directory_creation`
*   **우선순위:** 중간
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 내부에 `eval/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `eval/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/eval/` 디렉토리가 존재합니다.

#### 1.1.11. `tests/` 디렉토리 생성: `theme_news_agent/tests/`

- [X]
*   **테스트 케이스 ID:** `test_tests_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 내부에 `tests/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `tests/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/tests/` 디렉토리가 존재합니다.

## 1.2. 의존성 관리 초기화

### 1.2.1. `pyproject.toml` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_pyproject_toml_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `poetry init` 실행 후 `theme_news_agent/` 디렉토리 내부에 `pyproject.toml` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `pyproject.toml` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/pyproject.toml` 파일이 존재합니다.

### 1.2.2. 핵심 의존성 추가 확인

- [X]
*   **테스트 케이스 ID:** `test_core_dependencies_added`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `pyproject.toml` 파일에 핵심 의존성(`google-adk`, `requests`, `beautifulsoup4`, `playwright`, `newspaper3k`, `numpy`, `pandas`, `pydantic`, `python-dotenv`)이 포함되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/pyproject.toml` 파일을 로드합니다.
    2.  `[tool.poetry.dependencies]` 섹션에 명시된 모든 핵심 의존성이 존재하는지 확인합니다.
*   **예상 결과:** 모든 핵심 의존성이 `pyproject.toml` 파일에 명시되어 있습니다.

### 1.2.3. 개발 의존성 추가 확인 (pytest)

- [X]
*   **테스트 케이스 ID:** `test_dev_dependency_pytest_added`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `pyproject.toml` 파일의 `[tool.poetry.group.dev.dependencies]` 섹션에 `pytest`가 포함되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/pyproject.toml` 파일을 로드합니다.
    2.  `[tool.poetry.group.dev.dependencies]` 섹션에 `pytest`가 존재하는지 확인합니다.
*   **예상 결과:** `pytest` 의존성이 `pyproject.toml` 파일의 개발 그룹에 명시되어 있습니다.

### 1.2.4. `poetry.lock` 파일 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_poetry_lock_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `poetry install` 실행 후 `theme_news_agent/` 디렉토리 내부에 `poetry.lock` 파일이 성공적으로 생성/업데이트되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `poetry.lock` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/poetry.lock` 파일이 존재합니다.

## 1.3. 환경 변수 구성

### 1.3.1. `.env.example` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_env_example_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `.env.example` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `.env.example` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/.env.example` 파일이 존재합니다.

### 1.3.2. `.env` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_env_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `.env` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `.env` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/.env` 파일이 존재합니다.

### 1.3.3. `.gitignore`에 `.env` 추가 확인

- [X]
*   **테스트 케이스 ID:** `test_env_ignored`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `.gitignore` 파일에 `.env` 경로가 포함되어 Git 추적에서 제외되는지 확인합니다. (경로 수정됨)
*   **단계:**
    1.  `git check-ignore .env` 명령을 실행합니다. (경로 수정됨)
    2.  명령어가 성공적으로 실행되고 해당 경로를 출력하는지 확인합니다.
*   **예상 결과:** `git check-ignore` 명령이 성공하고 `.env`를 출력합니다. (경로 수정됨)

## 1.4. 기본 프로젝트 파일

### 1.4.1. `theme_news_agent/README.md` 파일 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_agent_readme_creation`
*   **우선순위:** 중간
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `README.md` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `README.md` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/README.md` 파일이 존재합니다.

### 1.4.2. `theme_news_agent/data/` 디렉토리 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_agent_data_directory_creation`
*   **우선순위:** 중간
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `data/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `data/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/data/` 디렉토리가 존재합니다.

### 1.4.3. `.gitignore`에 `data/` 추가 확인

- [X]
*   **테스트 케이스 ID:** `test_data_dir_ignored`
*   **우선순위:** 중간
*   **유형:** 기능 테스트
*   **설명:** `.gitignore` 파일에 `theme_news_agent/data/` 경로가 포함되어 Git 추적에서 제외되는지 확인합니다.
*   **단계:**
    1.  `git check-ignore theme_news_agent/data/` 명령을 실행합니다.
    2.  명령어가 성공적으로 실행되고 해당 경로를 출력하는지 확인합니다.
*   **예상 결과:** `git check-ignore` 명령이 성공하고 `theme_news_agent/data/`를 출력합니다.

## 2.1. DataCollectionAgent 정의

### 2.1.1. `DataCollectionAgent` 클래스 존재 및 상속 확인

- [X]
*   **테스트 케이스 ID:** `test_data_collection_agent_definition`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `theme_news_agent.sub_agents.data_collection.agent` 모듈에 `DataCollectionAgent` 클래스가 정의되어 있고, `google.adk.Agent`를 상속하는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent.sub_agents.data_collection.agent` 모듈을 임포트합니다.
    2.  `DataCollectionAgent` 클래스가 해당 모듈에 존재하는지 확인합니다.
    3.  `DataCollectionAgent` 클래스가 `google.adk.Agent`의 서브클래스인지 확인합니다.
*   **예상 결과:** 클래스가 존재하고 `google.adk.Agent`를 상속합니다.

### 2.1.2. `DataCollectionAgent` 인스턴스 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_data_collection_agent_instantiation`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `DataCollectionAgent` 클래스의 인스턴스를 성공적으로 생성할 수 있는지 확인합니다.
*   **단계:**
    1.  `DataCollectionAgent()`를 호출하여 인스턴스를 생성합니다.
*   **예상 결과:** 오류 없이 인스턴스가 생성됩니다.

## 2.2. 뉴스 API 도구 구현 (`NewsApiTool`)

### 2.2.1. `fetch_newsapi_headlines` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_newsapi_headlines_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_newsapi_headlines` 함수가 유효한 API 키로 실제 NewsAPI를 호출했을 때 예외 없이 리스트를 반환하는지 확인합니다. (주의: 유효한 `NEWS_API_KEY` 환경 변수 및 네트워크 연결 필요)
*   **단계:**
    1.  유효한 `NEWS_API_KEY` 환경 변수를 설정합니다.
    2.  `fetch_newsapi_headlines` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
*   **예상 결과:** 예외 없이 리스트를 반환합니다. (반환되는 리스트의 내용은 API 응답에 따라 달라질 수 있음)

### 2.2.2. `fetch_nytimes_articles` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_nytimes_articles_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_nytimes_articles` 함수가 유효한 API 키로 실제 NYTimes API를 호출했을 때 예외 없이 리스트를 반환하는지 확인합니다. (주의: 유효한 `NYT_API_KEY` 환경 변수 및 네트워크 연결 필요)
*   **단계:**
    1.  유효한 `NYT_API_KEY` 환경 변수를 설정합니다.
    2.  `fetch_nytimes_articles` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
*   **예상 결과:** 예외 없이 리스트를 반환합니다. (반환되는 리스트의 내용은 API 응답에 따라 달라질 수 있음)

### 2.2.3. `fetch_naver_news` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_naver_news_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_naver_news` 함수가 유효한 API 키로 실제 Naver News API를 호출했을 때 예외 없이 리스트를 반환하는지 확인합니다. (주의: 유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수 및 네트워크 연결 필요)
*   **단계:**
    1.  유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수를 설정합니다.
    2.  `fetch_naver_news` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
    5.  (선택적) 반환된 리스트의 각 항목에서 HTML 태그가 제거되었는지 샘플 확인합니다.
*   **예상 결과:** 예외 없이 리스트를 반환합니다. (반환되는 리스트의 내용은 API 응답에 따라 달라질 수 있음)

### 2.2.4. API 키 누락 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_news_api_key_missing`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** 각 뉴스 API 함수가 관련 API 키 환경 변수가 설정되지 않았을 때 빈 리스트를 반환하고 오류 메시지를 출력하는지 확인합니다.
*   **단계:**
    1.  각 API 함수에 필요한 환경 변수를 설정하지 않습니다 (또는 None으로 설정).
    2.  각 함수(`fetch_newsapi_headlines`, `fetch_nytimes_articles`, `fetch_naver_news`)를 호출합니다.
    3.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    4.  표준 출력(stdout)에 해당 키 누락 오류 메시지가 출력되었는지 확인합니다.
*   **예상 결과:** 모든 함수가 빈 리스트를 반환하고, 적절한 오류 메시지를 출력합니다.

### 2.2.5. API 호출 실패 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_news_api_call_failure`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 각 뉴스 API 함수가 API 호출 중 오류(예: `requests.exceptions.RequestException`) 발생 시 빈 리스트를 반환하고 오류 메시지를 출력하는지 확인합니다.
*   **단계:**
    1.  `requests.get` 함수를 모킹하여 `requests.exceptions.RequestException` 예외를 발생시키도록 설정합니다.
    2.  각 API 함수에 필요한 환경 변수를 설정합니다.
    3.  각 함수(`fetch_newsapi_headlines`, `fetch_nytimes_articles`, `fetch_naver_news`)를 호출합니다.
    4.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    5.  표준 출력(stdout)에 API 호출 오류 메시지가 출력되었는지 확인합니다.
*   **예상 결과:** 모든 함수가 빈 리스트를 반환하고, 적절한 오류 메시지를 출력합니다.

## 2.3. 블로그/카페 검색 API 도구 구현 (`BlogCafeApiTool`)

### 2.3.1. `fetch_naver_blogs` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_naver_blogs_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_naver_blogs` 함수가 유효한 API 키로 실제 Naver Blog API를 호출했을 때 예외 없이 리스트를 반환하는지 확인합니다. (주의: 유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수 및 네트워크 연결 필요)
*   **단계:**
    1.  유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수를 설정합니다.
    2.  `fetch_naver_blogs` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
    5.  (선택적) 반환된 리스트의 각 항목에서 HTML 태그가 제거되었는지 샘플 확인합니다.
*   **예상 결과:** 예외 없이 리스트를 반환합니다. (반환되는 리스트의 내용은 API 응답에 따라 달라질 수 있음)

### 2.3.2. `fetch_naver_cafe_articles` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_naver_cafe_articles_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_naver_cafe_articles` 함수가 유효한 API 키로 실제 Naver Cafe API를 호출했을 때 예외 없이 리스트를 반환하는지 확인합니다. (주의: 유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수 및 네트워크 연결 필요)
*   **단계:**
    1.  유효한 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수를 설정합니다.
    2.  `fetch_naver_cafe_articles` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
    5.  (선택적) 반환된 리스트의 각 항목에서 HTML 태그가 제거되었는지 샘플 확인합니다.
*   **예상 결과:** 예외 없이 리스트를 반환합니다. (반환되는 리스트의 내용은 API 응답에 따라 달라질 수 있음)

### 2.3.3. API 키 누락 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_blog_cafe_api_key_missing`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `fetch_naver_blogs` 및 `fetch_naver_cafe_articles` 함수가 `NAVER_CLIENT_ID` 또는 `NAVER_CLIENT_SECRET` 환경 변수가 설정되지 않았을 때 빈 리스트를 반환하고 오류 메시지를 출력하는지 확인합니다.
*   **단계:**
    1.  `NAVER_CLIENT_ID` 또는 `NAVER_CLIENT_SECRET` 환경 변수를 설정하지 않습니다 (또는 None으로 설정).
    2.  `fetch_naver_blogs` 함수를 호출합니다.
    3.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    4.  표준 출력(stdout)에 해당 키 누락 오류 메시지가 출력되었는지 확인합니다.
    5.  `fetch_naver_cafe_articles` 함수를 호출합니다.
    6.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    7.  표준 출력(stdout)에 해당 키 누락 오류 메시지가 출력되었는지 확인합니다.
*   **예상 결과:** 두 함수 모두 빈 리스트를 반환하고, 적절한 오류 메시지를 출력합니다.

### 2.3.4. API 호출 실패 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_blog_cafe_api_call_failure`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `fetch_naver_blogs` 및 `fetch_naver_cafe_articles` 함수가 API 호출 중 오류(예: `requests.exceptions.RequestException`) 발생 시 빈 리스트를 반환하고 오류 메시지를 출력하는지 확인합니다.
*   **단계:**
    1.  `requests.get` 함수를 모킹하여 `requests.exceptions.RequestException` 예외를 발생시키도록 설정합니다.
    2.  `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 환경 변수를 설정합니다.
    3.  `fetch_naver_blogs` 함수를 호출합니다.
    4.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    5.  표준 출력(stdout)에 API 호출 오류 메시지가 출력되었는지 확인합니다.
    6.  `fetch_naver_cafe_articles` 함수를 호출합니다.
    7.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    8.  표준 출력(stdout)에 API 호출 오류 메시지가 출력되었는지 확인합니다.
*   **예상 결과:** 두 함수 모두 빈 리스트를 반환하고, 적절한 오류 메시지를 출력합니다.

## 2.4. 금융 트렌드 도구 구현 (`FinancialTrendTool`)

### 2.4.1. `fetch_trending_tickers` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_trending_tickers_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live Web with Playwright)
*   **설명:** `fetch_trending_tickers` 함수가 Playwright를 사용하여 Yahoo Finance 웹사이트를 성공적으로 스크래핑하고 예외 없이 티커 정보 딕셔너리 리스트를 반환하는지 확인합니다. (주의: 네트워크 연결, Playwright 바이너리 설치, Yahoo Finance 웹사이트 구조 의존성 있음)
*   **단계:**
    1.  (필요시) `playwright install` 실행.
    2.  `fetch_trending_tickers` 함수를 호출합니다.
    3.  반환값이 리스트(`list`) 타입인지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
    5.  (선택적) 리스트가 비어있지 않다면, 첫 번째 항목이 예상된 키(`title`, `content`, `source`, `published`, `url`)를 포함하는지 확인합니다.
*   **예상 결과:** 예외 없이 티커 정보 딕셔너리 리스트를 반환합니다. (사이트 상태에 따라 빈 리스트일 수 있음)

### 2.4.2. 스크래핑 실패 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_trending_tickers_scraping_failure`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** Yahoo Finance 웹사이트 구조 변경 등으로 인해 스크래핑 대상 요소를 찾지 못했을 때, 함수가 빈 리스트를 반환하고 경고 로그를 남기는지 확인합니다.
*   **단계:**
    1.  (모킹 사용 시) `playwright`의 `page.content()`는 정상적인 HTML을 반환하지만, `BeautifulSoup`의 `find` 또는 `find_all` 메서드가 `None` 또는 빈 리스트를 반환하도록 모킹합니다.
    2.  `fetch_trending_tickers` 함수를 호출합니다.
    3.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    4.  로그 출력에 "Could not find..." 또는 "Found trending tickers section, but no ticker links inside..." 같은 경고 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 빈 리스트를 반환하고, 적절한 경고 로그 메시지를 출력합니다.

### 2.4.3. 네트워크 오류 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_trending_tickers_network_error`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** Playwright로 Yahoo Finance 웹사이트 접근 중 네트워크 오류(`PlaywrightError`) 발생 시, 함수가 빈 리스트를 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `playwright.sync_api._generated.Page.goto` 함수를 모킹하여 `PlaywrightError` 예외를 발생시키도록 설정합니다.
    2.  `fetch_trending_tickers` 함수를 호출합니다.
    3.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    4.  로그 출력에 "Playwright error fetching Yahoo Finance..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 빈 리스트를 반환하고, 적절한 오류 로그 메시지를 출력합니다.

## 2.5. 검색 트렌드 도구 구현 (`SearchTrendTool`)

### 2.5.1. `fetch_google_trends` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_google_trends_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live API)
*   **설명:** `fetch_google_trends` 함수가 `pytrends` 라이브러리를 사용하여 실제 Google Trends API를 호출하고 예외 없이 검색어 정보 딕셔너리 리스트를 반환하는지 확인합니다. (주의: 네트워크 연결 필요)
*   **단계:**
    1.  `fetch_google_trends` 함수를 호출합니다 (예: `region='KR'`).
    2.  반환값이 리스트(`list`) 타입인지 확인합니다.
    3.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
    4.  (선택적) 리스트가 비어있지 않다면, 첫 번째 항목이 예상된 키(`title`, `content`, `source`, `published`, `url`)를 포함하고 `source`가 올바른지 확인합니다.
*   **예상 결과:** 예외 없이 검색어 정보 딕셔너리 리스트를 반환합니다. (트렌드 유무에 따라 빈 리스트일 수 있음)

### 2.5.2. `pytrends` 라이브러리 오류 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_google_trends_pytrends_error`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `pytrends` 라이브러리 함수(`trending_searches`) 호출 중 예외 발생 시, 함수가 빈 리스트를 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `pytrends.request.TrendReq.trending_searches` 메서드를 모킹하여 `Exception`을 발생시키도록 설정합니다.
    2.  `fetch_google_trends` 함수를 호출합니다.
    3.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    4.  로그 출력에 "Error fetching Google Trends..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 빈 리스트를 반환하고, 적절한 오류 로그 메시지를 출력합니다.

### 2.5.3. `fetch_naver_datalab_trends` 플레이스홀더 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_naver_datalab_trends_placeholder`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** `fetch_naver_datalab_trends` 함수가 현재 구현되지 않았으므로, 호출 시 빈 리스트를 반환하고 경고 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `fetch_naver_datalab_trends` 함수를 호출합니다.
    2.  반환값이 빈 리스트(`[]`)인지 확인합니다.
    3.  로그 출력에 "fetch_naver_datalab_trends_func is not implemented yet." 경고 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 빈 리스트를 반환하고, 경고 로그 메시지를 출력합니다.

## 2.6. 웹 크롤링 도구 구현 (`WebCrawlingTool`)

### 2.6.1. `fetch_full_content` 성공 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_success`
*   **우선순위:** 높음
*   **유형:** 통합 테스트 (Live Web)
*   **설명:** `fetch_full_content` 함수가 유효한 기사 URL을 입력받아 `newspaper3k`를 사용하여 실제 웹 페이지에서 본문 텍스트를 성공적으로 추출하여 문자열을 반환하는지 확인합니다. (주의: 네트워크 연결 및 대상 웹사이트 상태에 의존)
*   **단계:**
    1.  실제 존재하는 기사의 URL을 준비합니다.
    2.  `fetch_full_content` 함수에 해당 URL을 전달하여 호출합니다.
    3.  반환값이 문자열(`str`) 타입이고 내용이 비어있지 않은지 확인합니다.
    4.  함수 호출 중 예외가 발생하지 않았는지 확인합니다.
*   **예상 결과:** 추출된 본문 텍스트 문자열을 반환합니다.

### 2.6.2. `newspaper3k` 라이브러리 오류 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_newspaper_error`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `newspaper3k`의 `Article.download()` 또는 `Article.parse()` 메서드 실행 중 `ArticleException` 발생 시, 함수가 `None`을 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `newspaper.Article` 객체의 `download` 또는 `parse` 메서드를 모킹하여 `ArticleException`을 발생시키도록 설정합니다.
    2.  유효한 형식의 URL로 `fetch_full_content` 함수를 호출합니다.
    3.  반환값이 `None`인지 확인합니다.
    4.  로그 출력에 "Newspaper3k error processing URL..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** `None`을 반환하고, 적절한 오류 로그 메시지를 출력합니다.

### 2.6.3. 내용 추출 실패 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_extraction_failure`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `newspaper3k`가 페이지 다운로드 및 파싱은 성공했지만 `article.text` 속성이 비어있는 경우, 함수가 `None`을 반환하고 경고 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `newspaper.Article` 객체를 모킹하여 `download`와 `parse` 메서드는 성공적으로 호출되지만, `text` 속성이 빈 문자열(`""`)을 반환하도록 설정합니다.
    2.  유효한 형식의 URL로 `fetch_full_content` 함수를 호출합니다.
    3.  반환값이 `None`인지 확인합니다.
    4.  로그 출력에 "Could not extract main text content..." 같은 경고 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** `None`을 반환하고, 적절한 경고 로그 메시지를 출력합니다.

### 2.6.4. 잘못된 URL 입력 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_invalid_url`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `fetch_full_content` 함수에 유효하지 않은 형식의 URL(예: http/https 없음, None, 빈 문자열)이 입력되었을 때, `None`을 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  유효하지 않은 URL 값들(예: "example.com", "", None)을 준비합니다.
    2.  각각의 값으로 `fetch_full_content` 함수를 호출합니다.
    3.  모든 호출에 대해 반환값이 `None`인지 확인합니다.
    4.  로그 출력에 "Invalid URL provided..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 모든 잘못된 입력에 대해 `None`을 반환하고, 적절한 오류 로그 메시지를 출력합니다.

### 2.6.5. `fetch_full_content` 타임아웃 테스트 (모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_timeout`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `newspaper3k`의 `Article` 객체 생성 또는 `download` 시 타임아웃 관련 예외(`requests.exceptions.Timeout` 등) 발생 시, 함수가 `None`을 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `newspaper.Article` 생성자 또는 `download` 메서드를 모킹하여 `requests.exceptions.Timeout` (또는 유사 예외)를 발생시키도록 설정합니다.
    2.  유효한 형식의 URL로 `fetch_full_content_func`를 호출합니다.
    3.  반환값이 `None`인지 확인합니다.
    4.  로그 출력에 타임아웃 관련 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 빈 리스트를 반환하고, 타임아웃 관련 오류 로그를 출력합니다.

### 2.6.6. `fetch_full_content` 요청 간 지연 테스트 (모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_full_content_delay`
*   **우선순위:** 낮음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `fetch_full_content_func`가 성공적으로 내용을 추출하고 반환하기 직전에 `time.sleep`이 설정된 `DEFAULT_WAIT_TIME`만큼 호출되는지 확인합니다.
*   **단계:**
    1.  `time.sleep` 함수를 모킹합니다.
    2.  `newspaper.Article` 객체를 모킹하여 정상적으로 텍스트를 반환하도록 설정합니다.
    3.  유효한 URL로 `fetch_full_content_func`를 호출합니다.
    4.  함수가 성공적으로 텍스트를 반환하는지 확인합니다.
    5.  모킹된 `time.sleep` 함수가 `web_crawling_tool.DEFAULT_WAIT_TIME` 값으로 한 번 호출되었는지 확인합니다.
*   **예상 결과:** 함수는 텍스트를 반환하고, `time.sleep`이 정확한 인수로 호출됩니다.

### 2.6.7. `fetch_dynamic_content` 성공 테스트 (JS 필요, 모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_dynamic_content_success_js_mocked`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `fetch_dynamic_content_func` 함수가 JavaScript 렌더링이 필요한 URL 입력 시, Playwright 관련 객체들(browser, page)이 정상적으로 생성 및 호출되고, `page.inner_text('body')`가 예상된 내용을 반환하며, 최종적으로 해당 내용이 반환되는지 확인합니다. (Playwright 완전 모킹)
*   **단계:**
    1.  `playwright.sync_api.sync_playwright` 컨텍스트 매니저와 그 내부 객체들(`Browser`, `Page`)의 주요 메서드(`launch`, `new_page`, `goto`, `wait_for_load_state`, `inner_text`, `close`)를 모두 모킹합니다.
    2.  `page.inner_text('body')`가 특정 테스트 문자열을 반환하도록 설정합니다.
    3.  JavaScript 렌더링이 필요한 URL 형식으로 `fetch_dynamic_content_func`를 호출합니다.
    4.  반환값이 모킹된 `inner_text`와 일치하는지 확인합니다.
    5.  모킹된 Playwright 메서드들이 예상대로 호출되었는지 확인합니다 (예: `browser.close()` 호출 확인).
*   **예상 결과:** 모킹된 본문 텍스트를 반환하고, Playwright 객체들이 순서대로 사용됩니다.

### 2.6.8. `fetch_dynamic_content` 잘못된 URL 테스트

- [X]
*   **테스트 케이스 ID:** `test_fetch_dynamic_content_invalid_url`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `fetch_dynamic_content_func` 함수에 유효하지 않은 형식의 URL이 입력되었을 때, Playwright 관련 로직을 실행하지 않고 즉시 `None`을 반환하며 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  유효하지 않은 URL 값들(예: "example.com", "", None)을 준비합니다.
    2.  `playwright.sync_api.sync_playwright`를 모킹하여 호출되지 않음을 검증할 수 있도록 합니다.
    3.  각각의 값으로 `fetch_dynamic_content_func` 함수를 호출합니다.
    4.  모든 호출에 대해 반환값이 `None`인지 확인합니다.
    5.  로그 출력에 "Invalid URL format..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
    6.  모킹된 `sync_playwright`가 호출되지 않았는지 확인합니다.
*   **예상 결과:** 모든 잘못된 입력에 대해 `None`을 반환하고, 적절한 오류 로그를 출력하며, Playwright 로직은 실행되지 않습니다.

### 2.6.9. `fetch_dynamic_content` Playwright 타임아웃 테스트 (모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_dynamic_content_playwright_timeout`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** Playwright의 `page.goto` 또는 `page.wait_for_load_state` 등에서 `PlaywrightTimeoutError` 발생 시, 함수가 `None`을 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `playwright` 관련 객체들을 모킹하고, `page.goto` 또는 `wait_for_load_state` 등에서 `PlaywrightTimeoutError`를 발생시키도록 설정합니다.
    2.  유효한 형식의 URL로 `fetch_dynamic_content_func`를 호출합니다.
    3.  반환값이 `None`인지 확인합니다.
    4.  로그 출력에 "Playwright timeout error..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** `None`을 반환하고, 타임아웃 관련 오류 로그를 출력합니다.

### 2.6.10. `fetch_dynamic_content` Playwright 일반 오류 테스트 (모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_dynamic_content_playwright_error`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** Playwright 작업 중 일반적인 `PlaywrightError` (타임아웃 제외) 발생 시, 함수가 `None`을 반환하고 오류 로그를 남기는지 확인합니다.
*   **단계:**
    1.  `playwright` 관련 객체들을 모킹하고, 특정 메서드(예: `inner_text`) 호출 시 `PlaywrightError`를 발생시키도록 설정합니다.
    2.  유효한 형식의 URL로 `fetch_dynamic_content_func`를 호출합니다.
    3.  반환값이 `None`인지 확인합니다.
    4.  로그 출력에 "Playwright error processing URL..." 같은 오류 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** `None`을 반환하고, 일반 Playwright 오류 로그를 출력합니다.

### 2.6.11. `fetch_dynamic_content` 요청 간 지연 테스트 (모킹)

- [X]
*   **테스트 케이스 ID:** `test_fetch_dynamic_content_delay`
*   **우선순위:** 낮음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `fetch_dynamic_content_func`가 성공적으로 내용을 추출하고 반환하기 직전에 `time.sleep`이 설정된 `DEFAULT_WAIT_TIME`만큼 호출되는지 확인합니다.
*   **단계:**
    1.  `time.sleep` 함수를 모킹합니다.
    2.  `playwright` 관련 객체들을 모킹하여 정상적으로 텍스트를 반환하도록 설정합니다.
    3.  유효한 URL로 `fetch_dynamic_content_func`를 호출합니다.
    4.  함수가 성공적으로 텍스트를 반환하는지 확인합니다.
    5.  모킹된 `time.sleep` 함수가 `web_crawling_tool.DEFAULT_WAIT_TIME` 값으로 한 번 호출되었는지 확인합니다.
*   **예상 결과:** 함수는 텍스트를 반환하고, `time.sleep`이 정확한 인수로 호출됩니다.

## 2.7 데이터 모델 정의 (Pydantic)

### `ArticleData` 모델
- [X] **정상 데이터 생성**: 필수 필드(`title`, `source`)와 선택 필드(`content`, `published`, `url`)를 포함한 유효한 데이터로 `ArticleData` 인스턴스를 성공적으로 생성하는지 확인합니다.
- [X] **필수 필드 누락**: `title` 또는 `source`가 누락된 데이터로 인스턴스 생성 시 `ValidationError` 발생하는지 확인합니다.
- [X] **URL 유효성 검사**: 유효하지 않은 형식의 `url` 값(예: "htp://invalid") 입력 시 `ValidationError` 발생하는지 확인합니다.
- [X] **`published` 날짜 파싱 (ISO 8601)**: ISO 8601 형식의 문자열(`"2024-01-01T12:00:00Z"`)이 `datetime` 객체로 올바르게 파싱되는지 확인합니다.
- [X] **`published` 날짜 파싱 (datetime 객체)**: 이미 `datetime` 객체인 값이 그대로 유지되는지 확인합니다.
- [X] **`published` 날짜 파싱 (None)**: `None` 값이 그대로 `None`으로 유지되는지 확인합니다.
- [X] **`published` 날짜 파싱 (잘못된 형식)**: 파싱할 수 없는 문자열(예: "invalid date") 또는 잘못된 타입(예: 123) 입력 시 `None`으로 처리되고 경고 로그가 발생하는지 확인합니다.

### `CollectedData` 모델
- [X] **기본 인스턴스 생성**: 아무 데이터 없이 `CollectedData()` 호출 시, 모든 필드가 빈 리스트(`[]`)인 인스턴스가 성공적으로 생성되는지 확인합니다.
- [X] **데이터 추가 및 확인**: 각 소스별 필드(예: `newsapi_articles`)에 `ArticleData` 인스턴스 리스트를 할당하고, 해당 필드에 데이터가 올바르게 저장되는지 확인합니다.
- [X] **`get_all_articles` 메서드**: 여러 소스에 데이터가 포함된 `CollectedData` 인스턴스에서 `get_all_articles()` 메서드 호출 시, 모든 소스의 `ArticleData`가 포함된 단일 리스트를 올바르게 반환하는지 확인합니다.
- [X] **`log_summary` 메서드**: `CollectedData` 인스턴스에서 `log_summary()` 메서드 호출 시, 각 소스별 항목 수와 총 항목 수가 포함된 요약 정보가 INFO 레벨로 로깅되는지 확인합니다 (로그 캡처 필요).

## 2.8. 도구 통합 및 상태 관리 (`DataCollectionAgent.process`)

### 2.8.1. 모든 데이터 수집 도구 호출 및 결과 통합

- [X] # 체크 완료
*   **테스트 케이스 ID:** `test_data_collection_process_integration`
*   **우선순위:** 높음
*   **유형:** 통합 테스트
*   **설명:** `DataCollectionAgent.process` 메서드가 각 데이터 수집 도구(News, Blog/Cafe, Financial, Search)를 올바르게 호출하고, 반환된 데이터를 `CollectedData` 모델로 통합하여 `ctx.state`에 저장하는지 확인합니다. (선택적 크롤링은 이 테스트에서 제외)
*   **단계:**
    1.  `DataCollectionAgent` 인스턴스를 생성합니다.
    2.  `NewsApiTool`, `BlogCafeApiTool`, `FinancialTrendTool`, `SearchTrendTool`의 각 fetch 메서드들을 모킹(mock)합니다. 각 모킹된 메서드는 미리 정의된 **딕셔너리** 리스트를 반환하도록 설정합니다. # 수정: 객체 -> 딕셔너리
    3.  `google.adk.agents.invocation_context.InvocationContext` 객체를 모킹합니다. (초기 `state`는 비어 있음) # 수정: Context -> InvocationContext
    4.  `agent.process(ctx)`를 호출합니다.
    5.  각 모킹된 도구 메서드가 한 번씩 호출되었는지 확인합니다.
    6.  `ctx.state["collected_data"]`가 존재하는지 확인합니다.
    7.  `ctx.state["collected_data"]`의 값이 `CollectedData` 모델의 구조와 일치하고, 각 소스별로 모킹된 데이터가 올바르게 포함되었는지 확인합니다.
    8.  반환된 상태 메시지에 각 소스별 수집 건수가 올바르게 포함되었는지 확인합니다.
*   **예상 결과:**
    - 모든 모킹된 도구 메서드가 호출됩니다.
    - `ctx.state["collected_data"]`에 모든 소스의 모킹 데이터가 포함된 `CollectedData` 딕셔너리가 저장됩니다.
    - 반환된 상태 메시지가 예상된 형식과 수집 건수를 포함합니다.

### 2.8.2. 개별 도구 호출 시 오류 처리

- [X] # 체크 완료
*   **테스트 케이스 ID:** `test_data_collection_process_error_handling`
*   **우선순위:** 높음
*   **유형:** 예외 처리 테스트
*   **설명:** 특정 데이터 수집 도구 호출 시 예외가 발생했을 때, `process` 메서드가 오류를 적절히 처리하고 상태 메시지에 오류 정보를 포함하여 반환하는지 확인합니다.
*   **단계:**
    1.  `DataCollectionAgent` 인스턴스를 생성합니다.
    2.  `NewsApiTool`의 fetch 메서드 중 하나가 `Exception`을 발생시키도록 모킹합니다.
    3.  다른 도구들의 메서드는 정상적으로 **딕셔너리** 리스트를 반환하도록 모킹합니다. # 수정: 객체 -> 딕셔너리
    4.  `InvocationContext` 객체를 모킹합니다. # 수정: Context -> InvocationContext
    5.  `agent.process(ctx)`를 호출합니다.
    6.  `ctx.state["collected_data"]`에 오류가 발생하지 않은 소스의 데이터가 포함되어 있는지 확인합니다.
    7.  반환된 상태 메시지에 "오류 발생" 문구와 함께 예외가 발생한 소스("newsapi" 등) 및 오류 정보가 포함되어 있는지 확인합니다. # 수정: 소스 이름 구체화
*   **예상 결과:**
    - `process` 메서드가 예외를 일으키지 않고 정상적으로 완료됩니다.
    - `ctx.state["collected_data"]`에 정상 수집된 데이터가 저장됩니다.
    - 반환된 상태 메시지에 오류 발생 정보가 포함됩니다.

### 2.8.3. 선택적 웹 크롤링 로직 (구현 시)

- [X] # 체크 완료
*   **테스트 케이스 ID:** `test_data_collection_process_optional_crawling`
*   **우선순위:** 중간
*   **유형:** 통합 테스트
*   **설명:** (선택적 웹 크롤링 로직이 구현된 경우) `process` 메서드가 URL은 있지만 `content`가 비어있는 데이터(딕셔너리)에 대해 `WebCrawlingTool.fetch_full_content`를 호출하고 결과를 업데이트하는지 확인합니다.
*   **단계:**
    1.  `DataCollectionAgent` 인스턴스를 생성합니다.
    2.  뉴스/블로그 도구의 fetch 메서드를 모킹하여 `url`은 있지만 `content`는 비어있는 **딕셔너리**를 반환하도록 설정합니다. # 수정: 객체 -> 딕셔너리
    3.  `WebCrawlingTool.fetch_full_content` 메서드를 모킹하여 특정 URL에 대해 본문 텍스트를 반환하도록 설정합니다.
    4.  `InvocationContext` 객체를 모킹합니다. # 수정: Context -> InvocationContext
    5.  `agent.process(ctx)`를 호출합니다.
    6.  모킹된 `WebCrawlingTool.fetch_full_content`가 예상된 URL로 호출되었는지 확인합니다.
    7.  `ctx.state["collected_data"]` 내 해당 데이터의 `content` 필드가 크롤링 결과로 업데이트되었는지 확인합니다. (모델 객체로 로드 후 확인)
*   **예상 결과:**
    - `WebCrawlingTool.fetch_full_content`가 호출됩니다.
    - `ctx.state["collected_data"]` 내 해당 항목의 `content`가 업데이트됩니다.
