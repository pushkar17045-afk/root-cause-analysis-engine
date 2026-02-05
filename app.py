import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "service": "Root Cause Analysis Engine",
        "status": "running",
        "endpoints": ["/analyze", "/docs", "/health"]
    }

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/docs")
def docs():
    return {
        "POST /analyze": {
            "description": "Analyze logs/events to find probable root causes",
            "payload": {
                "events": [
                    {
                        "timestamp": 1710000123,
                        "service": "service_b",
                        "level": "ERROR",
                        "message": "Timeout while calling service_c"
                    }
                ]
            }
        }
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    events = data.get("events", [])

    scores = {}
    for e in events:
        key = f'{e["service"]}: {e["message"]}'
        weight = 3 if e["level"] == "ERROR" else 1
        scores[key] = scores.get(key, 0) + weight

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return jsonify({
        "root_causes": [
            {"event": k, "confidence": v} for k, v in ranked
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
