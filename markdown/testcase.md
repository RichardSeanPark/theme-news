# 테스트 케이스

## 1. 프로젝트 설정

### 1.1. 프로젝트 구조 초기화

#### 1.1.1. 메인 에이전트 디렉토리 생성: `theme_news_agent/`

- [X]
*   **테스트 케이스 ID:** `test_main_agent_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 메인 에이전트 디렉토리 `theme_news_agent/`가 프로젝트 루트에 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  프로젝트 루트에 `theme_news_agent/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/` 디렉토리가 존재합니다.

#### 1.1.2. 핵심 파이썬 패키지 디렉토리 생성: `theme_news_agent/theme_news_agent/`

- [X]
*   **테스트 케이스 ID:** `test_package_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 파이썬 패키지 디렉토리 `theme_news_agent/theme_news_agent/`가 `theme_news_agent/` 내부에 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `theme_news_agent/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/theme_news_agent/` 디렉토리가 존재합니다.

#### 1.1.3. `__init__.py` 파일 생성: `theme_news_agent/theme_news_agent/__init__.py`

- [X]
*   **테스트 케이스 ID:** `test_init_file_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 `__init__.py` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/theme_news_agent/` 디렉토리 내부에 `__init__.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/theme_news_agent/__init__.py` 파일이 존재합니다.

#### 1.1.4. `agent.py` 파일 생성: `theme_news_agent/theme_news_agent/agent.py`

- [X]
*   **테스트 케이스 ID:** `test_agent_file_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 마스터 에이전트용 `agent.py` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/theme_news_agent/` 디렉토리 내부에 `agent.py` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/theme_news_agent/agent.py` 파일이 존재합니다.

#### 1.1.5. `sub_agents/` 디렉토리 생성: `theme_news_agent/theme_news_agent/sub_agents/`

- [X]
*   **테스트 케이스 ID:** `test_sub_agents_directory_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** 핵심 패키지 디렉토리 내에 `sub_agents/` 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/theme_news_agent/` 디렉토리 내부에 `sub_agents/` 디렉토리가 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리가 존재합니다.

#### 1.1.6. 개별 하위 에이전트 디렉토리 생성

- [X]
*   **테스트 케이스 ID:** `test_specific_sub_agent_directories_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `sub_agents/` 내부에 개별 에이전트(`data_collection`, `keyword_extraction`, `theme_clustering`, `trend_analysis`, `summary_generation`) 디렉토리가 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리 내부에 `data_collection/` 디렉토리가 존재하는지 확인합니다.
    2.  `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리 내부에 `keyword_extraction/` 디렉토리가 존재하는지 확인합니다.
    3.  `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리 내부에 `theme_clustering/` 디렉토리가 존재하는지 확인합니다.
    4.  `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리 내부에 `trend_analysis/` 디렉토리가 존재하는지 확인합니다.
    5.  `theme_news_agent/theme_news_agent/sub_agents/` 디렉토리 내부에 `summary_generation/` 디렉토리가 존재하는지 확인합니다.
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
    1.  `theme_news_agent/theme_news_agent/sub_agents/__init__.py` 파일이 존재하는지 확인합니다.
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

## 2. 의존성 관리

### 2.1. Poetry 초기화

#### 2.1.1. `pyproject.toml` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_pyproject_toml_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `poetry init` 실행 후 `theme_news_agent/` 디렉토리 내부에 `pyproject.toml` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `pyproject.toml` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/pyproject.toml` 파일이 존재합니다.

#### 2.1.2. 핵심 의존성 추가 확인

- [X]
*   **테스트 케이스 ID:** `test_core_dependencies_added`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `pyproject.toml` 파일에 핵심 의존성(`google-adk`, `requests`, `beautifulsoup4`, `playwright`, `newspaper3k`, `numpy`, `pandas`, `pydantic`, `python-dotenv`)이 포함되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/pyproject.toml` 파일을 로드합니다.
    2.  `[tool.poetry.dependencies]` 섹션에 명시된 모든 핵심 의존성이 존재하는지 확인합니다.
*   **예상 결과:** 모든 핵심 의존성이 `pyproject.toml` 파일에 명시되어 있습니다.

#### 2.1.3. 개발 의존성 추가 확인 (pytest)

- [X]
*   **테스트 케이스 ID:** `test_dev_dependency_pytest_added`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `pyproject.toml` 파일의 `[tool.poetry.group.dev.dependencies]` 섹션에 `pytest`가 포함되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/pyproject.toml` 파일을 로드합니다.
    2.  `[tool.poetry.group.dev.dependencies]` 섹션에 `pytest`가 존재하는지 확인합니다.
*   **예상 결과:** `pytest` 의존성이 `pyproject.toml` 파일의 개발 그룹에 명시되어 있습니다.

#### 2.1.4. `poetry.lock` 파일 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_poetry_lock_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `poetry install` 실행 후 `theme_news_agent/` 디렉토리 내부에 `poetry.lock` 파일이 성공적으로 생성/업데이트되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `poetry.lock` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/poetry.lock` 파일이 존재합니다.

## 3. 환경 설정 파일

### 3.1. 예제 환경 파일

#### 3.1.1. `.env.example` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_env_example_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `.env.example` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `.env.example` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/.env.example` 파일이 존재합니다.

#### 3.1.2. `.env` 파일 생성

- [X]
*   **테스트 케이스 ID:** `test_env_creation`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `theme_news_agent/` 디렉토리 내부에 `.env` 파일이 성공적으로 생성되었는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent/` 디렉토리 내부에 `.env` 파일이 존재하는지 확인합니다.
*   **예상 결과:** `theme_news_agent/.env` 파일이 존재합니다.

### 3.2. Git 무시 설정

#### 3.2.1. `.gitignore`에 `.env` 추가 확인

- [X]
*   **테스트 케이스 ID:** `test_env_ignored`
*   **우선순위:** 높음
*   **유형:** 기능 테스트
*   **설명:** `.gitignore` 파일에 `theme_news_agent/.env` 경로가 포함되어 Git 추적에서 제외되는지 확인합니다.
*   **단계:**
    1.  `git check-ignore theme_news_agent/.env` 명령을 실행합니다.
    2.  명령어가 성공적으로 실행되고 해당 경로를 출력하는지 확인합니다.
*   **예상 결과:** `git check-ignore` 명령이 성공하고 `theme_news_agent/.env`를 출력합니다.
