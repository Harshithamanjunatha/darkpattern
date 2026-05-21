from flask import Blueprint
from flask import request
from flask import jsonify

from services.dataset_loader import load_dataset

regenerate_bp = Blueprint(
    "regenerate",
    __name__
)


@regenerate_bp.route(
    "/api/regenerate",
    methods=["POST"]
)
def regenerate():
    """Re-seed the database from the default CSV dataset."""

    load_dataset()

    return jsonify({
        "message": "Database regenerated successfully"
    })
