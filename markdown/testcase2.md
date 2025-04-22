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
*   **예상 결과:** 오류 로그 발생 후, 상태에 빈 키워드 리스트가 저장되고, 0개 추출 메시지가 반환됩니다.

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

### 5.2 통계 분석 도구 구현 (`StatisticalAnalysisTool`)

#### 5.2.1. 과거 데이터 파일 없을 때 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_no_historical_file`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** `historical_themes.json` 파일이 없을 때, `calculate_trends` 함수가 오류 없이 실행되고, 모든 테마의 Z-점수를 0으로 반환하며, 새로운 빈 데이터로 파일을 생성하는지 확인합니다.
*   **단계:**
    1.  테스트용 `current_themes` 딕셔너리 리스트를 생성합니다.
    2.  과거 데이터 파일 경로(`HISTORICAL_DATA_PATH` 환경 변수 또는 기본값)에 파일이 존재하지 않도록 설정합니다 (예: `os.remove` 또는 모킹).
    3.  `calculate_trends` 함수를 호출합니다.
    4.  반환된 리스트의 모든 테마 딕셔너리에 `z_score` 키가 있고 값이 0.0인지 확인합니다.
    5.  지정된 경로에 빈 내용 또는 초기 테마 데이터가 포함된 `historical_themes.json` 파일이 생성되었는지 확인합니다.
*   **예상 결과:** Z-점수가 0으로 계산된 테마 리스트 반환, 과거 데이터 파일 생성.

#### 5.2.2. 과거 데이터 로드 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_load_historical_data`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** 유효한 `historical_themes.json` 파일이 존재할 때, `calculate_trends` 함수가 데이터를 올바르게 로드하여 Z-점수 계산에 사용하는지 확인합니다.
*   **단계:**
    1.  미리 정의된 과거 데이터(테마명, `mentions_history`, `avg`, `std` 포함)를 담은 JSON 파일을 지정된 경로에 생성합니다.
    2.  테스트용 `current_themes` 딕셔너리 리스트를 생성합니다 (일부는 과거 데이터와 겹치고, 일부는 새로운 테마 포함).
    3.  `calculate_trends` 함수를 호출합니다.
    4.  반환된 리스트에서 과거 데이터가 있는 테마의 Z-점수가 올바르게 계산되었는지 확인합니다 (`(current_mentions - avg) / std`).
    5.  과거 데이터가 없는 새로운 테마의 Z-점수가 0.0인지 확인합니다.
*   **예상 결과:** 과거 데이터를 기반으로 Z-점수가 정확히 계산됨.

#### 5.2.3. 손상된 과거 데이터 파일 처리 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_corrupted_historical_file`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** `historical_themes.json` 파일이 존재하지만 유효하지 않은 JSON 형식일 때, 함수가 오류 없이 실행되고 빈 데이터로 시작하는 것처럼 동작하는지 (Z-점수 0 반환) 확인합니다.
*   **단계:**
    1.  지정된 경로에 손상된 JSON 내용(예: `{"invalid"}`)을 가진 파일을 생성합니다.
    2.  테스트용 `current_themes` 리스트를 생성합니다.
    3.  `calculate_trends` 함수를 호출합니다 (오류 로그가 발생하는지 확인).
    4.  반환된 리스트의 모든 테마 Z-점수가 0.0인지 확인합니다.
    5.  업데이트된 과거 데이터 파일이 (정상적인 JSON 형식으로) 덮어쓰여졌는지 확인합니다.
*   **예상 결과:** 오류 로그 발생, Z-점수는 0, 손상된 파일은 정상 데이터로 덮어쓰여짐.

