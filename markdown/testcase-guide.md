# 자비스 AI 프레임워크 단위 테스트 가이드
## 코드 구현 완료 후 테스트 케이스 작성

코드 구현이 완료되면 지금 이 문서는 가이드라인이므로 이 문서에 작성하지 말고 "./markdown/testcase2.md" 파일을 로드하여 관련된 테스트 케이스를 추가 작성합니다:

1. **모듈별 테스트 케이스 식별**:
   - 구현된 각 모듈/클래스/함수에 대한 테스트 케이스 목록 작성
   - 정상 동작 케이스와 예외 케이스를 모두 포함
   - 각 테스트 케이스 옆에 체크박스 배치 (`[ ]`)

2. **우선순위 결정**:
   - 핵심 기능에 대한 테스트 케이스 우선
   - 복잡한 로직이나 오류 가능성이 높은 부분 중점
   - 의존성 순서를 고려하여 배치

3. **테스트 케이스 상세화**:
   - 각 테스트 케이스의 입력값, 예상 결과, 검증 방법 명시
   - 경계 조건 및 특수 상황에 대한 테스트 케이스 추가
   - 모킹이 필요한 외부 의존성 식별

4. **테스트 코드 구현 및 실행**:
   - 식별된 테스트 케이스를 pytest 코드로 구현
   - 해당 항목의 테스트 코드 실행

5. **테스트 케이스 업데이트**:
   - 테스트 성공 시 해당 테스트 케이스 체크박스 표시 (`[ ]` → `[X]`)
   - 테스트 실패 시 해당 테스트 케이스 체크박스 초기화

5. **테스트 커버리지 확인**:
   - pytest-cov를 사용하여 코드 커버리지 측정
   - 커버리지가 낮은 부분 식별하여 추가 테스트 케이스 작성

## 테스트 준비

### 1. 테스트 환경 설정

1. 격리된 테스트 환경을 구성합니다.
   - 필요한 의존성 설치
   - 테스트 전용 환경 변수 설정 (API 키 등)

2. 테스트 프레임워크 설치:
   - pytest 설치: `pip install pytest pytest-cov`
   - 필요시 추가 플러그인 설치 (예: pytest-mock, pytest-asyncio)

### 2. 테스트 구조화

**참고:** 모든 테스트 관련 파일은 프로젝트 루트 디렉토리 (`theme_news_agent` 디렉토리와 동일한 레벨)에 위치한 `tests/` 디렉토리 내에 구성합니다.

각 컴포넌트/모듈별로 테스트 파일을 구성합니다:

1. 파일 명명 규칙: `test_[모듈명].py` (예: `tests/test_directory_structure.py`)
2. 테스트 클래스/함수 명명 규칙: `Test[클래스명]` / `test_[함수명]`
3. 각 테스트는 독립적으로 실행 가능해야 합니다.
4. 필요한 경우 fixtures를 사용하여 테스트 환경을 설정합니다.

## 단위 테스트 작성 가이드

### 1. 기본 테스트 구조

```python
# 테스트 파일의 기본 구조 예시
import pytest
from [패키지] import [테스트할_모듈]

def test_기능명():
    # 준비 (Arrange)
    # 실행 (Act)
    # 검증 (Assert)
```

### 2. 테스트 유형별 접근 방법

1. **클래스/객체 테스트**:
   - 객체 초기화 테스트
   - 메서드 동작 테스트
   - 상태 변화 테스트

2. **함수 테스트**:
   - 입력-출력 검증
   - 예외 처리 검증
   - 경계값 테스트

3. **비동기 코드 테스트**:
   - pytest-asyncio 사용
   - 코루틴 함수 테스트 방법

4. **외부 의존성 모킹**:
   - API 호출 모킹
   - 데이터베이스 연결 모킹
   - 파일 시스템 모킹

## 모듈별 테스트 전략

### 1. 핵심 컴포넌트 테스트

각 핵심 컴포넌트마다 다음 측면을 테스트합니다:

1. **기본 초기화 및 구성**:
   - 올바른 설정으로 인스턴스가 생성되는지 확인
   - 기본값이 예상대로 설정되는지 확인

2. **주요 메서드 동작**:
   - 각 메서드가 예상 입력에 대해 올바른 출력을 생성하는지 확인
   - 유효하지 않은 입력에 대한 오류 처리 확인

