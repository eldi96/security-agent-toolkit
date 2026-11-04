import pandas as pd

EVENTS_PATH = "normalized_events.json"
TYPE_ORDER = ["비정상 로그인", "비인가 접근", "기타 실패", "정상"]


def load_events(path):
    """이벤트 JSON 파일을 판다스 표로 읽는다."""
    events = pd.read_json(path)
    return events


def classify_event(action, result):
    """행동과 결과를 받아 먼저 맞는 규칙의 유형 이름을 반환한다."""
    # 1. 로그인 실패를 먼저 확인한다.
    if result == "실패" and action == "POST /login":
        return "비정상 로그인"
    # 2. 관리자 경로에 대한 실패를 확인한다.
    if result == "실패" and "/admin" in action:
        return "비인가 접근"
    # 3. 앞의 두 조건에 해당하지 않는 실패를 모은다.
    if result == "실패":
        return "기타 실패"
    return "정상"


def count_types(events):
    """이벤트 표를 받아 유형별 개수를 딕셔너리로 반환한다."""
    event_list = events.to_dict("records")  # 한 행을 딕셔너리 하나로 바꾼다.
    counts = {}
    for event in event_list:
        action = event["action"]
        result = event["result"]
        type_name = classify_event(action, result)
        counts[type_name] = counts.get(type_name, 0) + 1
    return counts