#### 5.2.4. Z-점수 계산 정확성 테스트 (std > 0)

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_z_score_calculation_std_positive`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** 과거 데이터의 표준편차(`std`)가 0보다 클 때 Z-점수가 `(current_mentions - avg) / std` 공식에 따라 정확히 계산되는지 확인합니다.
*   **단계:**
    1.  `avg=100`, `std=20`인 특정 테마의 과거 데이터를 포함하는 JSON 파일 생성.
    2.  해당 테마의 `mentions=140`인 `current_themes` 리스트 생성.
    3.  `calculate_trends` 함수 호출.
    4.  반환된 결과에서 해당 테마의 `z_score`가 `(140 - 100) / 20 = 2.0`에 가까운지 확인합니다 (부동 소수점 오차 고려).
*   **예상 결과:** Z-점수가 약 2.0으로 계산됨.

#### 5.2.5. Z-점수 계산 정확성 테스트 (std = 0)

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_z_score_calculation_std_zero`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** 과거 데이터의 표준편차(`std`)가 0일 때 Z-점수가 0으로 계산되는지 확인합니다.
*   **단계:**
    1.  `avg=100`, `std=0` (예: `mentions_history=[100]`)인 특정 테마의 과거 데이터를 포함하는 JSON 파일 생성.
    2.  해당 테마의 `mentions=120`인 `current_themes` 리스트 생성.
    3.  `calculate_trends` 함수 호출 (로그 메시지 확인).
    4.  반환된 결과에서 해당 테마의 `z_score`가 0.0인지 확인합니다.
*   **예상 결과:** Z-점수가 0.0으로 계산됨 (표준편차 0일 때).

#### 5.2.6. 과거 데이터 업데이트 테스트 (기존 테마)

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_update_existing_theme`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** 기존 테마의 현재 언급량이 과거 데이터의 `mentions_history`에 추가되고, `avg`와 `std`가 올바르게 재계산되어 파일에 저장되는지 확인합니다.
*   **단계:**
    1.  `mentions_history=[100, 120]`, `avg=110`, `std=10`인 테마 "A"의 과거 데이터 파일 생성.
    2.  테마 "A"의 `mentions=150`인 `current_themes` 리스트 생성.
    3.  `calculate_trends` 함수 호출.
    4.  저장된 과거 데이터 파일을 다시 로드합니다.
    5.  로드된 데이터에서 테마 "A"의 `mentions_history`가 `[100, 120, 150]`이 되었는지 확인합니다.
    6.  로드된 데이터에서 테마 "A"의 `avg`가 `np.mean([100, 120, 150])` 값과 일치하는지 확인합니다.
    7.  로드된 데이터에서 테마 "A"의 `std`가 `np.std([100, 120, 150])` 값과 일치하는지 확인합니다.
*   **예상 결과:** 과거 데이터가 올바르게 업데이트되고 저장됨.

#### 5.2.7. 과거 데이터 업데이트 테스트 (새로운 테마)

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_add_new_theme`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (파일 시스템 모킹 필요)
*   **설명:** 새로운 테마가 과거 데이터 파일에 올바른 초기값(`mentions_history`, `avg`, `std=0`)으로 추가되는지 확인합니다.
*   **단계:**
    1.  비어 있거나 다른 테마만 있는 과거 데이터 파일 생성.
    2.  새로운 테마 "B"의 `mentions=50`인 `current_themes` 리스트 생성.
    3.  `calculate_trends` 함수 호출.
    4.  저장된 과거 데이터 파일을 다시 로드합니다.
    5.  로드된 데이터에 테마 "B"가 포함되어 있는지 확인합니다.
    6.  테마 "B"의 `mentions_history`가 `[50]`인지 확인합니다.
    7.  테마 "B"의 `avg`가 `50.0`인지 확인합니다.
    8.  테마 "B"의 `std`가 `0.0`인지 확인합니다.
*   **예상 결과:** 새로운 테마가 올바른 초기값으로 과거 데이터에 추가되고 저장됨.

