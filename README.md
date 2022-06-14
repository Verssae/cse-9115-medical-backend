# 0. 개요

- Flask 기반 예진표 작성 프로그램
- [Front-End](https://github.com/Verssae/cse9115-medical-app) 앱에서 예진한 결과가 본 서버로 전송되어 예진표를 작성한다

# 1. 의존성 패키지 설치

```bash
$ pip install flask mdutils requests pyinstaller markdown
```


# 2. 빌드

```bash
$ pyinstaller --onefile server.py
```


# 3. 서버 실행

- 실행파일 경로: ./dist/server.*

- 생성되는 md파일 경로는 실행파일 기준 현재폴더에서 "(환자이름)\_(생년)\_(월).md" 


# 4. Examples

- `220609`, `220610` 안 `*.html`
