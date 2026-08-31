# GitHub Upload Checklist

## 올리기 전 확인

- `README.md`가 프로젝트 설명, 설치, 실행 방법을 포함하는지 확인
- `.gitignore`가 `venv/`, `build/`, `dist/`, `*.exe`, 임시 이미지 파일을 제외하는지 확인
- `requirements.txt`가 필요한 패키지를 포함하는지 확인
- `run.bat`가 `http://localhost:8504`로 실행되는지 확인
- 민감한 정보, API 키, 개인 데이터가 없는지 확인
- 라이선스를 공개할지 결정

## GitHub에 포함할 핵심 파일

- `app.py`
- `requirements.txt`
- `run.bat`
- `launcher.py`
- `build_exe_launcher.bat`
- `README.md`
- `README.txt`
- `CHANGELOG.md`
- `.gitignore`
- `.github/workflows/smoke-test.yml`

## GitHub에 올리지 않을 파일/폴더

- `venv/`
- `build/`
- `dist/`
- `*.exe`
- `*.spec`
- 로컬 캡처 이미지
- 앱에서 저장한 리포트 파일

## 추천 명령

```bat
git init
git add app.py requirements.txt run.bat launcher.py build_exe_launcher.bat README.md README.txt CHANGELOG.md .gitignore GITHUB_UPLOAD_CHECKLIST.md
git commit -m "Initial Hangeul Design release"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO.git
git push -u origin main
```
