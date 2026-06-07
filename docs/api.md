# API 문서

## 실행 기준

FastAPI 서버 실행 후 기본 주소는 `http://127.0.0.1:8000`이다.
대화형 문서는 `/docs`에서 확인한다.

기본 `APP_DATA_MODE=sample`은 팀이 작성한 샘플 데이터만 반환한다.
`APP_DATA_MODE=finlife`는 `FINLIFE_API_KEY`와 `FINLIFE_ALLOWED_BANKS`가 모두 있어야 동작한다.

## 엔드포인트

| 방식 | 경로 | 설명 |
| --- | --- | --- |
| `GET` | `/api/health` | 서버 상태와 데이터 모드 |
| `GET` | `/api/health/mysql` | MySQL 연결 상태 |
| `GET` | `/api/products` | 상품 목록과 필터 |
| `GET` | `/api/products/{product_id}` | 상품 상세 |
| `POST` | `/api/products/compare` | 선택 상품 비교 |
| `POST` | `/api/products/compare-summary` | 선택 상품 비교 요약 |
| `POST` | `/api/recommendations` | 규칙 기반 추천과 설명 |
| `GET` | `/api/stats/rates` | 유형별 최고금리 통계 |

## 상품 목록

`GET /api/products`

선택 파라미터:

| 이름 | 설명 |
| --- | --- |
| `product_type` | `deposit` 또는 `saving` |
| `bank_name` | 정확히 일치하는 은행명 |
| `term_months` | 가입 기간 개월 수 |

## 비교

`POST /api/products/compare`

요청:

```json
{
  "product_ids": [
    "sample:deposit:sample-bank-a:deposit-a",
    "sample:deposit:sample-bank-b:deposit-b"
  ]
}
```

상품은 두 개 또는 세 개를 선택한다.
`POST /api/products/compare-summary`도 같은 요청 형식을 사용한다.
OpenAI 설명 보조가 비활성화되거나 실패하면 서버 기본 비교 문구를 반환한다.

## 추천

`POST /api/recommendations`

요청:

```json
{
  "product_type": "saving",
  "term_months": 12,
  "amount": 100000,
  "prefer_simple_conditions": true,
  "max_results": 3
}
```

추천 순위는 서버의 규칙 기반 점수가 결정한다.
OpenAI API는 활성화된 경우 설명 문구만 보조한다.

## 오류

예상 가능한 애플리케이션 오류는 다음 형식으로 반환한다.

```json
{
  "detail": "오류 설명"
}
```

주요 상태 코드:

| 상태 코드 | 상황 |
| --- | --- |
| `404` | 상품을 찾을 수 없음 |
| `422` | 요청 형식 또는 값 검증 실패 |
| `502` | 금융감독원 API 호출 실패 |
| `503` | `finlife` 모드 필수 환경변수 누락 |
