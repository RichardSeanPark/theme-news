import json
import asyncio # 비동기 모킹을 위해 추가
from unittest.mock import patch, MagicMock
import pytest
from theme_news_agent.sub_agents.keyword_extraction.agent import KeywordExtractionAgent
from theme_news_agent.sub_agents.data_collection.models import CollectedData, ArticleData # 테스트 데이터 생성을 위해 임포트
from google.adk.agents.invocation_context import InvocationContext
from google.adk.models.llm_request import LlmRequest # LlmRequest 타입 힌트 및 확인용


def test_keyword_extraction_agent_initialization():
    """KeywordExtractionAgent 객체가 기본 인자로 정상적으로 생성되는지 확인합니다."""
    try:
        agent = KeywordExtractionAgent()
        assert agent is not None, "KeywordExtractionAgent 객체 생성에 실패했습니다."
    except Exception as e:
        pytest.fail(f"KeywordExtractionAgent 초기화 중 예외 발생: {e}")

def test_keyword_extraction_agent_attributes():
    """KeywordExtractionAgent 객체 생성 시 속성이 올바른 값으로 설정되었는지 확인합니다."""
    agent = KeywordExtractionAgent()
    assert agent.name == "KeywordExtractor", f"Expected name 'KeywordExtractor', but got '{agent.name}'"
    assert agent.description == "텍스트에서 주요 키워드를 추출하는 에이전트", \
           f"Expected description '텍스트에서 주요 키워드를 추출하는 에이전트', but got '{agent.description}'"
    assert agent.model == "gemini-2.5-flash", f"Expected model 'gemini-2.5-flash', but got '{agent.model}'"
    # instruction은 이제 prompt 함수에서 관리되므로, 기본값 또는 빈 값 확인
    assert agent.instruction == "", f"Expected empty instruction, but got '{agent.instruction}'"

# --- process 메서드 테스트 --- #

@pytest.fixture
def mock_context() -> MagicMock:
    """테스트용 InvocationContext 모의 객체를 생성합니다."""
    context = MagicMock(spec=InvocationContext)
    context.state = {} # 상태를 빈 딕셔너리로 초기화
    return context

@pytest.fixture
def sample_collected_data_dict() -> dict:
    """테스트용 CollectedData 딕셔너리를 생성합니다."""
    article1 = ArticleData(title="테스트 기사 1", content="키워드1 관련 내용", source="test_source", published="2024-01-01T00:00:00Z", url="http://example.com/1")
    article2 = ArticleData(title="테스트 기사 2", content="키워드2에 대한 정보", source="test_source", published="2024-01-02T00:00:00Z", url="http://example.com/2")
    collected_data = CollectedData(newsapi_articles=[article1.model_dump()], nytimes_articles=[article2.model_dump()])
    return collected_data.model_dump()

@pytest.mark.asyncio
async def test_process_missing_collected_data(mock_context):
    """3.3.1: ctx.state에 collected_data가 없을 때 오류 메시지를 반환하는지 테스트합니다."""
    agent = KeywordExtractionAgent()
    # process가 비동기 함수로 변경되었으므로 await 사용
    result = await agent.process(mock_context)
    assert "오류: 키워드 추출을 위한 수집된 데이터(collected_data)가 상태에 없습니다." in result
    assert "extracted_keywords_raw" not in mock_context.state

@pytest.mark.asyncio
async def test_process_no_articles_in_collected_data(mock_context):
    """3.3.2: collected_data는 있지만 기사가 없을 때 적절히 처리하는지 테스트합니다."""
    agent = KeywordExtractionAgent()
    empty_data = CollectedData().model_dump()
    mock_context.state["collected_data"] = empty_data
    result = await agent.process(mock_context)
    assert "추출할 기사가 없습니다" in result
    assert mock_context.state.get("extracted_keywords_raw") == []

# --- Helper for async generator mocking --- #
async def async_generator_from_list(items):
    for item in items:
        yield item
        await asyncio.sleep(0) # Give control back to the event loop

