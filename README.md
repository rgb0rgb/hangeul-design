# Hangeul Design

Hangeul Design은 이미지, 영상, 3D 생성형 AI 작업을 위한 한국어 우선 프롬프트 기획 도구입니다.

기존 DesignPD를 그대로 보존하고, 새 프로젝트로 분리해 한글 디자인과 전문가형 프롬프트 구조를 강화했습니다.

## 주요 기능

- 한국어 주제 입력 기반 프롬프트 생성
- 빠른 프리셋 기반 작업 흐름
- 전문가 모드 기반 장문 구조화 프롬프트
- `구조`, `이미지`, `영상`, `3D` 결과 탭
- 한글 타이포그래피와 한국적 에디토리얼 스타일
- 컨셉 스파인, 정확한 한글 문구, HEX 팔레트, 세트 일관성, 디테일 밀도 제어
- 즐겨찾기/템플릿 로컬 저장
- 리포트 저장
- 한국어 주제 자동 영어 변환 옵션
- Windows `run.bat` 실행
- Windows 실행파일 런처 빌드 지원

## 빠른 프리셋

- `한글 디자인`: Hangul typography, Korean layout, poster, and visual identity work
- `매출형`: Product and conversion-focused promotional images
- `감성형`: Warm, emotional, lifestyle-oriented visuals
- `트렌드`: Trend-forward social visuals
- `브랜드 일관성`: Campaign visuals with consistent palette and identity
- `숏폼 바이럴`: Short-form video and vertical-hook prompt planning
- `시네마 영상형`: Cinematic video and storyboard prompts
- `제품 상세형`: Macro product detail and material-focused prompts
- `캐릭터 IP형`: Character, mascot, and IP concept prompts
- `화보 전문가형`: Editorial portrait and fashion prompt structure

## 프롬프트 엔진

### 전문가 모드

품질과 일관성이 중요한 작업을 위한 장문 구조화 프롬프트를 만듭니다. 주제의 핵심 의도, 피사체 특징, 장면, 조명, 팔레트, 카메라, 금지 요소를 함께 반영합니다.

주요 입력값:

- `컨셉 스파인`: 결과가 흔들리지 않도록 잡아주는 한 문장짜리 핵심 의도입니다.
- `정확한 한글 문구`: 이미지 안에 넣고 싶은 한글 문구입니다. 실제 글자 정확도는 사용하는 생성 모델에 따라 달라집니다.
- `색상/HEX 팔레트`: 결과 전체에 반복할 색상 규칙입니다.
- `세트 일관성 유지`: 여러 장을 만들 때 피사체, 소재, 색상 규칙을 유지합니다.
- `디테일 밀도`: 프롬프트가 얼마나 자세하게 작성될지 조절합니다.

### 빠른 모드

선택한 프리셋, 작업 모드, 이미지 스타일, 조명, 카메라 앵글을 조합해 짧은 프롬프트를 만듭니다. 빠른 초안이나 간단한 시안 탐색에 적합합니다.

## 설치

필요 환경:

- Windows 10 or newer
- Python 3.10 or newer

수동 설치:

```bat
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

## 실행

Windows에서:

```bat
run.bat
```

브라우저 주소:

```text
http://localhost:8504
```

`run.bat`는 Streamlit 설치 상태를 확인합니다. 로컬 가상환경이 깨져 있으면 `requirements.txt` 기준으로 강제 재설치합니다.

## Windows 실행파일 빌드

```bat
build_exe_launcher.bat
```

생성 위치:

```text
dist\HangeulDesign_Streamlit_Launcher.exe
```

이 실행파일은 Streamlit 앱을 실행하는 작은 런처입니다. 단독 앱 번들이 아니므로 `app.py`와 프로젝트 파일을 같은 폴더에 유지해야 합니다.

## 프로젝트 구조

```text
HangeulDesign_Streamlit_UI/
├─ app.py
├─ requirements.txt
├─ run.bat
├─ launcher.py
├─ build_exe_launcher.bat
├─ README.md
├─ README.txt
└─ CHANGELOG.md
```

`venv/`, `build/`, `dist/` 같은 생성 폴더는 `.gitignore`에서 제외합니다.

## 참고

- 이 앱은 프롬프트 생성 도구입니다. 이미지나 영상을 직접 생성하지 않습니다.
- 구글 번역 옵션은 비공식 엔드포인트를 사용하므로 실패할 수 있습니다.
- 한글 문구의 정확한 렌더링은 프롬프트를 붙여 넣는 이미지/영상 생성 모델의 성능에 따라 달라집니다.
- 최종 상업 디자인에서는 글자와 타이포그래피를 별도 디자인 도구에서 검수하는 것이 안전합니다.

## 라이선스

아직 오픈소스 라이선스를 추가하지 않았습니다. 소유자가 별도 라이선스를 명시하기 전까지 모든 권리는 보유됩니다.
