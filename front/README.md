# FinMatch frontend

금융감독원 금융상품 정보를 비교하고 조건별 추천을 확인하는 Next.js 프론트엔드입니다.

## 사용 데이터

- 금융상품 목록, 상세, 금리 통계, 비교 요약, 추천: FastAPI 호출
- 회원가입과 로그인 사용자: Neon PostgreSQL `app_users`
- 금융상품 원문과 정규화 결과: 브라우저, SQLite, DB에 영구 저장하지 않음
- 기존 SQLite 마이그레이션: `prisma/migrations-sqlite-legacy/`에 참고용으로만 보존

CSV 금융상품 시드는 제거되어 있습니다.

## 최초 설정

Neon 접속 문자열을 `front/.env.local`의 `DATABASE_URL`에 넣은 뒤
프론트엔드 의존성을 설치합니다. 예시는 `front/.env.example`을 참고합니다.

```powershell
cd front
& "C:\Program Files\nodejs\npm.cmd" ci
```

`front/.env.local`은 로컬 전용이며 Git에 포함하지 않습니다.

## 실행

FastAPI를 먼저 실행한 뒤 별도 터미널에서 프론트엔드를 시작합니다.

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
cd front
& "C:\Program Files\nodejs\npm.cmd" run dev
```

- 프론트엔드: `http://127.0.0.1:3000`
- FastAPI 문서: `http://127.0.0.1:8000/docs`

## 검증

```powershell
& "C:\Program Files\nodejs\npm.cmd" run lint
& "C:\Program Files\nodejs\npm.cmd" run build
```
