from flask import Blueprint
from flask import jsonify

from database.db import (
    sessions_collection
)

health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route("/api/health")
def health():

    return jsonify({

        "status": "online",

        "sessions":
            sessions_collection.count_documents({})
    })