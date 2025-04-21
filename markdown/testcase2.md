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