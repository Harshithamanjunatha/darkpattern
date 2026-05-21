import pandas as pd

from flask import Blueprint, request, jsonify

from services.dataset_loader import load_uploaded_dataset

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_dataset():

    file = request.files.get("dataset")
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    # merge=true keeps existing data; merge=false (default) replaces it
    merge = request.form.get("merge", "false").lower() == "true"

    try:
        df = pd.read_csv(file)
    except Exception as exc:
        return jsonify({"error": f"Could not parse CSV: {exc}"}), 400

    ok, error = load_uploaded_dataset(df, merge=merge)
    if not ok:
        return jsonify({"error": error}), 422

    return jsonify({
        "message": "Dataset uploaded and processed successfully",
        "rows": len(df),
        "mode": "merge" if merge else "replace"
    })
