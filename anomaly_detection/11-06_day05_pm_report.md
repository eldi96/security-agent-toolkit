# 4과목 Day 5 도커 컴포즈로 서버 두 대 켜기 · 웹 서버 로그 만들기 · 오후 (이름 · 2026-11-06(금))

> **쓰는 법**
> - 문제를 풀 때마다 그 문제 제목 아래 질문에 답합니다.
> - 질문마다 `쓸 내용:` 에 무엇을 쓰면 되는지 적혀 있습니다. 그대로 `답:` 뒤에 씁니다.
> - 출력이나 코드를 붙여 넣는 질문은 `답:` 아래 빈 코드 상자에 붙여 넣고, 설명은 `답:` 뒤에 씁니다.
> - 「왜」를 묻는 질문은 한 단어로 끝내지 말고, 내 화면에서 본 값이나 배운 내용을 근거로 이유까지 씁니다.
> - 🔍 는 이 교시에서 꼭 알아야 할 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 이라고 씁니다. 🔍 가 없는 질문도 못 적으면 같은 말을 씁니다.

---

## 5교시 · 도커 복습 · 컴포즈로 서버 두 대 한 번에 켜기

### 문제 5-1 · 서버 한 대를 복습하고 컴포즈로 두 대 켜기

- (가) 5교시 순서의 서버 켜기 · 확인 명령(`docker images` 부터 `curl` 까지)과 그 결과를 친 순서대로 붙여 넣고, 서비스 이름 두 개와 각 서비스의 포트를 적어 주세요.
  - 쓸 내용: ① 명령과 결과를 친 순서대로(코드 상자에 붙여 넣기): `docker images` · `docker run` · `docker ps` · `docker stop` · `docker compose up -d` · `docker compose ps` · `curl` 두 개 (`docker pull` 은 받았을 때만, `pwd` · `touch` · `ls` 는 붙이지 않아도 됩니다) ② 서비스 이름 두 개 ③ 각 서비스의 포트
  - 답:

    - **서비스와 포트:** `web1`은 PC의 8080 → 컨테이너의 80, `web2`는 PC의 8081 → 컨테이너의 80으로 연결된다. 두 서비스 모두 `nginx:1.28`을 사용한다.
    - **실행 확인:** 두 컨테이너가 Up 상태이고, 8080·8081 모두 HTTP 200을 반환했다. 아래 Compose와 curl 부분은 실제 실행 기록이다. 앞선 `docker images`·`docker run`·`docker ps`·`docker stop`의 출력은 아직 추가가 필요하다.

```bash
docker images nginx:1.28
# 예상: nginx 1.28 이미지 표시. 실제 출력 붙이기 필요.

docker run -d --rm -p 8080:80 --name web-run nginx:1.28
# 예상: 생성된 컨테이너 ID 출력. 실제 출력 붙이기 필요.

docker ps
# 예상: web-run 실행 중, PC 8080 → 컨테이너 80 연결 표시.

docker stop web-run
# 예상: web-run 출력. --rm 옵션으로 정지 후 컨테이너 자동 삭제.

docker compose up -d
[+] up 3/3
 ✔ Network anomaly_detection_default  Created  0.0s
 ✔ Container anomaly_detection-web2-1 Started  0.6s
 ✔ Container anomaly_detection-web1-1 Started  0.4s

docker compose ps
NAME                       IMAGE        COMMAND                   SERVICE   CREATED          STATUS          PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      55 seconds ago   Up 54 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      55 seconds ago   Up 54 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp

curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080
200

curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081
200
```

- (나) 🔍 서버 두 대를 `docker run` 으로 켜는 것과 `compose.yaml` 과 `docker compose up -d` 로 켜는 것을 비교해, 컴포즈가 더 나은 점을 두 가지 적어 주세요.
  - 쓸 내용: ① 컴포즈가 더 나은 점 두 가지
  - 답:

    - **한 번에 관리:** 서비스 두 개를 파일에 정의하고 `docker compose up -d` 한 번으로 시작할 수 있어, 긴 run 명령을 각각 입력하는 수고와 실수를 줄인다.
    - **설정 공유·재현:** 이미지 버전, 포트, 재시작 정책을 파일에 남겨 팀원이 같은 설정을 확인하고 다시 사용할 수 있다. Git으로 변경 이력도 관리할 수 있다.

