from flask import Blueprint
from flask import jsonify
from flask import request

from database.db import (
    sessions_collection
)

sessions_bp = Blueprint(
    "sessions",
    __name__
)


@sessions_bp.route("/api/sessions")
def get_sessions():

    # ---------------- GET FILTERS ----------------

    pattern = request.args.get(
        "pattern",
        "all"
    )

    limit = int(
        request.args.get(
            "limit",
            20
        )
    )

    offset = int(
        request.args.get(
            "offset",
            0
        )
    )

    user_id = request.args.get(
        "user_id"
    )

    # ---------------- BUILD QUERY ----------------

    query = {}

    # Pattern filter

    if pattern != "all":

        query["pattern"] = pattern

    # User search

    if user_id:

        query["user_id"] = user_id

    # ---------------- FETCH DATA ----------------

    raw_sessions = list(

        sessions_collection.find(
            query,
            {"_id": 0}
        ).skip(offset).limit(limit)

    )

    total = sessions_collection.count_documents(query)

    # ---------------- REMOVE DUPLICATES ----------------

    unique_sessions = []

    seen_ids = set()

    for session in raw_sessions:

        sid = session.get("session_id")

        if sid in seen_ids:

            continue

        seen_ids.add(sid)

        unique_sessions.append(session)

    # ---------------- RESPONSE ----------------

    return jsonify({

        "sessions": unique_sessions,

        "total": total

    })