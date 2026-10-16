# day05 경보 판단

## 이상한 줄
- 줄 번호(여러 개면 모두):2번,3번
- 이유:인터넷에 있는 외부 PC(192.0.2.7)에서 내부망(INSIDE)의 DB 서버로 3306 포트 접속을 시도했는데, 방화벽이 이를 차단하지 않고 허용(permit)했기 때문이다. 외부에서는 DMZ의 WEB 서버에만 접근하도록 허용해야 한다.

## 고친 구성도
```
INTERNET ──── FW ──┬── DMZ    ( WEB : 443 open )
                   └── INSIDE ( DB  : 3306 deny )
DMZ ( WEB ) ── 3306 permit ──> INSIDE ( DB )                   

```
```


INTERNET ──── FW ──┬── DMZ    : WEB (443 open)
                   └── INSIDE : DB  (3306 from WEB only)


```


---


                         +------------------+
                         |     INTERNET     |
                         |   (External PC)  |
                         +------------------+
                                  |
                                  v
                         +------------------+
                         |    FIREWALL      |
                         |       (FW)       |
                         +------------------+
                            |           |
             443 permit     |           | 3306 deny
                            v           X
                    +---------------+   |
                    |      DMZ      |   |
                    | WEB (443 open)|   |
                    +---------------+   |
                            |           |
                3306 permit |           |
                            v           v
                    +-------------------+
                    |      INSIDE       |
                    |     DB (3306)     |
                    +-------------------+