# --- Tests for process method --- #

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies') # Mock frequency calc
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_success_with_mocked_llm(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict):
    """3.3.3: 정상 처리 및 LLM 응답 파싱 성공 테스트 (상태 저장 방식 변경 반영)."""
    # --- Mock LLM --- #
    mock_llm_instance = MagicMock()
    mock_llm_text_response = '```json\n["키워드1", "키워드2", "테스트 기사"]\n```'
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Mock calculate_keyword_frequencies --- #
    expected_frequency_results = [
        {"keyword": "키워드1", "frequency": {"total": 1, "test_source": 1}},
        {"keyword": "키워드2", "frequency": {"total": 1, "test_source": 1}},
        {"keyword": "테스트 기사", "frequency": {"total": 0}} # 예시 빈도
    ]
    mock_calc_freq.return_value = expected_frequency_results

    # --- Agent setup --- #
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process --- #
    result = await agent.process(mock_context)

    # --- Assertions --- #
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()
    call_args, _ = mock_llm_instance.generate_content_async.call_args
    llm_request_arg = call_args[0]
    assert isinstance(llm_request_arg, LlmRequest)
    assert "테스트 기사 1" in llm_request_arg.contents[0].parts[0].text
    assert "추출된 키워드 (JSON 리스트):" in llm_request_arg.contents[0].parts[0].text

    # Verify calculate_keyword_frequencies was called
    extracted_keywords = ["키워드1", "키워드2", "테스트 기사"]
    collected_data_obj = CollectedData(**sample_collected_data_dict)
    mock_calc_freq.assert_called_once_with(extracted_keywords, collected_data_obj)

    # Verify state update (keyword_results 확인)
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == expected_frequency_results
    assert mock_context.state.get("extracted_keywords_raw") is None # 더 이상 사용되지 않음

    # Verify return message
    assert "키워드 추출 및 빈도 계산 완료" in result
    assert "3개 키워드 처리됨" in result

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies') # Mock freq calc
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_llm_response_parsing_failure(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict, caplog):
    """3.3.4: LLM 응답 파싱 실패 시 처리 테스트 (상태 저장 방식 변경 반영)."""
    # --- Mock LLM --- #
    mock_llm_instance = MagicMock()
    mock_llm_text_response = '이것은 JSON이 아닙니다.'
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Agent setup --- #
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process --- #
    result = await agent.process(mock_context)

    # --- Assertions --- #
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()
    # Verify frequency calculation was NOT called
    mock_calc_freq.assert_not_called()

    # Verify logs
    assert "LLM 응답에서 유효한 JSON 리스트를 찾지 못했습니다" in caplog.text

    # Verify state update (should store empty list in keyword_results)
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == []
    assert mock_context.state.get("extracted_keywords_raw") is None

    # Verify return message
    assert "키워드 추출 및 빈도 계산 완료" in result
    assert "0개 키워드 처리됨" in result

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies') # Mock freq calc
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_llm_response_invalid_json_structure(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict, caplog):
    """3.3.4 (추가): LLM 응답이 JSON이지만 리스트가 아닐 때 (상태 저장 방식 변경 반영)."""
    # --- Mock LLM --- #
    mock_llm_instance = MagicMock()
    mock_llm_text_response = '{"key": "value"}' # 리스트가 아닌 JSON
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Agent setup --- #
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process --- #
    result = await agent.process(mock_context)

    # --- Assertions --- #
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()
    # Verify frequency calculation was NOT called
    mock_calc_freq.assert_not_called()

    # Verify logs
    assert "LLM 응답에서 유효한 JSON 리스트를 찾지 못했습니다" in caplog.text

    # Verify state update (should store empty list in keyword_results)
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == []
    assert mock_context.state.get("extracted_keywords_raw") is None

    # Verify return message
    assert "키워드 추출 및 빈도 계산 완료" in result
    assert "0개 키워드 처리됨" in result

@pytest.mark.asyncio
@patch('google.adk.models.registry.LLMRegistry.new_llm') # new_llm 직접 패치
async def test_process_llm_call_failure(mock_new_llm, mock_context, sample_collected_data_dict): # mock_new_llm 파라미터 추가
    """3.3.5: LLM 호출 실패 시 처리 테스트 (모킹 수정)."""
    mock_llm_instance = MagicMock()
    mock_exception = Exception("LLM API 통신 오류")
    mock_llm_instance.generate_content_async.side_effect = mock_exception
    mock_new_llm.return_value = mock_llm_instance

    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    result = await agent.process(mock_context)

    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()
    assert mock_context.state.get("extracted_keywords_raw") == []
    assert "LLM 호출 중 오류 발생" in result
    assert "LLM API 통신 오류" in result

# --- Tests for State Management (TODO 3.5) --- #

