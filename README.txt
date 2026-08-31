Hangeul Design - Streamlit UI v1.0

기존 DesignPD를 보존하고 새 폴더에서 진행하는 한국어 우선 프롬프트 기획 도구입니다.

핵심 기능
1) 전문가 모드
- 컨셉 스파인, 주체/디테일 앵커, 장면 레이어, 조명, 팔레트, 카메라, 네거티브 제어를 구조화합니다.
- 이미지, 영상, 3D 프롬프트와 함께 구조 탭을 제공합니다.

2) 한글 디자인 모드
- 한글 타이포그래피, 한글 모던 그래픽, 전통 한글 포스터, K-에디토리얼 화보 스타일을 포함합니다.
- 정확한 한글 문구 입력란을 제공합니다. 단, 실제 글자 정확도는 사용하는 이미지 생성 모델의 텍스트 렌더링 성능에 좌우됩니다.

3) 세트 일관성
- 같은 주제의 여러 장을 만들 때 팔레트와 정체성 규칙을 유지합니다.
- 팔레트를 입력하지 않으면 배치 단위 기본 HEX 팔레트를 자동 생성합니다.

4) 기존 DesignPD 기능 유지
- 빠른 모드
- 프리셋/작업 모드/이미지 스타일 선택
- 이미지/영상/3D 프롬프트 생성
- 즐겨찾기/템플릿 저장
- 리포트 저장
- 한국어 주제 자동 영어 변환

실행
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
run.bat

접속 주소
http://localhost:8504

실행파일 빌드
build_exe_launcher.bat

생성 파일
dist\HangeulDesign_Streamlit_Launcher.exe