#### 5.2.8. 입력 형식 유효성 검사 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_invalid_input_format`
*   **우선순위:** 중간
*   **유형:** 단위 테스트
*   **설명:** `current_themes` 리스트의 항목이 예상된 딕셔너리 형식이 아니거나(예: 문자열), 'theme' 또는 'mentions' 키가 누락/잘못된 타입일 때 경고를 로깅하고 해당 항목의 Z-점수를 0으로 처리하는지 확인합니다.
*   **단계:**
    1.  유효하지 않은 형식의 항목(예: `{"theme": "A"}` (mentions 누락), `{"mentions": 100}` (theme 누락), `"just a string"`)을 포함하는 `current_themes` 리스트 생성.
    2.  `calculate_trends` 함수를 호출하고 로그 출력을 캡처합니다.
    3.  반환된 리스트에서 유효하지 않았던 항목의 `z_score`가 0.0인지 확인합니다.
    4.  로그 출력에 관련 경고 메시지가 포함되어 있는지 확인합니다.
    5.  과거 데이터 업데이트 시 유효하지 않은 항목은 제외되었는지 확인합니다 (선택적).
*   **예상 결과:** 경고 로그 발생, 유효하지 않은 항목은 Z-점수 0으로 처리됨.

#### 5.2.9. 환경 변수 `HISTORICAL_DATA_PATH` 테스트

- [X]
*   **테스트 케이스 ID:** `test_calculate_trends_historical_data_path_env_var`
*   **우선순위:** 낮음
*   **유형:** 단위 테스트 (환경 변수 모킹 필요)
*   **설명:** `HISTORICAL_DATA_PATH` 환경 변수가 설정되었을 때, 함수가 해당 경로를 사용하여 데이터를 로드하고 저장하는지 확인합니다.
*   **단계:**
    1.  `HISTORICAL_DATA_PATH` 환경 변수를 특정 테스트 경로로 설정합니다 (예: `/tmp/test_history.json`).
    2.  해당 경로에 테스트용 과거 데이터를 생성합니다.
    3.  `calculate_trends` 함수를 호출합니다.
    4.  함수 실행 중 기본 경로가 아닌 설정된 경로에서 파일을 읽고 썼는지 확인합니다 (예: 파일 I/O 모킹 또는 실제 파일 변경 확인).
*   **예상 결과:** 환경 변수에 지정된 경로의 파일을 사용함.

### 5.3 에이전트 로직 구현 (`TrendAnalysisAgent.process`)

#### 5.3.1. 상태 데이터 로드 실패 테스트 (`clustered_themes` 누락)

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_missing_state`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `ctx.state`에 `clustered_themes` 키가 없거나 값이 없을 때 `process` 메서드가 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  `InvocationContext` 객체를 모킹하고 `state`를 빈 딕셔너리로 설정합니다.
    3.  `await agent.process(mock_ctx)`를 호출합니다.
    4.  반환된 문자열에 "Error: 'clustered_themes' not found or invalid in state."가 포함되어 있는지 확인합니다.
*   **예상 결과:** 지정된 오류 메시지를 반환합니다.

#### 5.3.2. 상태 데이터 형식 오류 테스트 (`clustered_themes`가 리스트가 아님)

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_invalid_state_type`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `ctx.state["clustered_themes"]`의 값이 리스트가 아닌 경우 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]`에 문자열이나 숫자 등 리스트가 아닌 값을 설정합니다.
    3.  `await agent.process(mock_ctx)`를 호출합니다.
    4.  반환된 문자열에 "Error: 'clustered_themes' not found or invalid in state."가 포함되어 있는지 확인합니다.
*   **예상 결과:** 지정된 오류 메시지를 반환합니다.

#### 5.3.3. `calculate_trends` 도구 호출 확인 테스트

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_calls_stats_tool`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `process` 메서드가 내부적으로 `self.stats_tool.func` (즉, `calculate_trends`)를 올바른 인자(`clustered_themes` 리스트)로 호출하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  테스트용 `clustered_themes` 리스트를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]`를 설정합니다.
    4.  `agent.stats_tool.func`를 모킹하여 유효한 리스트를 반환하도록 설정합니다.
    5.  `await agent.process(mock_ctx)`를 호출합니다.
    6.  모킹된 `agent.stats_tool.func`가 2단계에서 정의한 리스트를 인자로 사용하여 한 번 호출되었는지 확인합니다 (`assert_called_once_with`).
*   **예상 결과:** `calculate_trends` 함수가 올바른 데이터로 호출됩니다.

#### 5.3.4. `calculate_trends` 도구 호출 실패 테스트

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_stats_tool_exception`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `calculate_trends` 함수 호출 중 예외가 발생했을 때 `process` 메서드가 해당 오류 메시지를 반환하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  테스트용 `clustered_themes` 리스트를 정의하고 `mock_ctx.state`에 설정합니다.
    3.  `agent.stats_tool.func`를 모킹하여 `Exception("Tool Error")`를 발생시키도록 설정합니다.
    4.  `await agent.process(mock_ctx)`를 호출합니다.
    5.  반환된 문자열에 "Error during trend analysis: Tool Error"와 유사한 내용이 포함되어 있는지 확인합니다.
