# Hangeul Design

Hangeul Design은 이미지, 영상, 3D 생성형 AI 작업을 위한 **한국어 우선 프롬프트 기획 도구**입니다.

누구나 내려받아 **개인적·비상업적 목적으로 무료 사용**할 수 있습니다. 상업적 사용은 허용하지 않으며 별도 허가가 필요합니다. 자세한 조건은 `LICENSE`를 확인하십시오.

> 이 프로젝트는 비상업 개인사용을 허용하는 source-available 프로젝트입니다. OSI가 정의하는 오픈소스 라이선스는 아닙니다.

## 주요 기능

- 한국어 주제 입력 기반 이미지·영상·3D 프롬프트 생성
- 전문가 모드 / 빠른 모드
- 목적별 빠른 프리셋과 작업 모드
- `구조`, `이미지`, `영상`, `3D` 결과 탭
- JPG, JPEG, PNG, BMP, WEBP, GIF, TIF/TIFF 참조 이미지 첨부
- 참조 이미지의 원본 정체성, 구도, 스타일 등을 선택적으로 유지
- Cinematic Product Video: 쇼트, 카메라 이동, 렌즈, 조명, 사람 등장·제품 상호작용 기반 영상 프롬프트
- 컨셉 스파인, 한글 문구, HEX 팔레트, 세트 일관성, 디테일 밀도 제어
- 생성 개수별 구도·조명·카메라·팔레트 변형
- 즐겨찾기/템플릿 로컬 저장 및 재적용
- 리포트 저장
- 한국어 주제 자동 영어 변환 옵션
- Windows `run.bat` 실행

## 참조 이미지

`run.bat` 또는 Cinematic 실행 화면에서 이미지를 첨부할 수 있습니다.

지원 형식:

`JPG / JPEG / PNG / BMP / WEBP / GIF / TIF / TIFF`

적용 방식:

- 원본 정체성 유지
- 원본 최대 유지
- 구도/배치 참고
- 스타일/분위기 참고

Hangeul Design에서는 이미지·영상·3D 프롬프트에 참조 이미지 제어 지시가 추가됩니다. Cinematic Product Video에서는 제품/인물의 정체성과 프레임 간 연속성을 유지하는 지시가 함께 추가됩니다.

이 앱 자체가 생성 AI에 이미지를 전송하거나 이미지를 생성하는 것은 아닙니다. 생성된 프롬프트와 첨부 원본을 참조 이미지 입력을 지원하는 생성 AI에서 함께 사용하는 방식입니다.

## 빠른 프리셋

- `한글 디자인`: 한글 타이포그래피, 한국적 레이아웃과 시각 정체성
- `매출형`: 제품·전환 중심 홍보 이미지
- `감성형`: 감성·라이프스타일 비주얼
- `트렌드`: SNS·트렌드 비주얼
- `브랜드 일관성`: 색상·소재·정체성을 유지하는 캠페인
- `숏폼 바이럴`: 세로형 숏폼 영상 프롬프트
- `시네마 영상형`: 시네마틱 영상·스토리보드
- `제품 상세형`: 제품 소재·매크로 디테일
- `캐릭터 IP형`: 캐릭터·마스코트·IP
- `화보 전문가형`: 인물·패션 에디토리얼

## 프롬프트 엔진

### 전문가 모드

컨셉 스파인, 피사체 특징, 장면, 조명, 팔레트, 카메라, 금지 요소를 구조화하여 장문 프롬프트를 만듭니다. `직접입력` 스타일을 선택하면 사용자가 입력한 스타일 문구가 실제 프롬프트에 반영됩니다.

### 빠른 모드

프리셋, 작업 모드, 스타일, 조명, 카메라를 조합하여 비교적 짧은 프롬프트를 만듭니다.

여러 기획안을 생성하면 단순 단어 몇 개만 바꾸는 방식이 아니라 구도, 조명, 카메라, 팔레트 변형 축을 배분하여 비교 가능한 결과를 만듭니다.

## 설치

권장 환경:

- Windows 10 이상
- Python 3.10 이상
- Streamlit 1.50 이상, 2.0 미만

```bat
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 실행

Hangeul Design + 참조 이미지:

```bat
run.bat
```

Cinematic 통합 테스트 버전:

```bat
run_cinematic.bat
```

기본 주소:

```text
http://localhost:8504
```

## 테스트

```text
python -m pytest -q
```

GitHub Actions에서는 Ubuntu에서 회귀 테스트와 Streamlit `AppTest`를 실행합니다. 문법 검사만 하는 CI가 아니라 실제 앱 엔트리 포인트를 실행해 예외 발생 여부를 검사합니다.

## 실행파일 런처

`launcher.py`는 frozen EXE가 자기 자신을 다시 실행하지 않도록 프로젝트의 `venv` Python을 사용합니다. 따라서 런처 EXE는 독립형 프로그램이 아니며 프로젝트 폴더와 `venv`가 필요합니다. 일반 사용에는 `run.bat`를 권장합니다.

## 프로젝트 구조

```text
hangeul-design/
├─ .github/workflows/
│  └─ smoke-test.yml
├─ tests/
│  └─ test_prompt_quality.py
├─ app.py
├─ app_reference.py
├─ app_cinematic.py
├─ cinematic_product.py
├─ reference_image.py
├─ runtime_quality.py
├─ launcher.py
├─ requirements.txt
├─ run.bat
├─ run_cinematic.bat
├─ LICENSE
├─ README.md
└─ CHANGELOG.md
```

## 번역 및 데이터

한국어→영어 자동 변환은 비공식 Google 번역 엔드포인트를 사용합니다. ASCII/영어 입력은 번역 서버에 보내지 않으며, 같은 실행 세션의 번역 결과는 캐시합니다. 번역에 실패하면 원문을 유지하고 사용자에게 알립니다.

즐겨찾기는 사용자 홈의 `.hangeul_design` 영역에 로컬 JSON으로 저장합니다. 저장 실패 시 성공으로 표시하지 않고 오류를 표시하도록 구성했습니다.

## 라이선스

**개인·비상업적 사용은 누구나 무료로 허용합니다.**

허용:
- 개인 PC에서 다운로드 및 실행
- 개인 학습·연구·실험
- 개인적인 비상업 프로젝트에서 사용
- 개인 용도로 코드 수정

금지(별도 서면 허가가 없는 경우):
- 소프트웨어 판매
- 유료 서비스·구독 서비스에 포함
- 기업·사업자의 영리 업무 또는 수익 창출을 주목적으로 사용
- 수정판의 상업적 배포

전체 조건은 [`LICENSE`](LICENSE)를 따릅니다.

Copyright © 2026 Jeon Youngshin.