- (다) 🔍 보안 사고가 난 뒤 감사팀이 「사고 당시와 같은 구성으로 서버를 다시 켜 보라」고 요청했습니다. 팀원 한 명은 3주 전에 긴 `docker run` 명령을 직접 쳐서 서버를 켰는데 그 명령을 기억하지 못합니다. 다른 팀은 `compose.yaml` 을 깃허브에 올려 두었습니다. 두 팀이 같은 구성을 다시 켤 수 있는지 비교하고, 파일에 `nginx:1.28` 처럼 버전을 적어 두는 것이 이런 재현에 왜 중요한지 적어 주세요.
  - 쓸 내용: ① 두 팀의 차이 ② 버전을 적어 두는 것이 재현에 중요한 이유
  - 답:

    - **두 팀의 차이:** 명령을 기억하지 못하는 팀은 당시 이미지·포트·옵션을 다시 조사해야 한다. 파일을 Git에 보관한 팀은 사고 당시 커밋의 `compose.yaml`을 찾아 설정을 확인하고 다시 실행할 수 있다.
    - **버전 기록:** `latest`처럼 바뀔 수 있는 태그 대신 `nginx:1.28`을 적으면 다른 버전으로 실행될 가능성을 줄인다. 다만 버전 태그도 이미지가 갱신될 수 있어 완전히 같은 이미지를 보장하려면 이미지 digest까지 기록해야 한다.

- (라) 🔍 팀원 세 명이 같은 `compose.yaml` 로 서버를 켰는데 한 명의 PC 에서만 `8081` 번 포트를 다른 프로그램이 쓰고 있어서 `web2` 가 켜지지 않았습니다. 이 사람이 파일의 어느 줄을 어떻게 바꾸면 되는지 적고, 바꿔도 서버 안에서는 여전히 `80` 번 포트로 동작하는 이유를 적어 주세요. 이 사람이 `curl` 로 확인할 때 달라지는 점도 적어 주세요.
  - 쓸 내용: ① 바꿀 줄과 바꾼 모양 ② 서버 안은 그대로 80 인 이유 ③ curl 주소의 달라지는 점
  - 답:

    - **변경:** 사용하지 않는 PC 포트가 8082라면 web2의 ports 아래 `"8081:80"`을 `"8082:80"`으로 바꾸고 `docker compose up -d`로 적용한다.
    - **컨테이너 내부:** 왼쪽은 PC가 받는 포트이고 오른쪽은 컨테이너가 받는 포트이다. 왼쪽만 바꿨으므로 nginx는 계속 컨테이너 내부 80에서 동작한다.
    - **확인 주소:** web2는 `http://localhost:8082`로 확인한다. web1은 기존 `http://localhost:8080`을 사용한다.

## 6교시 · 서버마다 접속 범위 정하기 · 설정 바꿔 적용하기

### 문제 6-1 · 서버마다 접속 범위를 정해 컴포즈 파일로 적용하기

- (가) 1번과 5번의 `docker compose ps` 출력을 붙여 넣고, 접속 범위가 바뀐 기존 서비스와 새로 추가된 서비스를 따로 적어 주세요.
  - 쓸 내용: ① 1번 출력(코드 상자에 붙여 넣기) ② 5번 출력(코드 상자에 붙여 넣기) ③ 접속 범위가 바뀐 기존 서비스 ④ 새로 추가된 서비스
  - 답:

    - **변경된 기존 서비스:** web2. `8081:80`에서 `127.0.0.1:8081:80`으로 바꿔 내 PC에서만 접속하도록 설정했다. web1은 기존 `8080:80`을 유지한다.
    - **추가된 서비스:** web3. `127.0.0.1:8082:80`으로 내 PC에서만 접속하며, `./logs:/var/log/nginx`로 로그를 PC에 보관한다.
    - **출력 보완:** 변경 전 ps는 5-1의 실제 기록이다. 변경 후 ps 출력은 전달된 실행 기록에 없어 추가가 필요하다. 아래 확인 결과로 내부 접속과 로그 생성·보존은 확인했다.

