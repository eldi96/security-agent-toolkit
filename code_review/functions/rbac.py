

# users.json과 roles.json에서 사용자·자원·행위를 받아 역할별 권한표로 접근 가능 여부를 검사한다.
# 사용자 등록 → 재직 여부 → 역할 등록 → 요청 권한 보유 순서로 확인한다.
# 하나라도 통과하지 못하면 (False, 거부 이유), 모두 통과하면 (True, "허용")을 반환한다.
# “원래 역할로 할 수 있어?”


import json                                                      # JSON 파일을 읽는 모듈을 불러온다

with open("config/roles.json", encoding="utf-8") as f:           # 역할 파일을 연다
    ROLES = json.load(f)                                         # 역할 → 권한 목록 딕셔너리로 읽는다
with open("config/users.json", encoding="utf-8") as f:           # 사용자 파일을 연다
    USERS = json.load(f)                                         # 사용자 → 정보 딕셔너리로 읽는다


def check_permission(user, resource, action):                    # 사용자 · 자원 · 행위를 받는 함수
    """(허용 여부, 이유)를 리턴한다. 허용 목록에 없으면 모두 거부한다."""   # 함수 첫 줄의 """ … """ 는 함수 설명 글이고 실행에는 영향이 없다
    if user not in USERS:                                        # 사용자 파일에 없는 계정이면
        return False, "등록되지 않은 사용자"                       # 바로 거부하고 함수를 끝낸다
    # [2]-1. USERS[user]["employed"] 가 참이 아니면 "퇴사한 계정" 을 이유로 거부한다   # ←
    if not USERS[user]["employed"]:                              # 재직 중이 아니면
            return False, "퇴사한 계정"                                # 거부하고 함수를 끝낸다
    # [3]-1. 이 사용자의 역할 USERS[user]["role"] 을 role 에 담는다   # ←
    role = USERS[user]["role"]                                   # 이 사용자의 역할을 꺼낸다
    # [3]-2. role 이 ROLES 에 없으면 "역할이 없음" 을 이유로 거부한다   # ←
    if role not in ROLES:                                        # 역할 파일에 없는 역할이면
            return False, "역할이 없음"                                # 거부하고 함수를 끝낸다
    # [4]-1. resource 와 action 을 "자원:행위" 모양 글자로 합쳐 permission 에 담는다   # ←
    permission = f"{resource}:{action}"                          # "자원:행위" 모양 글자로 합친다
    # [4]-2. permission 이 ROLES[role] 목록에 없으면 "권한 없음" 을 이유로 거부한다   # ←
    if permission not in ROLES[role]:                            # 그 역할의 권한 목록에 없으면
            return False, "권한 없음"                                  # 거부하고 함수를 끝낸다

    return True, "허용"                                          # 모든 검사를 지나면 허용한다

'''
"seoyeon": {"role": "sales", "employed": true},
"junho": {"role": "finance", "employed": true},
"gaeun": {"role": "account_admin", "employed": true},
"dami": {"role": "sales", "employed": false},
"batch-night": {"role": "batch", "employed": true},
"tester": {"role": "intern", "employed": true}

"서연": {"역할": "영업팀", "재직여부": true},
"준호": {"역할": "재무팀", "재직여부": true},
"가은": {"역할": "계정관리자", "재직여부": true},
"다미": {"역할": "영업팀", "재직여부": false},
"야간배치": {"역할": "배치작업", "재직여부": true},
"테스터": {"역할": "인턴", "재직여부": true}
-------------------------------------------
"sales": ["SALES:QUERY", "SALES:CHANGE"],
"account_admin": ["ACCOUNT:QUERY", "ACCOUNT:CHANGE"],
"finance":["SALES:QUERY", "SETTLE:QUERY"],
"batch":["SETTLE:QUERY"],
"auditor":["SALES:QUERY", "SETTLE:QUERY", "ACCOUNT:QUERY"]

"영업팀": ["영업정보:조회", "영업정보:변경"],
"계정관리자": ["계정정보:조회", "계정정보:변경"],
"재무팀": ["영업정보:조회", "정산내역:조회"],
"배치작업": ["정산내역:조회"],
"감사자": ["영업정보:조회", "정산내역:조회", "계정정보:조회"]
'''