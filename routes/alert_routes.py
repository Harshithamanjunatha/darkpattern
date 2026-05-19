from flask import Blueprint, jsonify
from database.db import alerts_collection

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/api/alerts")
def get_alerts():

    alerts = list(
        alerts_collection.find({}, {"_id": 0})
    )

    return jsonify(alerts)