변경 전 `docker compose ps` 실제 출력:

```
NAME                       IMAGE        COMMAND                   SERVICE   CREATED          STATUS          PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      55 seconds ago   Up 54 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      55 seconds ago   Up 54 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
```

변경 후 `docker compose -f compose.secure.yaml ps` 실제 출력:

```
미첨부 — 종료 전 실행한 ps 출력 추가 필요.
```

추가로 확인한 실제 실행 기록:

```text
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081
200
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8082
200
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8082/.env
404
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8082/phpmyadmin
404
$ cat logs/access.log
172.18.0.1 - - [06/Nov/2026:06:19:19 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.22.0" "-"
172.18.0.1 - - [06/Nov/2026:06:19:22 +0000] "GET /.env HTTP/1.1" 404 153 "-" "curl/8.22.0" "-"
172.18.0.1 - - [06/Nov/2026:06:19:26 +0000] "GET /phpmyadmin HTTP/1.1" 404 153 "-" "curl/8.22.0" "-"
$ grep " 404 " logs/access.log | wc -l
2
$ grep " 404 " logs/access.log > logs/web_404.log
$ docker compose -f compose.secure.yaml down
[+] down 4/4
 ✔ Container anomaly_detection-web3-1 Removed  0.7s
 ✔ Container anomaly_detection-web1-1 Removed  0.7s
 ✔ Container anomaly_detection-web2-1 Removed  0.5s
 ✔ Network anomaly_detection_default  Removed  0.2s
$ ls logs
access.log  error.log  web_404.log
```

- (나) 🔍 `"8081:80"` 과 `"127.0.0.1:8081:80"` 은 누가 접속할 수 있는지가 어떻게 다른가요? 관리 화면이나 데이터베이스 서버를 이렇게 설정하는 이유도 적어 주세요.
  - 쓸 내용: ① 두 포트 줄에서 누가 접속할 수 있는지의 차이 ② 관리 화면 · 데이터베이스를 이렇게 설정하는 이유
  - 답:

    - **접속 범위:** `8081:80`은 PC의 모든 인터페이스에 포트를 공개하므로, 네트워크 경로와 방화벽이 허용하면 다른 PC에서도 접속할 수 있다. `127.0.0.1:8081:80`은 내 PC의 루프백 주소에만 공개해 다른 PC의 직접 접속을 제한한다.
    - **설정 이유:** 관리 화면이나 데이터베이스는 불필요한 외부 접근을 줄여야 한다. 로컬로 접속 범위를 제한하면 원격에서 로그인·취약점 공격을 시도할 수 있는 노출을 줄일 수 있다.

- (다) 🔍 `up -d` 의 출력에서 `web1` 은 `Running`, `web2` 는 `Recreated`, `web3` 은 `Created` 였습니다. 서버마다 출력이 다른 이유와, 운영 중인 서비스의 설정을 바꿀 때 이것이 왜 도움이 되는지 적어 주세요.
  - 쓸 내용: ① 서버마다 출력이 다른 이유 ② 서버를 끊지 않고 바꿀 수 있는 것의 쓸모
  - 답:

    - **Running:** web1은 설정 변경이 없어 기존 컨테이너를 계속 사용한다.
    - **Recreated:** web2는 공개 주소 설정이 바뀌어 기존 컨테이너를 새 설정으로 재생성한다.
    - **Created:** web3는 새 서비스여서 컨테이너를 처음 만든다. 이 구분은 문제에서 제시한 출력에 대한 설명이다.
    - **운영상 이점:** 전체를 내렸다가 올리지 않고 변경이 필요한 서비스만 반영해 web1 같은 다른 서비스의 중단을 줄인다. 다만 재생성되는 web2 자체에는 일시적인 중단이 생길 수 있으며 무중단을 보장하는 것은 아니다.

### 마무리 · 오늘 만든 것을 깃허브에 올리기

- (가) `git status` 를 쳤을 때 `.env` 나 `.venv` 가 보였는지, 보였다면 어떻게 했는지 적어 주세요.
  - 쓸 내용: ① `.env` · `.venv` 가 보였는지 ② 보였다면 한 조치
  - 답:
