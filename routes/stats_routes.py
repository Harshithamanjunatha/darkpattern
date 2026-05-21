from flask import Blueprint, jsonify

from services.analytics import (
    get_total_sessions,
    get_total_events,
    get_suspicious_sessions,
    get_high_alerts,
    get_average_ethical_score,
    get_pattern_distribution,
    get_avg_clicks_to_reject
)

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/stats")
def get_stats():

    return jsonify({
        "total_sessions":      get_total_sessions(),
        "total_events":        get_total_events(),
        "suspicious_sessions": get_suspicious_sessions(),
        "high_alerts":         get_high_alerts(),
        "avg_clicks_to_reject": get_avg_clicks_to_reject(),
        "ethical_score":       get_average_ethical_score(),
        "pattern_distribution": get_pattern_distribution()
    })
