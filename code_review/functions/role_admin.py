from functions.rbac import ROLES                                           # 어제 rbac.py 가 읽어 둔 역할 딕셔너리를 불러온다

# 두 함수는 실행 중인 사용자 명단을 변경하며, users.json 파일에는 저장하지 않는다.

# 실행 파일이 전달한 사용자 명단(USERS)·이름·새 역할을 받는다.
# ROLES에 있는 역할인지 확인하고, 없으면 False와 "없는 역할"을 반환한다.
# 새 사용자면 추가하고, 기존 사용자면 역할을 교체하며 재직 상태를 True로 설정한다.
# 변경을 완료하면 True와 "부여"를 반환한다.
# “입사·이동·퇴사한 사람의 정보를 어떻게 바꿀까?”

def assign_role(users, name, role):                              # 사용자 딕셔너리 · 이름 · 역할을 받는 함수
    """사용자에게 역할을 부여한다(입사 · 부서 이동). (성공 여부, 이유)를 리턴한다."""
    # ← 아래를 직접 씁니다 (주석은 두고 각 주석 바로 아래 줄에 씁니다)
    # 1. role 이 ROLES 에 없으면 False, "없는 역할" 을 리턴한다
    if role not in ROLES:
        return False, "없는 역할"
    # 2. users[name] 을 {"role": role, "employed": True} 로 바꾼다(새 사용자도, 이동하는 사용자도 같은 줄이다)
    users[name] = {"role": role, "employed": True}
    # 3. True, "부여" 를 리턴한다
    return True, "부여"



# 실행 파일이 전달한 사용자 명단(USERS)과 퇴사 처리할 이름을 받는다.
# 명단에 없는 이름이면 False와 "없는 사용자"를 반환한다.
# 해당 사용자의 역할은 남기고 재직 상태만 False로 바꿔 접근을 막는다.
# 변경을 완료하면 True와 "회수"를 반환한다.

def revoke_access(users, name):                                  # 사용자 딕셔너리 · 이름을 받는 함수
    """퇴사한 사용자의 접근을 회수한다. 역할은 남기고 `employed` 값만 바꾼다. (성공 여부, 이유)를 리턴한다."""
    # ← 아래를 직접 씁니다 (주석은 두고 각 주석 바로 아래 줄에 씁니다)
    # 1. name 이 users 에 없으면 False, "없는 사용자" 를 리턴한다
    if name not in users:
        return False, "없는 사용자"
    # 2. users[name]["employed"] 를 False 로 바꾼다
    users[name]["employed"] = False
    # 3. True, "회수" 를 리턴한다
    return True, "회수"
