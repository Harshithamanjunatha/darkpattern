# routes/ingest_routes.py
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from database.db import clickstream_collection, sessions_collection, alerts_collection
from services.detection_engine import detect_pattern, calculate_scores
from services.ml_model import predict_session

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.route("/api/ingest", methods=["POST", "OPTIONS"])
def ingest():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    data = request.json or {}
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build a row dict that detection_engine expects
    row = {
        "BounceRates":              data.get("BounceRates", 0),
        "ExitRates":                data.get("ExitRates", 0),
        "ProductRelated":           data.get("ProductRelated", 0),
        "ProductRelated_Duration":  data.get("ProductRelated_Duration", 0),
        "Revenue":                  data.get("Revenue", 0),
    }

    pattern = detect_pattern(row)
    clicks_to_reject, dp_score, ethical_score = calculate_scores(row)

    user_id    = data.get("user_id",    "U_manual")
    session_id = data.get("session_id", "S_manual")

    # 1. Clickstream
    event = {
        "user_id":    user_id,
        "session_id": session_id,
        "page":       data.get("page"),
        "action":     data.get("action"),
        "time_spent": data.get("time_spent"),
        "timestamp":  now_iso,
        "pattern":    pattern,          # ← was hard-coded "manual"
    }
    clickstream_collection.insert_one(event)

    # 2. Session  ← was missing entirely
    session_doc = {
        "user_id":         user_id,
        "session_id":      session_id,
        "pattern":         pattern,
        "dp_score":        dp_score,
        "ethical_score":   ethical_score,
        "clicks_to_reject": clicks_to_reject,
        "session_length":  int(row["ProductRelated"]),
        "path":            [data.get("page", "Unknown")],
    }
    sessions_collection.insert_one(session_doc)

    # 3. Alert (only when a dark pattern is detected)  ← was missing entirely
    alert_doc = None
    if pattern != "none":
        alert_doc = {
            "severity": "high" if dp_score > 70 else "medium",
            "title":    f"{pattern.title()} pattern detected",
            "desc":     f"Suspicious behavior in session {session_id}",
            "icon":     "ti-alert-triangle",
        }
        alerts_collection.insert_one(alert_doc)

    event_out = {k: v for k, v in event.items() if k != "_id"}
    return jsonify({
        "message": "Event ingested successfully",
        "event":   event_out,
        "session": {k: v for k, v in session_doc.items() if k != "_id"},
        "alert":   {k: v for k, v in alert_doc.items() if k != "_id"} if alert_doc else None,
    }) 