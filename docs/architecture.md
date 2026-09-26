---
noteId: "1a23f6e0b9c011f19627c33cf2aff401"
tags: []
---

# Project Architecture

## 1. 전체 처리 흐름

학생 답안지 PDF 자동 분류 프로그램의 기본 처리 흐름은 다음과 같다.

1. 입력 폴더 확인
2. 입력 폴더명에서 반 또는 특강 학교 정보 추출
3. PDF 파일 목록 탐색
4. 각 PDF의 첫 페이지를 OCR 대상으로 전송
5. OCR 결과에서 학생 이름과 학교명 추출
6. 기존 학생 폴더 목록과 비교
7. 학생 식별 결과에 따라 분류 상태 결정
8. PDF를 학생 폴더, 보류 폴더, 신규생 폴더 중 하나로 이동
9. 처리 결과를 로그로 기록

---

## 2. 초기 모듈 구조

````text
src/
└── answer_classifier/
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── input_parser.py
    ├── pdf_reader.py
    ├── ocr_client.py
    ├── student_repository.py
    ├── classifier.py
    ├── file_manager.py
    └── logger.py

---

## 3. 초기 모듈 구조

1. main.py
프로그램 전체 실행 흐름을 제어한다.
직접 OCR 처리나 파일 탐색 로직을 수행하지 않고,
각 모듈을 호출하여 작업 순서를 조정한다.

2.config.py
프로그램 설정값을 관리한다.
예:
- CLOVA OCR API URL
- CLOVA OCR Secret Key
- 학생별 답안지 기본 경로
- 로그 경로
- 추후 OCR confidence threshold

3.input_parser.py
입력 폴더명을 분석한다.
입력 폴더명에서 다음 정보를 판별한다.
- S반
- Y반
- 특강 학교명

4.pdf_reader.py
PDF 파일과 관련된 처리를 담당한다.
초기 단계에서는 다음 기능을 담당한다.
- 입력 폴더의 PDF 파일 탐색
- OCR에 전달할 PDF 준비

5.ocr_client.py
CLOVA OCR API와 통신한다.
책임:
- API 요청 생성
- PDF 전송
- API 응답 수신
- 오류 처리
OCR 결과를 바탕으로 학생을 직접 분류하지 않는다.

6.student_repository.py
기존 학생 폴더 정보를 조회한다.
책임:
- 학생 이름 폴더 탐색
- 동일 이름 학생 검색
- 반별 학생 목록 조회
- 특강 학생 폴더 조회

7.classifier.py
학생 분류 판단을 담당한다.
입력 예:
- OCR로 읽은 학생 이름
- OCR로 읽은 학교명
- 기존 학생 후보
- confidence 정보
출력 예:
- CLASSIFIED
- REVIEW
- NEW_STUDENT

8.file_manager.py
분류 결과에 따라 실제 PDF 파일을 이동한다.
책임:
- 학생 폴더로 이동
- 보류 폴더로 이동
- 신규생 폴더로 이동
- 파일 이름 충돌 처리

9.logger.py
프로그램 실행 결과를 기록한다.
예:
- 처리한 PDF 수
- 자동 분류 성공 수
- 보류 수
- 신규생 수
- 오류 발생 수
- PDF별 분류 결과
- 처리 시간

__

## 4. 설계 원칙

1. 책임 분리
각 모듈은 하나의 주요 책임을 가진다.
예를 들어 OCR API 호출 코드는 학생 폴더를 직접 탐색하지 않는다.

2. 판단과 실행 분리
classifier는 어디로 분류해야 하는지만 판단한다.
실제 파일 이동은 file_manager가 담당한다.
이렇게 하면 분류 로직 테스트 시 실제 파일을 이동하지 않고도
판단 결과만 검증할 수 있다.

3. 외부 API와 내부 로직 분리
CLOVA OCR API가 변경되더라도
학생 분류 로직 전체를 수정하지 않도록 OCR 관련 처리를 분리한다.

4. 임의 분류 금지
분류 결과가 불확실한 경우 임의 분류하지 않고 REVIEW로 처리한다.

## 5. 추후 변경 가능성

프로젝트 진행 과정에서 실제 코드의 책임이 명확해지면
모듈을 추가하거나 통합할 수 있다.
초기 구조를 절대적인 구조로 고정하지 않고,
실제 구현과 테스트 과정에서 필요한 근거가 생겼을 때 리팩터링한다.

여기서 중요한 설계 :

`classifier.py`와 `file_manager.py`를 분리

잘못된 구조 예시 :
```python
if student_found:
    shutil.move(...)

판단과 파일 이동이 같은 함수 안에 들어가면 나중에 테스트하기 불편하다.

우리는 개념적으로:
classifier
    ↓
"이 학생은 CLASSIFIED이고 대상 폴더는 김민수"
    ↓
file_manager
    ↓
실제 파일 이동

처럼 분리할 것이다.

나중에 단위 테스트를 만들 때 큰 장점이 될 것이다.
````
