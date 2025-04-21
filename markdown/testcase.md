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
