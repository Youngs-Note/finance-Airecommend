# 금융감독원 API 인증키 신청

## 신청 링크

금융감독원 `금융상품 한눈에` 인증키 신청 화면:

<https://finlife.fss.or.kr/finlife/api/finlifeApiKey/list.do?menuNo=700034>

## 개인 인증키 신청 순서

1. 오픈 API 이용약관과 개인정보 수집 및 이용에 동의한다.
2. 이용형태에서 `개인`을 선택한다.
3. `본인 인증`을 진행한다.
4. 이메일 주소를 입력하고 `이메일 인증`을 완료한다.
5. 사용용도는 웹 서비스 개발 기준으로 `WEB`을 선택한다.
6. 사용 URL이 아직 없다면 로컬 개발 주소 또는 프로젝트 용도를 식별할 수 있는 주소를 입력한다.
7. `인증키 신청` 버튼을 누른다.
8. 발급된 인증키는 채팅이나 명령어에 직접 붙여넣지 않고 로컬 보안 입력 스크립트로 저장한다.

인증키는 채팅, GitHub Issue, Pull Request, 문서에 붙여넣지 않는다.

## 개인 신청 조건

금융감독원 신청 화면 기준:

* 개인 신청은 신청 즉시 인증키가 발급된다.
* 개인 인증키는 일일 조회 수 `10,000`건으로 제한된다.
* 기본적으로 1회 조회 시 `100`건씩 페이지 처리된다.
* 인증키는 신청자만 사용한다.
* 발급된 인증키는 `12개월` 동안 사용하지 않으면 삭제될 수 있다.

## 프로젝트 적용

다음 명령을 실행한 뒤 표시되는 보안 입력란에 새 키를 붙여넣는다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\set-local-api-keys.ps1 -Finlife
```

스크립트는 Git에서 제외된 로컬 `.env`에 `FINLIFE_API_KEY`를 저장하고
`APP_DATA_MODE=finlife`를 설정한다.

은행 권역은 `020000`으로 고정한다.
노출 은행은 프로젝트의 명시적 허용 목록으로 한 번 더 제한한다.

## 저장 및 표시 주의 사항

금융감독원 이용약관에 따라 API 응답 원문과 정규화 결과를 DB 또는 Git에 저장하지 않는다.
화면에는 다음 출처 문구를 표시한다.

```text
금융상품통합비교공시시스템(금융감독원) 금융회사 상품정보를 사용한 결과입니다.
```

## 공식 출처

* 인증키 신청: <https://finlife.fss.or.kr/finlife/api/finlifeApiKey/list.do?menuNo=700034>
* 오픈 API 소개: <https://finlife.fss.or.kr/finlife/main/contents.do?menuNo=700029>