3. **상태 관리**:
   - 내부 상태가 예상대로 변경되는지 확인
   - 부작용이 없는지 확인

4. **통합 지점**:
   - 다른 컴포넌트와의 인터페이스가 올바르게 작동하는지 확인

### 2. 도구 및 유틸리티 테스트

1. **독립적인 기능 테스트**:
   - 각 함수가 독립적으로 올바르게 작동하는지 확인

2. **오류 조건 테스트**:
   - 경계 조건 및 예외 사례 확인

### 3. 에이전트 테스트

1. **초기화 및 구성**:
   - 에이전트가 올바른 설정으로 생성되는지 확인

2. **메시지 처리**:
   - 모의 메시지에 대한 응답이 예상대로인지 확인

3. **도구 사용**:
   - 도구 호출 및 결과 처리가
   올바르게 이루어지는지 확인

## 테스트 실행 및 관리

### 1. 테스트 실행 방법

**참고:** 모든 `pytest` 명령은 프로젝트 루트 디렉토리 (예: `/home/jhbum01/project/custom_agent/theme_news`)에서 실행해야 합니다. `theme_news_agent` 디렉토리 내부에서 실행하면 `tests` 디렉토리를 찾지 못할 수 있습니다.

1. 전체 테스트 실행:
   ```bash
   # 프로젝트 루트에서 실행
   pytest tests/
   ```

2. 특정 모듈만 테스트:
   ```bash
   # 프로젝트 루트에서 실행
   pytest tests/test_특정모듈.py
   ```

3. 특정 테스트 함수만 실행:
   ```bash
   # 프로젝트 루트에서 실행
   pytest tests/test_특정모듈.py::test_특정함수
   ```

4. 커버리지 리포트 생성:
   ```bash
   # 프로젝트 루트에서 실행
   pytest --cov=theme_news_agent tests/
   ```

### 2. 테스트 결과 해석

1. 통과/실패 요약 확인
2. 실패한 테스트의 오류 메시지 분석
3. 커버리지 리포트 검토

### 3. 테스트 실패 대응

테스트 실패 시 다음 단계를 따릅니다:

1. 실패한 테스트의 오류 메시지 분석
2. 관련 코드 검토 및 수정
3. TODO.md 파일에서 "0. 프로젝트 초기 설정"를 제외한 모든 체크박스를 초기화**하고 처음부터 다시 테스트 실행
4. 모든 테스트가 통과할 때까지 반복

## 체크리스트 사용법

테스트 과정을 추적하기 위해 체크리스트 방식을 사용합니다:

1. 테스트 항목 옆에 체크박스를 배치합니다 (빈 대괄호 사용).
2. 테스트가 성공적으로 통과하면 대괄호 안에 X 표시를 합니다.
3. **중요**: 어느 하나의 테스트라도 실패할 경우, 모든 체크박스를 초기화하고 첫 번째 테스트부터 다시 시작해야 합니다.
4. 테스트를 진행할 단계가 아닌 경우(예: 현재 구현되지 않은 기능, 아직 의존성이 준비되지 않은 기능), X 대신 대괄호 안에 `-` 표시를 합니다. 이렇게 하면 아직 테스트할 준비가 되지 않은 항목을 구분할 수 있습니다.

## 모범 사례

1. **테스트 독립성 유지**:
   - 각 테스트는 다른 테스트와 독립적으로 실행 가능해야 함
   - 테스트 간 상태 공유 금지

2. **테스트 가독성 향상**:
   - 명확한 테스트 이름 사용
   - 각 테스트가 하나의 기능만 검증하도록 구성
   - AAA 패턴 사용 (Arrange-Act-Assert)

3. **효율적인 모킹**:
   - 외부 의존성은 항상 모킹
   - 모의 객체의 동작을 명확히 정의

4. **테스트 유지 관리**:
   - 코드 변경 시 관련 테스트도 함께 업데이트
   - 주기적인 테스트 리팩토링

## 결론

체계적인 단위 테스트는 자비스 AI 프레임워크의 안정성과 품질을 보장하는 핵심입니다. 이 가이드에 따라 테스트를 작성하고 실행함으로써 구현된 코드가 예상대로 작동하는지 확인할 수 있습니다.

테스트를 진행할 때는 반드시 체크리스트를 활용하여 진행 상황을 추적하고, 어떤 테스트라도 실패할 경우 모든 체크리스트를 초기화하고 처음부터 다시 시작해야 함을 명심하세요. 