@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies')
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_stores_keyword_results(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict):
    """3.5.1: 성공 시 계산된 키워드 빈도 결과가 상태에 저장되는지 테스트합니다."""
    # --- Mock LLM ---
    mock_llm_instance = MagicMock()
    mock_llm_text_response = '```json\n["ai", "ml"]\n```'
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Mock calculate_keyword_frequencies ---
    expected_frequency_results = [
        {"keyword": "ai", "frequency": {"total": 5, "newsapi": 2, "nytimes": 3}},
        {"keyword": "ml", "frequency": {"total": 2, "newsapi": 1, "nytimes": 1}}
    ]
    mock_calc_freq.return_value = expected_frequency_results

    # --- Agent setup ---
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process ---
    result = await agent.process(mock_context)

    # --- Assertions ---
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()

    # Verify calculate_keyword_frequencies was called correctly
    extracted_keywords = ["ai", "ml"]
    collected_data_obj = CollectedData(**sample_collected_data_dict) # Pass the object
    mock_calc_freq.assert_called_once_with(extracted_keywords, collected_data_obj)

    # Verify state update
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == expected_frequency_results
    assert mock_context.state.get("extracted_keywords_raw") is None # Should not be set anymore

    # Verify return message
    assert "키워드 추출 및 빈도 계산 완료" in result
    assert "2개 키워드 처리됨" in result


@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies')
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_stores_empty_results_if_no_keywords(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict):
    """3.5.2: LLM이 빈 키워드 리스트를 반환했을 때 빈 결과가 저장되는지 테스트합니다."""
    # --- Mock LLM ---
    mock_llm_instance = MagicMock()
    # Return empty list in JSON format
    mock_llm_text_response = '```json\n[]\n```'
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Agent setup ---
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process ---
    result = await agent.process(mock_context)

    # --- Assertions ---
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()

    # calculate_keyword_frequencies should NOT be called
    mock_calc_freq.assert_not_called()

    # Verify state update
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == [] # Expect empty list
    assert mock_context.state.get("extracted_keywords_raw") is None # Should not be set

    # Verify return message
    assert "키워드 추출 및 빈도 계산 완료" in result # Message still indicates completion
    assert "0개 키워드 처리됨" in result


@pytest.mark.asyncio
@patch('theme_news_agent.sub_agents.keyword_extraction.agent.calculate_keyword_frequencies')
@patch('google.adk.models.registry.LLMRegistry.new_llm')
async def test_process_stores_empty_results_on_freq_calc_error(mock_new_llm, mock_calc_freq, mock_context, sample_collected_data_dict, caplog):
    """3.5.3: 빈도 계산 중 예외 발생 시 빈 결과가 저장되는지 테스트합니다."""
    # --- Mock LLM ---
    mock_llm_instance = MagicMock()
    mock_llm_text_response = '```json\n["error_trigger"]\n```'
    mock_response = MagicMock()
    mock_response.text = mock_llm_text_response
    mock_llm_instance.generate_content_async.return_value = async_generator_from_list([mock_response])
    mock_new_llm.return_value = mock_llm_instance

    # --- Mock calculate_keyword_frequencies to raise an exception ---
    calc_exception = Exception("Frequency calculation failed!")
    mock_calc_freq.side_effect = calc_exception

    # --- Agent setup ---
    agent = KeywordExtractionAgent()
    mock_context.state["collected_data"] = sample_collected_data_dict

    # --- Run process ---
    result = await agent.process(mock_context)

    # --- Assertions ---
    mock_new_llm.assert_called_once_with(agent.model)
    mock_llm_instance.generate_content_async.assert_called_once()

    # Verify calculate_keyword_frequencies was called
    extracted_keywords = ["error_trigger"]
    collected_data_obj = CollectedData(**sample_collected_data_dict)
    mock_calc_freq.assert_called_once_with(extracted_keywords, collected_data_obj)

    # Verify error log
    assert "키워드 빈도 계산 중 오류 발생" in caplog.text
    assert "Frequency calculation failed!" in caplog.text # Check for the specific exception message

    # Verify state update
    assert "keyword_results" in mock_context.state
    assert mock_context.state["keyword_results"] == [] # Expect empty list due to error
    assert mock_context.state.get("extracted_keywords_raw") is None # Should not be set

    # Verify return message (still indicates completion, but mentions the number of keywords processed *before* the error)
    assert "키워드 추출 및 빈도 계산 완료" in result
    assert "1개 키워드 처리됨" in result # Reflects keywords extracted before the frequency error 