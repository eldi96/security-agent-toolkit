from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.get_json()
    print("===== 받은 데이터 =====", flush=True)
    # 1. event 에 "rule" 칸이 있으면 {"status": "ok", "rule": event 의 rule 값} 과 200 을 return 하세요
    if "rule" in event:
            return {"status": "ok", "rule": event["rule"]}, 200
    else: 
        return {"status" : "ok"}, 200



app.run(port=5002)
