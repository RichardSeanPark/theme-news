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
