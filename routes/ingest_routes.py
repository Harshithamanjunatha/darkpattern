from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from database.db import clickstream_collection

ingest_bp = Blueprint("ingest", __name__)


@ingest_bp.route("/api/ingest", methods=["POST", "OPTIONS"])
def ingest():

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    data = request.json or {}

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    event = {
        "user_id":    data.get("user_id"),
        "session_id": data.get("session_id"),
        "page":       data.get("page"),
        "action":     data.get("action"),
        "time_spent": data.get("time_spent"),
        "timestamp":  now_iso,
        "pattern":    "manual"
    }

    clickstream_collection.insert_one(event)

    # Return the saved event (without MongoDB _id) so the UI can prepend it
    event_out = {k: v for k, v in event.items() if k != "_id"}

    return jsonify({
        "message": "Event ingested successfully",
        "event": event_out
    })
