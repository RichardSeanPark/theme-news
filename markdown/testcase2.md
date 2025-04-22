# 테스트 케이스 (testcase2.md)

이 문서는 개발 프로세스 규칙에 따라 생성된 테스트 케이스를 기록합니다.

## 3.2 추출 프롬프트 정의

### 3.2.1. `get_extraction_prompt` 함수 기본 테스트

- [X]
*   **테스트 케이스 ID:** `test_get_extraction_prompt_basic`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `get_extraction_prompt` 함수가 입력된 텍스트를 포함하여 올바른 형식의 프롬프트 문자열을 생성하는지 확인합니다.
*   **단계:**
    1.  `get_extraction_prompt` 함수를 임포트합니다.
    2.  테스트용 입력 텍스트를 정의합니다 (예: "AI 기술이 발전하고 있습니다.").
    3.  `get_extraction_prompt(test_text)`를 호출하여 결과를 얻습니다.
    4.  반환된 문자열이 None이 아닌지 확인합니다.
    5.  반환된 문자열이 `DEFAULT_EXTRACTION_PROMPT`의 기본 구조 (예: "다음 텍스트에서...", "텍스트:\n---", "추출된 키워드 (JSON 리스트):")를 포함하는지 확인합니다.
    6.  반환된 문자열이 입력된 테스트 텍스트 ("AI 기술이 발전하고 있습니다.")를 포함하는지 확인합니다.
*   **예상 결과:** 입력 텍스트가 포함된 완전하고 올바른 형식의 프롬프트 문자열이 반환됩니다.

## 3.3 에이전트 로직 구현 (`KeywordExtractionAgent.process`)

### 3.3.1. `collected_data` 누락 시 오류 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_missing_collected_data`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `ctx.state`에 `collected_data`가 없을 때 `process` 메서드가 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  `InvocationContext` 객체를 모킹하고, `state`를 빈 딕셔너리로 설정합니다.
    3.  `agent.process(mock_ctx)`를 호출합니다.
    4.  반환된 메시지에 "collected_data가 상태에 없습니다" 와 유사한 오류 문구가 포함되어 있는지 확인합니다.
*   **예상 결과:** 오류 메시지를 포함한 문자열을 반환합니다.

### 3.3.2. `collected_data` 내 기사 없을 시 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_no_articles_in_collected_data`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `collected_data`는 있지만 추출할 기사가 없을 때 `process` 메서드가 적절한 메시지를 반환하고 상태에 빈 리스트를 저장하는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  모든 기사 리스트가 비어있는 `CollectedData` 모델의 딕셔너리 표현을 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`에 위 딕셔너리를 설정합니다.
    4.  `agent.process(mock_ctx)`를 호출합니다.
    5.  반환된 메시지에 "추출할 기사가 없습니다" 와 유사한 문구가 포함되어 있는지 확인합니다.
    6.  `mock_ctx.state["extracted_keywords_raw"]`가 빈 리스트(`[]`)인지 확인합니다.
*   **예상 결과:** 경고성 메시지를 반환하고, 상태에 빈 키워드 리스트를 저장합니다.

### 3.3.3. 정상 처리 (LLM 응답 모킹) 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_success_with_mocked_llm`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 정상적인 `collected_data` 입력과 모킹된 유효한 LLM 응답(JSON 리스트 문자열)이 주어졌을 때, `process` 메서드가 키워드를 파싱하여 상태에 저장하고 성공 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `ArticleData`를 포함하는 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`에 위 딕셔너리를 설정합니다.
    4.  `agent.generate_content` 메서드를 모킹하여 유효한 JSON 리스트 문자열 (예: `"[\"키워드1\", \"키워드2\"]"`)을 반환하도록 설정합니다.
    5.  `agent.process(mock_ctx)`를 호출합니다.
    6.  `agent.generate_content`가 호출되었는지 확인합니다.
    7.  `mock_ctx.state["extracted_keywords_raw"]`가 파싱된 키워드 리스트 (예: `["키워드1", "키워드2"]`)와 일치하는지 확인합니다.
    8.  반환된 메시지에 "키워드 추출 완료" 와 유사한 성공 문구와 추출된 키워드 개수가 포함되어 있는지 확인합니다.