*   **예상 결과:** 도구 실행 중 발생한 예외 메시지를 포함한 오류 문자열을 반환합니다.

#### 5.3.5. Z-점수 기준 정렬 테스트

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_sorts_by_zscore`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `calculate_trends` 함수가 Z-점수를 포함한 테마 리스트를 반환했을 때, `process` 메서드가 이 리스트를 Z-점수 기준 내림차순으로 올바르게 정렬하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  Z-점수가 무작위 순서로 포함된 테마 딕셔너리 리스트를 정의합니다 (예: `[{'theme': 'A', 'z_score': 1.5}, {'theme': 'B', 'z_score': 3.0}, {'theme': 'C', 'z_score': 0.5}]`).
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]`를 설정합니다 (임의의 값, 여기서는 사용되지 않음).
    4.  `agent.stats_tool.func`를 모킹하여 2단계에서 정의한 Z-점수 포함 리스트를 반환하도록 설정합니다.
    5.  `await agent.process(mock_ctx)`를 호출합니다.
    6.  `ctx.state["trend_results"]`에 저장된 리스트를 확인합니다.
    7.  리스트의 첫 번째 항목이 Z-점수가 가장 높은 테마('B')이고, 마지막 항목이 Z-점수가 가장 낮은 테마('C')인지 확인합니다.
*   **예상 결과:** 상태에 저장된 `trend_results` 리스트가 Z-점수 내림차순으로 정렬되어 있습니다.

#### 5.3.6. 상위 N개 선택 테스트 (`TREND_TOP_N` 환경 변수)

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_selects_top_n`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `TREND_TOP_N` 환경 변수 값에 따라 정렬된 테마 리스트에서 상위 N개의 테마만 선택하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  Z-점수 순서로 정렬된 5개의 테마 딕셔너리 리스트를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]`를 설정합니다.
    4.  `agent.stats_tool.func`를 모킹하여 2단계 리스트를 반환하도록 설정합니다.
    5.  `os.getenv`를 모킹하여 `TREND_TOP_N`에 대해 "3"을 반환하도록 설정합니다.
    6.  `await agent.process(mock_ctx)`를 호출합니다.
    7.  `ctx.state["trend_results"]`에 저장된 리스트의 길이가 3인지 확인합니다.
    8.  저장된 리스트가 원래 리스트의 상위 3개 항목과 일치하는지 확인합니다.
*   **예상 결과:** `trend_results` 리스트에 상위 3개의 테마만 포함됩니다.

#### 5.3.7. 상위 N개 선택 테스트 (기본값)

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_selects_top_n_default`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `TREND_TOP_N` 환경 변수가 설정되지 않았을 때 기본값(20)을 사용하여 상위 테마를 선택하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  Z-점수 순서로 정렬된 25개의 테마 딕셔너리 리스트를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]`를 설정합니다.
    4.  `agent.stats_tool.func`를 모킹하여 2단계 리스트를 반환하도록 설정합니다.
    5.  `os.getenv`를 모킹하여 `TREND_TOP_N`에 대해 None (`os.getenv`의 기본 동작) 또는 다른 키에 대한 호출 시 원래 동작을 유지하도록 설정합니다.
    6.  `await agent.process(mock_ctx)`를 호출합니다.
    7.  `ctx.state["trend_results"]`에 저장된 리스트의 길이가 20인지 확인합니다.
