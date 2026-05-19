from flask import Blueprint, jsonify

from database.db import (
    sessions_collection,
    clickstream_collection
)

charts_bp = Blueprint("charts", __name__)


@charts_bp.route("/api/charts/clicks_distribution")
def clicks_distribution():

    pipeline = [
        {
            "$group": {
                "_id": "$clicks_to_reject",
                "users": {"$sum": 1}
            }
        }
    ]

    result = list(
        sessions_collection.aggregate(pipeline)
    )

    data = []

    for r in result:
        data.append({
            "clicks": r["_id"],
            "users": r["users"]
        })

    return jsonify(data)


@charts_bp.route("/api/charts/page_visits")
def page_visits():

    pipeline = [
        {
            "$group": {
                "_id": "$page",
                "visits": {"$sum": 1}
            }
        }
    ]

    result = list(
        clickstream_collection.aggregate(pipeline)
    )

    data = []

    for r in result:
        data.append({
            "page": r["_id"],
            "visits": r["visits"]
        })

    return jsonify(data)


@charts_bp.route("/api/charts/action_types")
def action_types():

    pipeline = [
        {
            "$group": {
                "_id": "$action",
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(
        clickstream_collection.aggregate(pipeline)
    )

    data = []

    for r in result:
        data.append({
            "action": r["_id"],
            "count": r["count"]
        })

    return jsonify(data)


@charts_bp.route("/api/charts/scatter")
def scatter():

    sessions = list(
        sessions_collection.find(
            {},
            {
                "_id": 0,
                "pattern": 1,
                "session_length": 1,
                "dp_score": 1
            }
        ).limit(300)
    )

    return jsonify(sessions)


@charts_bp.route("/api/charts/top_flows")
def top_flows():

    pipeline = [
        {
            "$match": {
                "pattern": {"$ne": "none"}
            }
        },
        {
            "$group": {
                "_id": "$pattern",
                "users": {"$sum": 1},
                "avg_clicks": {
                    "$avg": "$clicks_to_reject"
                }
            }
        }
    ]

    result = list(
        sessions_collection.aggregate(pipeline)
    )

    data = []

    for r in result:
        data.append({
            "pattern": r["_id"],
            "users": r["users"],
            "avg_clicks": round(r["avg_clicks"], 1)
        })

    return jsonify(data)