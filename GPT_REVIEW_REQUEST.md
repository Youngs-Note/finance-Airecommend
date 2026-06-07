# GPT 검토 요청서

> 상태: 검토 완료된 과거 요청서입니다. 현재 확정 사항은 [`docs/project-decisions.md`](./docs/project-decisions.md)를 따릅니다.

## 요청 목적

첨부한 프로젝트 문서와 PPT를 검토하고, 졸업 프로젝트의 MVP 범위와 구현 방향을 결정해 주세요.

아직 코드 구현 전 단계입니다.
문서에 있는 표현을 그대로 승인하기보다, 졸업작품으로 완성 가능한 범위인지 비판적으로 판단해 주세요.

## 프로젝트 개요

프로젝트명:

```text
AI 기반 금융상품(예금·적금) 비교 및 맞춤 추천 웹 서비스
```

목표:

* 대한민국 제1금융권의 예금·적금 상품 정보를 비교한다.
* 사용자가 금리, 가입 기간, 납입 금액, 우대조건 등을 기준으로 상품을 찾을 수 있도록 한다.
* 사용자 조건에 맞는 상품을 우선 제시한다.
* 외부 AI API를 활용해 자연어 조건 해석, 추천 이유 설명, 상품 비교 요약을 제공한다.
* 추천 결과는 확정적인 금융 조언이 아니라 비교와 판단을 돕는 참고 정보로 표현한다.
* 졸업작품 발표에서 데이터 수집, 비교, 추천, 설명, 시각화 흐름을 시연한다.

## 현재 준비 상태

완료:

* 로컬 Git 저장소 초기화
* 비공개 GitHub 원격 저장소 연결
* 프로젝트 작업 규칙 작성
* GitHub 협업 규칙 작성
* 팀원용 협업 지침서 작성
* PPT 기반 프로젝트 계획 초안 작성
* 금융상품 데이터 수집 기능 계획 작성
* AI API 연동 기능 계획 작성

아직 미완료:

* 초기 커밋과 원격 푸시
* `main`, 원격 `develop` 브랜치 생성
* 팀원 GitHub Collaborator 초대
* 백엔드와 프론트엔드 코드
* MySQL 실행 환경
* 금융감독원 API 인증키 신청
* AI API 제공자와 모델 선정
* 배포 환경

## 현재 제안된 기술 방향

### Backend

* Python
* FastAPI
* Pydantic
* requests
* BeautifulSoup
* pandas
* numpy
* 필요 시 scikit-learn

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap
* Chart.js

### Database

* MySQL

### 개발과 배포 후보

* GitHub
* Docker
* AWS EC2
* 필요 시 Prometheus, ELK Stack

## 금융상품 데이터 관련 핵심 이슈

금융감독원 `금융상품 한눈에` 오픈 API에서 은행 권역 코드 `020000`의 예금·적금 상품을 조회할 수 있습니다.

공식 API:

```text
GET https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json
GET https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json
```

문제:

* API 인증키가 필요합니다.
* 약관에는 실시간 연동은 가능하지만 API 정보의 복제, 저장, 전송 제한이 있습니다.
* 상품 정보를 DB에 영구 저장하고 분석 데이터셋으로 사용할 수 있는지 금융감독원에 문의해야 합니다.
* 은행별 직접 크롤링은 API에서 제공하지 않는 필드가 반드시 필요할 때만 검토하려 합니다.

검토가 필요한 선택지:

```text
A. 금융감독원 API를 요청 시 호출하고 메모리에서만 정제한다.
B. DB 저장이 필요하므로 금융감독원에 저장 허용 범위를 문의한다.
C. 저장과 재사용이 가능한 별도 공식 데이터 소스를 찾는다.
D. 허용 범위를 확인한 은행 사이트만 보조적으로 크롤링한다.
```

## AI API 관련 핵심 이슈

현재 제안:

* 규칙 기반 점수화가 추천 순위를 결정한다.
* 외부 AI API는 자연어 조건 해석, 추천 이유 설명, 비교 요약을 보조한다.
* 공식 상품명과 금리 수치를 AI가 새로 생성하도록 하지 않는다.
* AI API가 실패하면 규칙 기반 추천과 기본 설명 템플릿으로 복구한다.
* AI API Key는 백엔드 환경변수로만 관리한다.

