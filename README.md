# Hangeul Design

Hangeul Design은 이미지, 영상, 3D 생성형 AI 작업을 위한 **한국어 우선 프롬프트 기획 도구**입니다.

누구나 내려받아 **개인적·비상업적 목적으로 무료 사용**할 수 있습니다. 상업적 사용은 별도 허가가 필요합니다. 자세한 조건은 `LICENSE`를 확인하십시오.

## v1.2 개발 기능

- **초보자 자동 설정:** `무엇을 만들지 / 어디에 쓸지 / 어떤 느낌인지` 세 가지 답으로 작업 모드, 스타일, 화면비, 조명 등을 자동 추천합니다.
- **이미지 생성 AI 컴파일러:** ChatGPT/Gemini, Midjourney, Stable Diffusion/FLUX에 맞춰 프롬프트 문법을 변환합니다.
- **영상 생성 AI 컴파일러:** General, Veo, Sora, Runway, Kling용 실행 지시와 화면비를 메인 영상 프롬프트에 적용합니다.
- **화면비 직접 선택:** 1:1, 16:9, 9:16, 4:5, 3:2, 21:9를 생성 AI 설정에서 직접 바꿀 수 있습니다.
- **한글 타이포그래피 충돌 방지:** 의도한 한글이 있을 때 blanket `exclude text/letters` 금지어를 제거합니다.
- **한글 기대 관리:** 생성 모델의 한글 렌더링이 불안정할 수 있으므로, 정확한 문구가 중요하면 글자 없는 비주얼을 생성한 뒤 Canva·미리캔버스 등에서 한글을 얹는 방법을 안내합니다.
- **참조 이미지:** 컴파일 후 참조 지시를 붙여 네거티브 추출과 충돌하지 않으며, 실제 생성 AI에서도 같은 이미지를 함께 첨부하도록 안내합니다.

## 주요 기능

- 한국어 주제 입력 기반 이미지·영상·3D 프롬프트 생성
- 전문가 모드 / 빠른 모드
- 목적별 빠른 프리셋과 작업 모드
- `구조`, `이미지`, `영상`, `3D` 결과 탭
- JPG, JPEG, PNG, BMP, WEBP, GIF, TIF/TIFF 참조 이미지 첨부
- Cinematic Product Video: 쇼트, 카메라 이동, 렌즈, 조명, 사람 등장·제품 상호작용 기반 영상 프롬프트
- 컨셉 스파인, 한글 문구, HEX 팔레트, 세트 일관성, 디테일 밀도 제어
- 생성 개수별 구도·조명·카메라·팔레트 변형
- 즐겨찾기/템플릿 로컬 저장 및 재적용
- 리포트 저장

## 실행

Windows PowerShell에서 프로젝트 폴더로 이동한 뒤 실행합니다.

기본 Hangeul Design (8504):

```powershell
.\run.bat
```

Cinematic 통합 버전 (8505):

```powershell
.\run_cinematic.bat
```

종료:

```powershell
.\stop.bat
.\stop_cinematic.bat
```

두 실행 화면 모두 초보자 자동 설정, 이미지/영상 생성 AI 선택, 화면비 선택, 참조 이미지 기능을 제공합니다. Cinematic 버전에는 별도의 Cinematic Product Video 도구가 추가됩니다.

## 설치

권장 환경:

- Windows 10 이상
- Python 3.10 이상
- Streamlit 1.55 이상, 2.0 미만

```bat
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 참조 이미지

지원 형식: `JPG / JPEG / PNG / BMP / WEBP / GIF / TIF / TIFF`

적용 방식은 원본 정체성 유지, 원본 최대 유지, 구도/배치 참고, 스타일/분위기 참고입니다. Hangeul Design 자체가 이미지를 생성 AI로 전송하지는 않습니다. 생성된 프롬프트를 사용할 때 **같은 참조 이미지를 생성 AI에도 함께 첨부**해야 합니다.

## 테스트

```text
python -m pytest -q
```

GitHub Actions에서는 Ubuntu에서 회귀 테스트와 Streamlit `AppTest`를 실행합니다.

## 프로젝트 구조

```text
hangeul-design/
├─ .github/workflows/smoke-test.yml
├─ tests/test_prompt_quality.py
├─ app.py
├─ app_reference.py
├─ app_cinematic.py
├─ beginner_mode.py
├─ prompt_compiler.py
├─ cinematic_product.py
├─ reference_image.py
├─ runtime_quality.py
├─ launcher.py
├─ requirements.txt
├─ run.bat / stop.bat
├─ run_cinematic.bat / stop_cinematic.bat
├─ LICENSE
├─ README.md
└─ CHANGELOG.md
```

## 라이선스

**개인·비상업적 사용은 누구나 무료로 허용합니다.** 기업·사업자의 영리 업무, 판매, 유료 서비스 포함 등 상업적 사용은 별도 서면 허가가 필요합니다. 전체 조건은 `LICENSE`를 따릅니다.

Copyright © 2026 Jeon Youngshin.