*   **예상 결과:** `trend_results` 리스트에 상위 20개의 테마만 포함됩니다.

#### 5.3.8. 상위 N개 선택 테스트 (유효하지 않은 값)

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_selects_top_n_invalid`
*   **우선순위:** 중간
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** `TREND_TOP_N` 환경 변수 값이 숫자가 아니거나 음수일 때 기본값(20)을 사용하는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  Z-점수 순서로 정렬된 25개의 테마 딕셔너리 리스트를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]` 설정, `agent.stats_tool.func` 모킹.
    4.  `os.getenv`를 모킹하여 `TREND_TOP_N`에 대해 "abc" 또는 "-5"를 반환하도록 설정합니다.
    5.  `await agent.process(mock_ctx)`를 호출하고 로그 출력을 캡처합니다.
    6.  `ctx.state["trend_results"]`에 저장된 리스트의 길이가 20인지 확인합니다.
    7.  로그 출력에 "Invalid TREND_TOP_N value" 또는 "TREND_TOP_N (...) is not positive" 와 유사한 경고 메시지가 포함되어 있는지 확인합니다.
*   **예상 결과:** 경고 로그 발생 및 `trend_results` 리스트에 상위 20개 테마 포함.

#### 5.3.9. 순위(Rank) 추가 테스트

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_adds_rank`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 선택된 상위 N개 테마 리스트의 각 딕셔너리에 'rank' 키가 1부터 N까지 순서대로 올바르게 추가되는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  Z-점수 순서로 정렬된 3개의 테마 딕셔너리 리스트를 정의합니다.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]` 설정, `agent.stats_tool.func` 모킹 (2단계 리스트 반환).
    4.  `os.getenv` 모킹 (`TREND_TOP_N` = "3" 또는 기본값).
    5.  `await agent.process(mock_ctx)`를 호출합니다.
    6.  `ctx.state["trend_results"]`에 저장된 리스트를 확인합니다.
    7.  첫 번째 항목의 `rank`가 1인지 확인합니다.
    8.  두 번째 항목의 `rank`가 2인지 확인합니다.
    9.  세 번째 항목의 `rank`가 3인지 확인합니다.
*   **예상 결과:** `trend_results` 리스트의 각 항목에 1부터 시작하는 올바른 `rank` 값이 추가됩니다.

#### 5.3.10. 최종 상태 저장 및 성공 메시지 테스트

- [X]
*   **테스트 케이스 ID:** `test_trend_agent_process_saves_state_and_returns_success`
*   **우선순위:** 높음
*   **유형:** 단위 테스트 (모킹 사용)
*   **설명:** 모든 처리가 성공적으로 완료되었을 때, 최종 `ranked_themes` 리스트가 `ctx.state["trend_results"]`에 저장되고, 적절한 성공 메시지 문자열이 반환되는지 확인합니다.
*   **단계:**
    1.  `TrendAnalysisAgent` 인스턴스를 생성합니다.
    2.  테스트용 `clustered_themes` 리스트 정의.
    3.  `InvocationContext` 객체를 모킹하고 `state["clustered_themes"]` 설정.
    4.  `agent.stats_tool.func`를 모킹하여 Z-점수 포함 리스트 반환 설정.
    5.  `os.getenv` 모킹 (예: `TREND_TOP_N` = "5").
    6.  `await agent.process(mock_ctx)`를 호출합니다.
    7.  `mock_ctx.state` 딕셔너리에 `trend_results` 키가 존재하는지 확인합니다.
    8.  `mock_ctx.state["trend_results"]` 값이 예상되는 최종 순위 리스트 (정렬, 상위 N개 선택, rank 추가 완료)와 일치하는지 확인합니다.
    9.  반환된 문자열이 "Trend analysis complete. Top 5 trends identified and saved." 와 유사한 형식인지 확인합니다.
*   **예상 결과:** 최종 결과가 상태에 저장되고, 성공 메시지가 반환됩니다. 