*   **예상 결과:** `generate_content` 호출 후, 파싱된 키워드가 상태에 저장되고, 성공 메시지가 반환됩니다.

### 3.3.4. LLM 응답 파싱 실패 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_llm_response_parsing_failure`, `test_process_llm_response_invalid_json_structure`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 모킹된 LLM 응답이 유효한 JSON 형식이 아닐 때, `process` 메서드가 오류를 로깅하고 상태에 빈 리스트를 저장하며 처리 완료 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`를 설정합니다.
    4.  `agent.generate_content` 메서드를 모킹하여 유효하지 않은 JSON 문자열 (예: `"그냥 텍스트 응답"` 또는 `"{\"key\": \"value\"}"`)을 반환하도록 설정합니다.
    5.  로그 출력을 캡처하도록 설정합니다 (예: `caplog` fixture 사용).
    6.  `agent.process(mock_ctx)`를 호출합니다.
    7.  `agent.generate_content`가 호출되었는지 확인합니다.
    8.  로그 출력에 "LLM 응답 파싱 중 오류 발생" 또는 "LLM 응답이 예상된 JSON 형식이 아님" 과 유사한 오류/경고 메시지가 포함되어 있는지 확인합니다.
    9.  `mock_ctx.state["extracted_keywords_raw"]`가 빈 리스트(`[]`)인지 확인합니다.
    10. 반환된 메시지에 키워드 개수가 0개임을 나타내는 내용이 포함되어 있는지 확인합니다.
*   **예상 결과:** 오류 로그 발생 후, 상태에 빈 키워드 리스트가 저장되고, 0개 추출 메시지가 반환됩니다.

### 3.3.5. LLM 호출 실패 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_llm_call_failure`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `agent.generate_content` 호출 중 예외가 발생했을 때, `process` 메서드가 오류 메시지를 반환하고 상태에 빈 리스트를 저장하는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`를 설정합니다.
    4.  `agent.generate_content` 메서드를 모킹하여 `Exception`을 발생시키도록 설정합니다.
    5.  `agent.process(mock_ctx)`를 호출합니다.
    6.  `agent.generate_content`가 호출되었는지 확인합니다.
    7.  `mock_ctx.state["extracted_keywords_raw"]`가 빈 리스트(`[]`)인지 확인합니다.
    8.  반환된 메시지에 "LLM 호출 중 오류 발생" 과 유사한 오류 문구가 포함되어 있는지 확인합니다.
*   **예상 결과:** 오류 메시지를 반환하고, 상태에 빈 키워드 리스트를 저장합니다.

## 3.4 키워드 빈도 계산 도구/함수 구현 (`calculate_keyword_frequencies`)

