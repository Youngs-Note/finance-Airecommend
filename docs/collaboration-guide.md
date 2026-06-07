# 팀원 GitHub 협업 지침서

이 문서는 `finance-Airecommend` 프로젝트에 참여하는 팀원을 위한 GitHub 협업 안내서입니다.
팀원 모두가 같은 저장소를 사용하므로, 다른 사람의 작업을 보존하고 변경 이력을 남기는 것을 우선합니다.

## 1. 저장소 정보

* GitHub 저장소: [Youngs-Note/finance-Airecommend](https://github.com/Youngs-Note/finance-Airecommend)
* 안정 버전 브랜치: `main`
* 통합 개발 브랜치: `develop`
* 개인 작업 브랜치: `feature/...`, `fix/...`, `docs/...`, `chore/...`

`main`과 `develop`에는 직접 커밋하거나 직접 푸시하지 않습니다.
개인 브랜치에서 작업하고 Pull Request를 통해 변경 사항을 반영합니다.

## 2. 참여 전 준비

### Git 설치 확인

터미널에서 다음 명령을 실행합니다.

```bash
git --version
```

Git이 설치되어 있지 않으면 [Git 공식 사이트](https://git-scm.com/downloads)에서 설치합니다.

### GitHub 저장소 접근 권한 확인

저장소가 비공개 상태라면 저장소 관리자가 팀원을 Collaborator로 초대해야 합니다.

1. 저장소 관리자가 GitHub 사용자명을 확인합니다.
2. GitHub 저장소의 `Settings > Collaborators`에서 팀원을 초대합니다.
3. 팀원이 GitHub 알림 또는 이메일에서 초대를 수락합니다.
4. 팀원이 저장소 페이지에 접속되는지 확인합니다.

### Git 사용자 정보 설정

처음 한 번만 다음 명령을 실행합니다.

```bash
git config --global user.name "이름 또는 GitHub 사용자명"
git config --global user.email "GitHub에서 사용하는 이메일"
```

설정값은 다음 명령으로 확인합니다.

```bash
git config --global user.name
git config --global user.email
```

## 3. 프로젝트 처음 받기

작업할 폴더에서 다음 명령을 실행합니다.

```bash
git clone https://github.com/Youngs-Note/finance-Airecommend.git
cd finance-Airecommend
git branch --all
```

`develop` 브랜치가 원격 저장소에 있으면 다음 명령으로 이동합니다.

```bash
git switch develop
git pull origin develop
```

## 4. 작업 시작 절차

작업을 시작하기 전에 GitHub Issue 또는 팀 작업 목록에서 담당 작업을 확인합니다.
다른 팀원과 수정 범위가 겹칠 가능성이 있으면 먼저 조율합니다.

항상 최신 `develop`을 기준으로 개인 브랜치를 만듭니다.

```bash
git switch develop
git pull origin develop
git switch -c feature/product-compare
```

작업 종류에 맞춰 브랜치 이름을 정합니다.

```text
feature/product-compare
fix/recommendation-score
docs/api-guide
chore/docker-setup
```

## 5. 작업 중 커밋하기

변경 상태를 확인합니다.

```bash
git status
git diff
```

작업과 관련된 파일만 명시적으로 추가합니다.

```bash
git add backend/app/routers/products.py
git add tests/test_products.py
```

모든 파일을 한꺼번에 추가하는 `git add .`은 가급적 사용하지 않습니다.

커밋 메시지는 변경 목적이 드러나도록 작성합니다.

```bash
git commit -m "feat: add product comparison endpoint"
```

권장 커밋 유형:

| 유형 | 용도 |
| --- | --- |
| `feat` | 기능 추가 |
| `fix` | 오류 수정 |
| `docs` | 문서 변경 |
| `refactor` | 동작 변경 없는 코드 구조 개선 |
| `test` | 테스트 추가 또는 수정 |
| `chore` | 설정, 의존성, 기타 작업 |

## 6. 원격 저장소에 개인 브랜치 올리기

첫 푸시는 다음과 같이 실행합니다.

```bash
git push -u origin feature/product-compare
```

이후 같은 브랜치에서는 다음 명령으로 푸시할 수 있습니다.

```bash
git push
```

비밀번호, API Key, `.env`, 개인정보가 포함되지 않았는지 반드시 확인합니다.

## 7. Pull Request 만들기

GitHub 저장소 페이지에서 `Compare & pull request`를 선택합니다.

* 대상 브랜치: `develop`
* 작업 브랜치: 본인의 개인 브랜치
* 제목: 커밋 목적을 이해할 수 있는 짧은 문장

Pull Request 본문에는 다음 내용을 작성합니다.

```text
## 작업 목적
## 주요 변경 사항
## 영향받는 화면 / API / DB
## 실행 및 검증 방법
## 테스트 결과
## 리뷰 시 확인할 사항
## 남은 문제 또는 후속 작업
```

API, DB 스키마, 공통 데이터 모델을 변경했다면 관련 팀원이 확인할 수 있도록 명확히 표시합니다.

## 8. 리뷰와 병합

Pull Request는 가능하면 최소 1명의 다른 팀원이 확인한 뒤 병합합니다.

병합하면 안 되는 상태:

* 테스트가 실패한 상태
* 충돌이 해결되지 않은 상태
* 비밀번호, 인증 토큰, 개인정보가 포함된 상태
* API 또는 DB 변경을 관련 팀원과 공유하지 않은 상태

별도 합의가 없으면 `Squash and merge`를 우선 사용합니다.

## 9. 병합 후 동기화

Pull Request가 병합되면 로컬 `develop`을 최신 상태로 맞춥니다.

```bash
git switch develop
git pull origin develop
```

작업이 끝난 개인 브랜치는 더 이상 필요하지 않을 때 정리합니다.

```bash
git branch -d feature/product-compare
```

원격 브랜치 삭제는 팀원이 더 이상 사용하지 않는지 확인한 뒤 진행합니다.

## 10. 충돌이 발생했을 때

충돌이 발생하면 다른 팀원의 변경을 임의로 덮어쓰지 않습니다.

1. 충돌 파일과 충돌 범위를 확인합니다.
2. 관련 파일을 수정한 팀원에게 어떤 내용을 유지할지 확인합니다.
3. 합의한 내용을 기준으로 충돌을 해결합니다.
4. 해결한 파일과 판단 기준을 Pull Request에 기록합니다.

`force push`, `rebase`, `reset --hard`가 필요해 보이면 먼저 팀과 상의합니다.

## 11. 절대 커밋하면 안 되는 파일과 정보

* `.env`
* DB 비밀번호
* API Key
* AWS Access Key와 Secret Key
* 인증 토큰
* 개인 계정 정보
* 실제 사용자 개인정보

보안 정보가 실수로 커밋되면 단순히 파일을 삭제하는 것으로 끝나지 않습니다.
즉시 팀에 알리고 해당 키 또는 비밀번호를 폐기한 뒤 새로 발급해야 합니다.

## 12. 팀에서 함께 기록할 내용

다음 내용은 개인 메시지에만 남기지 않고 GitHub Issue, Pull Request, 또는 프로젝트 문서에 기록합니다.

* 기능 담당자와 작업 범위
* 주요 설계 결정과 변경 이유
* API 요청 및 응답 형식 변경
* DB 스키마 변경
* 데이터 수집 방식과 출처 변경
* 해결하지 못한 문제
* 임시 처리 로직과 미구현 기능

## 13. 자주 사용하는 명령어

```bash
# 현재 브랜치와 변경 파일 확인
git status --short --branch

# 원격 저장소 확인
git remote -v

# 원격 변경 사항 확인
git fetch origin

# develop 최신화
git switch develop
git pull origin develop

# 새 작업 브랜치 생성
git switch -c feature/example

# 커밋 이력 확인
git log --oneline --decorate --graph --all
```

## 14. 문제가 생겼을 때 공유할 정보

질문할 때는 다음 정보를 함께 전달하면 문제를 빠르게 확인할 수 있습니다.

```text
현재 브랜치:
실행한 명령:
오류 메시지:
변경한 파일:
원하는 결과:
```
