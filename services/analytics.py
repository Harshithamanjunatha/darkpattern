from database.db import (
    sessions_collection,
    clickstream_collection,
    alerts_collection
)


def get_total_sessions():

    return sessions_collection.count_documents({})


def get_total_events():

    return clickstream_collection.count_documents({})


def get_suspicious_sessions():

    return sessions_collection.count_documents({
        "pattern": {"$ne": "none"}
    })


def get_high_alerts():

    return alerts_collection.count_documents({
        "severity": "high"
    })


def get_average_ethical_score():

    pipeline = [
        {
            "$group": {
                "_id": None,
                "avgScore": {
                    "$avg": "$ethical_score"
                }
            }
        }
    ]

    result = list(
        sessions_collection.aggregate(pipeline)
    )

    if result:
        return round(result[0]["avgScore"], 2)

    return 0


def get_pattern_distribution():

    pipeline = [
        {
            "$group": {
                "_id": "$pattern",
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(
        sessions_collection.aggregate(pipeline)
    )

    distribution = {}

    for item in result:
        distribution[item["_id"]] = item["count"]

    return distribution


def get_page_visits():

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

    return result


def get_action_counts():

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

    return result

def get_avg_clicks_to_reject():

    pipeline = [
        {
            "$group": {
                "_id": None,
                "avgClicks": {
                    "$avg": "$clicks_to_reject"
                }
            }
        }
    ]

    result = list(
        sessions_collection.aggregate(pipeline)
    )

    if result and result[0]["avgClicks"] is not None:
        return round(result[0]["avgClicks"], 2)

    return 0
