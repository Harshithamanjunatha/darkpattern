from flask import Blueprint
from flask import jsonify
from flask import request

from database.db import (
    clickstream_collection
)

clickstream_bp = Blueprint(
    "clickstream",
    __name__
)


@clickstream_bp.route("/api/clickstream")
def get_clickstream():

    limit = int(
        request.args.get(
            "limit",
            50
        )
    )

    pattern = request.args.get(
        "pattern",
        "all"
    )

    query = {}

    if pattern != "all":

        query["pattern"] = pattern

    events = list(

        clickstream_collection.find(
            query,
            {"_id": 0}
        ).limit(limit)

    )

    total = clickstream_collection.count_documents(query)

    return jsonify({

        "events": events,

        "total": total

    })