### 3.4.1. 기본 빈도 계산 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_basic`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** 간단한 키워드와 데이터에 대해 전체 및 출처별 빈도수가 정확히 계산되는지 확인합니다.
*   **단계:**
    1.  테스트용 `CollectedData` 객체 생성 (다양한 소스의 `ArticleData` 포함).
    2.  테스트용 키워드 리스트 정의 (예: `["ai", "테스트"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  반환된 리스트의 각 딕셔너리가 예상 키워드와 예상 빈도수(`total`, `news`, `blogs` 등)를 포함하는지 확인합니다.
*   **예상 결과:** 각 키워드의 정확한 전체/출처별 빈도수가 계산된 결과 리스트 반환.

### 3.4.2. 대소문자 구분 없음 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_case_insensitive`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** 키워드 검색 시 대소문자를 구분하지 않고 빈도수를 계산하는지 확인합니다 (예: "AI"와 "ai" 모두 카운트).
*   **단계:**
    1.  대소문자가 혼용된 텍스트를 포함하는 테스트용 `CollectedData` 객체 생성.
    2.  테스트용 키워드 리스트 정의 (예: `["ai"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  결과에서 "ai" 키워드의 빈도수가 대소문자 구분 없이 모두 합산되었는지 확인합니다.
*   **예상 결과:** 대소문자 구분 없이 키워드 빈도수가 정확히 계산됨.

### 3.4.3. 단어 경계 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_word_boundaries`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** 키워드가 다른 단어의 일부일 경우 카운트하지 않는지 확인합니다 (예: "art"가 "article"의 일부로 카운트되지 않음).
*   **단계:**
    1.  키워드를 포함하는 더 긴 단어가 있는 테스트용 `CollectedData` 객체 생성.
    2.  테스트용 키워드 리스트 정의 (예: `["art"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  결과에서 "art" 키워드의 빈도수가 독립된 단어 "art"만 카운트했는지 확인합니다.
*   **예상 결과:** 단어 경계를 존중하여 정확한 빈도수가 계산됨.

### 3.4.4. 빈 키워드 리스트 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_empty_keywords`
*   **우선순위:** 낮음
*   **유형:** 단위 테스트
*   **설명:** 입력 키워드 리스트가 비어 있을 때 빈 결과 리스트를 반환하는지 확인합니다.
*   **단계:**
    1.  테스트용 `CollectedData` 객체 생성.
    2.  빈 키워드 리스트 정의 (`[]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  반환된 결과가 빈 리스트(`[]`)인지 확인합니다.
*   **예상 결과:** 빈 리스트 반환.

### 3.4.5. 빈 데이터 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_empty_data`
*   **우선순위:** 낮음
*   **유형:** 단위 테스트
*   **설명:** `CollectedData`에 아무런 `ArticleData`가 없을 때 모든 키워드의 빈도수가 0으로 계산되는지 확인합니다.
*   **단계:**
    1.  빈 `CollectedData` 객체 생성.
    2.  테스트용 키워드 리스트 정의 (예: `["ai"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  반환된 결과에서 "ai" 키워드의 모든 빈도수(`total`, `news` 등)가 0인지 확인합니다.
*   **예상 결과:** 모든 키워드의 빈도수가 0인 결과 리스트 반환.

### 3.4.6. 키워드 없음 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_keyword_not_found`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** 입력된 키워드가 데이터 내에 전혀 존재하지 않을 때 빈도수가 0으로 계산되는지 확인합니다.
*   **단계:**
    1.  테스트용 `CollectedData` 객체 생성.
    2.  데이터에 존재하지 않는 키워드 리스트 정의 (예: `["존재하지않는키워드"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  반환된 결과에서 해당 키워드의 모든 빈도수가 0인지 확인합니다.
*   **예상 결과:** 해당 키워드의 빈도수가 0인 결과 리스트 반환.

### 3.4.7. 특수 문자 포함 키워드 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_special_chars`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** 키워드에 정규식 특수 문자가 포함된 경우에도 정확히 빈도수를 계산하는지 확인합니다 (예: "C++", "node.js").
*   **단계:**
    1.  특수 문자가 포함된 키워드를 포함하는 텍스트를 가진 `CollectedData` 객체 생성.
    2.  테스트용 키워드 리스트 정의 (예: `["C++", "node.js"]`).
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  결과에서 "C++"와 "node.js" 키워드의 빈도수가 정확히 계산되었는지 확인합니다.
*   **예상 결과:** 특수 문자가 포함된 키워드의 빈도수가 정확히 계산됨.

### 3.4.8. 다양한 소스 카테고리 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_keyword_frequencies_source_categories`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** "NewsAPI", "Naver Blog", "Yahoo Finance Trending", "Google Trends" 등 다양한 소스 문자열이 올바른 카테고리("news", "blogs", "finance", "search")로 매핑되어 빈도수가 집계되는지 확인합니다.
*   **단계:**
    1.  다양한 `source` 값을 가진 `ArticleData`를 포함하는 `CollectedData` 객체 생성.
    2.  테스트용 키워드 리스트 정의.
    3.  `calculate_keyword_frequencies` 함수 호출.
    4.  결과에서 각 키워드의 빈도수가 올바른 소스 카테고리별로 집계되었는지 확인합니다.
*   **예상 결과:** 다양한 소스가 올바른 카테고리로 매핑되어 빈도수가 집계됨.

## 3.5 상태 관리

### 3.5.1. `keyword_results` 상태 저장 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_stores_keyword_results`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `KeywordExtractionAgent.process`가 성공적으로 실행된 후, 계산된 키워드 빈도 결과가 `ctx.state["keyword_results"]`에 올바른 형식으로 저장되는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`를 설정합니다.
    4.  `LLMRegistry.new_llm`을 모킹하여 모의 LLM 인스턴스를 반환하도록 설정합니다.
    5.  모의 LLM 인스턴스의 `generate_content_async`가 유효한 키워드 JSON 리스트 (예: `["ai"]`)를 반환하도록 설정합니다.
    6.  `calculate_keyword_frequencies` 함수를 **모킹**하여 예상되는 빈도 결과 딕셔너리 리스트 (예: `[{"keyword": "ai", "frequency": {"total": ...}}]`)를 반환하도록 설정합니다.
    7.  `agent.process(mock_ctx)`를 호출합니다.
    8.  `mock_ctx.state["keyword_results"]`의 값이 6단계에서 설정한 예상 빈도 결과와 일치하는지 확인합니다.
*   **예상 결과:** `calculate_keyword_frequencies`의 반환값이 `ctx.state["keyword_results"]`에 저장됩니다.

### 3.5.2. 키워드 없을 시 빈 결과 저장 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_stores_empty_results_if_no_keywords`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** LLM이 빈 키워드 리스트(`[]`)를 반환했을 때, `ctx.state["keyword_results"]`에 빈 리스트가 저장되는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`를 설정합니다.
    4.  `LLMRegistry.new_llm`을 모킹합니다.
    5.  모의 LLM 인스턴스의 `generate_content_async`가 빈 JSON 리스트 문자열 (`"[]"`)을 반환하도록 설정합니다.
    6.  `calculate_keyword_frequencies` 함수가 호출되지 **않는지** 확인하기 위해 모킹합니다 (선택 사항).
    7.  `agent.process(mock_ctx)`를 호출합니다.
    8.  `mock_ctx.state["keyword_results"]`가 빈 리스트(`[]`)인지 확인합니다.
*   **예상 결과:** `ctx.state["keyword_results"]`에 빈 리스트가 저장됩니다.

### 3.5.3. 빈도 계산 실패 시 빈 결과 저장 테스트

- [X]
*   **테스트 케이스 ID:** `test_process_stores_empty_results_on_freq_calc_error`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `calculate_keyword_frequencies` 함수 호출 중 예외가 발생했을 때, 오류가 로깅되고 `ctx.state["keyword_results"]`에 빈 리스트가 저장되는지 확인합니다.
*   **단계:**
    1.  `KeywordExtractionAgent` 인스턴스를 생성합니다.
    2.  테스트용 `CollectedData` 딕셔너리를 생성합니다.
    3.  `InvocationContext` 객체를 모킹하고, `state["collected_data"]`를 설정합니다.
    4.  `LLMRegistry.new_llm`을 모킹합니다.
    5.  모의 LLM 인스턴스의 `generate_content_async`가 유효한 키워드 JSON 리스트를 반환하도록 설정합니다.
    6.  `calculate_keyword_frequencies` 함수를 모킹하여 `Exception`을 발생시키도록 설정합니다.
    7.  로그 출력을 캡처하도록 설정합니다.
    8.  `agent.process(mock_ctx)`를 호출합니다.
    9.  로그 출력에 "키워드 빈도 계산 중 오류 발생" 과 유사한 오류 메시지가 있는지 확인합니다.
    10. `mock_ctx.state["keyword_results"]`가 빈 리스트(`[]`)인지 확인합니다.
*   **예상 결과:** 오류 로깅 후, `ctx.state["keyword_results"]`에 빈 리스트가 저장됩니다.

## 4단계: 테마 클러스터링 에이전트 구현

### 4.1 `ThemeClusteringAgent` 정의

#### 4.1.1. `ThemeClusteringAgent` 객체 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_theme_clustering_agent_creation`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `ThemeClusteringAgent` 클래스의 인스턴스가 성공적으로 생성되는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent.sub_agents.theme_clustering.agent` 모듈에서 `ThemeClusteringAgent` 클래스를 임포트합니다.
    2.  `agent = ThemeClusteringAgent()` 코드를 실행하여 인스턴스를 생성합니다.
    3.  생성된 `agent` 객체가 `ThemeClusteringAgent` 클래스의 인스턴스인지 확인합니다 (예: `isinstance(agent, ThemeClusteringAgent)`).
*   **예상 결과:** `ThemeClusteringAgent` 객체가 오류 없이 생성됩니다.

#### 4.1.2. `__init__` 속성 확인

- [X]
*   **테스트 케이스 ID:** `test_theme_clustering_agent_init_attributes`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** 생성된 `ThemeClusteringAgent` 인스턴스의 `model`, `instruction`, `description` 속성이 `__init__` 메서드에서 설정한 값과 일치하는지 확인합니다.
*   **단계:**
    1.  `ThemeClusteringAgent` 인스턴스를 생성합니다.
    2.  `agent.model` 속성이 `__init__`에 지정된 모델명 (예: 'gemini-1.5-flash-latest')과 일치하는지 확인합니다.
    3.  `agent.instruction` 속성이 `__init__`에 지정된 지침 문자열과 일치하는지 확인합니다.
    4.  `agent.description` 속성이 `__init__`에 지정된 설명 문자열과 일치하는지 확인합니다.
*   **예상 결과:** 인스턴스의 `model`, `instruction`, `description` 속성이 `__init__` 메서드에서 정의한 값과 정확히 일치합니다.

### 4.2 클러스터링 프롬프트 정의

#### 4.2.1. `CLUSTERING_PROMPT_TEMPLATE` 상수 확인

- [X]
*   **테스트 케이스 ID:** `test_clustering_prompt_template_content`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `prompt.py`에 정의된 `CLUSTERING_PROMPT_TEMPLATE` 상수가 필요한 키 문구들을 포함하는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent.sub_agents.theme_clustering.prompt` 모듈에서 `CLUSTERING_PROMPT_TEMPLATE`을 임포트합니다.
    2.  해당 상수가 문자열 타입인지 확인합니다.
    3.  상수 내용에 "JSON 형식의 배열", "theme", "keywords", "mentions", "{keyword_data_str}" 등의 키 문구가 포함되어 있는지 확인합니다.
*   **예상 결과:** 상수가 올바른 키 문구들을 포함한 문자열로 정의되어 있습니다.

#### 4.2.2. `get_clustering_prompt` 함수 - 정상 입력 테스트

- [X]
*   **테스트 케이스 ID:** `test_get_clustering_prompt_normal_input`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `get_clustering_prompt` 함수가 정상적인 키워드 빈도 리스트를 입력받았을 때, 프롬프트 템플릿의 `{keyword_data_str}` 부분을 올바르게 포맷팅하여 반환하는지 확인합니다.
*   **단계:**
    1.  `get_clustering_prompt` 함수를 임포트합니다.
    2.  테스트용 키워드 빈도 리스트를 생성합니다 (예: `[{"keyword": "AI", "frequency": {"total": 50}}, {"keyword": "ML", "frequency": {"total": 30}}]`).
    3.  함수를 호출하여 결과를 얻습니다.
    4.  반환된 문자열이 `CLUSTERING_PROMPT_TEMPLATE`의 기본 구조를 유지하는지 확인합니다.
    5.  반환된 문자열 내에 포맷팅된 키워드 데이터 문자열 (예: "- AI (50회 언급)\n- ML (30회 언급)")이 포함되어 있는지 확인합니다.
*   **예상 결과:** 키워드 데이터가 포함된 완전한 프롬프트 문자열이 반환됩니다.

#### 4.2.3. `get_clustering_prompt` 함수 - 빈 입력 테스트

- [X]
*   **테스트 케이스 ID:** `test_get_clustering_prompt_empty_input`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** `get_clustering_prompt` 함수가 빈 키워드 리스트(`[]`)를 입력받았을 때, `{keyword_data_str}` 부분이 "분석할 키워드가 없습니다."로 대체되어 반환되는지 확인합니다.
*   **단계:**
    1.  `get_clustering_prompt` 함수를 임포트합니다.
    2.  빈 리스트 (`[]`)를 인자로 함수를 호출합니다.
    3.  반환된 문자열에 "분석할 키워드가 없습니다."가 포함되어 있는지 확인합니다.
    4.  반환된 문자열이 여전히 `CLUSTERING_PROMPT_TEMPLATE`의 기본 구조를 유지하는지 확인합니다.
*   **예상 결과:** "분석할 키워드가 없습니다." 메시지가 포함된 프롬프트 문자열이 반환됩니다.

#### 4.2.4. `get_clustering_prompt` 함수 - 비정상 키 입력 테스트

- [X]
*   **테스트 케이스 ID:** `test_get_clustering_prompt_malformed_input`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** 입력 리스트 내 딕셔너리에 "keyword", "frequency", "total" 키가 일부 누락된 경우에도 오류 없이 기본값("N/A", 0)으로 처리되어 프롬프트가 생성되는지 확인합니다 (현재 구현은 문자열 변환에 의존하므로, 심각한 오류보다는 예상치 못한 프롬프트가 생성될 수 있음. 견고성을 높이기 위해 입력 검증 추가 고려).
*   **단계:**
    1.  `get_clustering_prompt` 함수를 임포트합니다.
    2.  잘못된 형식의 입력 데이터를 정의합니다 (예: 문자열, 숫자, 키가 누락된 딕셔너리 리스트).
    3.  `get_clustering_prompt(malformed_data)`를 호출합니다.
    4.  함수가 `TypeError` 또는 `KeyError`와 같은 적절한 예외를 발생시키는지 확인하거나, 혹은 예외 없이 특정 형식의 문자열을 반환하는 경우 해당 반환값을 검증합니다.
*   **예상 결과:** 함수가 예외를 발생시키거나, 잘못된 입력에 대해 예측 가능한 (오류를 나타내는) 문자열을 반환합니다.

### 4.3 에이전트 로직 구현 (`ThemeClusteringAgent.process`)

#### 4.3.1. 정상 처리 케이스

- [X]
*   **테스트 케이스 ID:** `test_process_returns_prompt_on_success`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 유효한 `keyword_results` 입력 시, `process` 메서드가 `get_clustering_prompt`를 호출하여 생성된 프롬프트 문자열을 올바르게 반환하는지 확인합니다.
*   **단계:**
    1.  `ThemeClusteringAgent` 인스턴스를 생성합니다.
    2.  테스트용 `keyword_results` (딕셔너리 리스트)를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["keyword_results"]`에 데이터를 설정합니다.
    4.  `get_clustering_prompt` 함수를 모킹하여 예상 프롬프트를 반환하도록 설정합니다.
    5.  `await agent.process(mock_ctx)`를 호출합니다.
    6.  `get_clustering_prompt`가 올바른 인자로 호출되었는지 확인합니다.
    7.  `process` 메서드의 반환값이 4단계에서 설정한 예상 프롬프트 문자열과 일치하는지 확인합니다.
    8.  로그 출력에 "클러스터링 프롬프트 생성 완료"가 포함되어 있는지 확인합니다.
*   **예상 결과:** `get_clustering_prompt` 호출 후, 생성된 프롬프트 문자열이 반환됩니다.

#### 4.3.2. 상태 누락 케이스

- [X]
*   **테스트 케이스 ID:** `test_process_missing_keyword_results`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `ctx.state`에 `keyword_results`가 없을 때 `process` 메서드가 경고 로깅 및 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `ThemeClusteringAgent` 인스턴스를 생성합니다.
    2.  `InvocationContext` 객체를 모킹하고, `state`를 빈 딕셔너리로 설정합니다.
    3.  로그 출력을 캡처하도록 설정합니다.
    4.  `await agent.process(mock_ctx)`를 호출합니다.
    5.  로그 출력에 "keyword_results'를 찾을 수 없거나 비어 있습니다" 와 유사한 경고 메시지가 있는지 확인합니다.
    6.  반환된 메시지에 "키워드 추출 결과가 없어" 와 유사한 오류 문구가 포함되어 있는지 확인합니다.
*   **예상 결과:** 경고 로그 발생 및 오류 메시지 반환.

#### 4.3.x. 프롬프트 생성 실패 케이스

- [X]
*   **테스트 케이스 ID:** `test_process_prompt_generation_failure`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `get_clustering_prompt` 함수 호출 중 예외가 발생했을 때, `process` 메서드가 오류 로깅 및 관련 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `ThemeClusteringAgent` 인스턴스를 생성합니다.
    2.  테스트용 `keyword_results`를 정의하고 `mock_ctx.state`에 설정합니다.
    3.  `get_clustering_prompt` 함수를 모킹하여 `Exception`을 발생시키도록 설정합니다.
    4.  로그 출력을 캡처하도록 설정합니다.
    5.  `await agent.process(mock_ctx)`를 호출합니다.
    6.  로그 출력에 "클러스터링 프롬프트 생성 중 오류 발생" 과 유사한 오류 메시지가 있는지 확인합니다.
    7.  반환된 메시지에 "클러스터링 프롬프트 생성 중 오류 발생:" 과 예외 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 오류 로그 발생 및 오류 메시지 반환.

## 5단계: 트렌드 분석 에이전트 구현

### 5.1 `TrendAnalysisAgent` 정의

#### 5.1.1. `TrendAnalysisAgent` 객체 생성 확인

- [X]
*   **테스트 케이스 ID:** `test_trend_analysis_agent_creation`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** `TrendAnalysisAgent` 클래스의 인스턴스가 성공적으로 생성되는지 확인합니다.
*   **단계:**
    1.  `theme_news_agent.sub_agents.trend_analysis.agent` 모듈에서 `TrendAnalysisAgent` 클래스를 임포트합니다.
    2.  `agent = TrendAnalysisAgent()` 코드를 실행하여 인스턴스를 생성합니다.
    3.  생성된 `agent` 객체가 `TrendAnalysisAgent` 클래스의 인스턴스인지 확인합니다 (예: `isinstance(agent, TrendAnalysisAgent)`).
*   **예상 결과:** `TrendAnalysisAgent` 객체가 오류 없이 생성됩니다.

#### 5.1.2. `__init__` 속성 확인 (description)

- [X]
*   **테스트 케이스 ID:** `test_trend_analysis_agent_init_attributes`
*   **우선순위:** 높음
*   **유형:** 단위 테스트
*   **설명:** 생성된 `TrendAnalysisAgent` 인스턴스의 `description` 속성이 `__init__` 메서드에서 설정한 값과 일치하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  `agent.description` 속성이 `__init__`에 지정된 설명 문자열 ("Analyzes theme trends based on historical data and Z-scores.")과 일치하는지 확인합니다.
*   **예상 결과:** 인스턴스의 `description` 속성이 `__init__` 메서드에서 정의한 값과 정확히 일치합니다. 