검토가 필요한 선택지:

```text
A. MVP에서는 AI API를 추천 설명 생성에만 사용한다.
B. MVP에서 자연어 조건 해석까지 포함한다.
C. AI API가 추천 순위 보정에도 관여하도록 한다.
D. MVP에서는 AI API를 제외하고 후속 단계에서 추가한다.
```

## 제1금융권 범위 관련 질문

기본 포함 후보:

* 시중은행
* 지방은행
* 인터넷전문은행

추가 검토:

* 특수은행 포함 여부
* 외국계 은행 국내 지점 포함 여부
* 저축은행 제외 여부

저축은행은 금융감독원 API에서 별도 권역 코드 `030300`이므로 기본 범위에서는 제외하려 합니다.

## 팀 협업 관련 질문

현재 GitHub 저장소는 비공개 상태이며 소유자만 등록되어 있습니다.

검토가 필요한 사항:

* `main`, `develop`, 개인 작업 브랜치 전략이 적절한가?
* 졸업작품 팀 규모에서 Issue와 Pull Request를 어느 수준까지 운영해야 하는가?
* `main`과 `develop`에 브랜치 보호 규칙을 어떻게 설정하면 좋은가?
* 최소 1명의 리뷰 후 `Squash and merge`를 기본으로 하는 방식이 적절한가?

## 일정 관련 질문

PPT에는 8주 일정이 제시되어 있습니다.

```text
1주차: 기획 및 요구사항 분석
2주차: 관련 연구 조사, 시스템 구조 설계
3주차: 데이터 수집, DB 설계
4주차: 백엔드 API 구현
5주차: 상품 분석, 추천 알고리즘
6주차: 프론트엔드 구현
7주차: 기능 통합, 테스트
8주차: 결과 정리, 발표 준비
```

실제 발표일은 아직 이 요청서에 기재하지 않았습니다.
현실적인 일정인지 검토하고, 병렬 작업이 필요한 부분을 제안해 주세요.

## 추가로 결정해야 할 사항

다음 항목도 판단해 주세요.

* 사용자 연령과 직업 정보를 저장할지, 요청 시점에만 사용할지
* MySQL을 Docker Compose로 실행할지, 팀원 로컬에 직접 설치할지
* PPT 파일을 GitHub 저장소에 포함할지
* `.gitignore`, `.env.example`, `.editorconfig`, `.vscode/extensions.json`을 초기 커밋에 포함할지
* Python 의존성을 `requirements.txt`와 `pyproject.toml` 중 무엇으로 관리할지
* MVP에서 로그인, 캐시 서버, 모니터링, 배포 자동화를 제외해도 되는지

## 검토 시 참고할 파일

우선순위 순서:

1. [`README.md`](./README.md)
2. [`docs/plans/2026-06-02-graduation-project-plan.md`](./docs/plans/2026-06-02-graduation-project-plan.md)
3. [`docs/plans/2026-06-02-financial-product-data-collection.md`](./docs/plans/2026-06-02-financial-product-data-collection.md)
4. [`docs/plans/2026-06-02-ai-api-integration.md`](./docs/plans/2026-06-02-ai-api-integration.md)
5. [`docs/collaboration-guide.md`](./docs/collaboration-guide.md)
6. [`AGENTS.md`](./AGENTS.md)
7. [`졸업프로젝트ppt.pptx`](./졸업프로젝트ppt.pptx)

## 원하는 답변 형식

아래 형식으로 답변해 주세요.

```text
1. 총평

2. MVP 확정안
- 반드시 포함:
- 제외 또는 후순위:

3. 금융상품 데이터 수집 결정
- 권장 선택지:
- 이유:
- 약관 확인 또는 문의가 필요한 부분:

4. AI API 사용 결정
- MVP 적용 범위:
- 추천 제공자 또는 제공자 선택 기준:
- 보안 및 비용 주의사항:

5. 제1금융권 포함 범위

6. 시스템 구조 확정안

7. 팀 협업 방식 확정안

8. 일정 수정안

9. 초기 커밋에 포함할 파일

10. 구현 전에 사용자가 추가로 제공해야 할 정보

11. Codex가 바로 진행해도 되는 작업 목록

12. 위험 요소와 우선 확인 사항
```
