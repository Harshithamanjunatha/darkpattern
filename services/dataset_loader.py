import pandas as pd
from datetime import datetime, timezone

from database.db import (
    clickstream_collection,
    sessions_collection,
    alerts_collection
)

from services.detection_engine import (
    detect_pattern,
    calculate_scores
)

from services.ml_model import predict_session, retrain_model
from config import DEFAULT_CSV


# Required columns for the uploaded CSV
REQUIRED_COLS = {
    'BounceRates', 'ExitRates', 'ProductRelated',
    'ProductRelated_Duration', 'VisitorType'
}


def validate_columns(df):
    """Return a list of missing required column names."""
    missing = REQUIRED_COLS - set(df.columns)
    return list(missing)


# -----------------------------------
# COMMON PROCESSOR
# -----------------------------------

def process_dataset(df, merge=False):
    """Process a dataframe into MongoDB collections.

    Args:
        df:    pandas DataFrame with the shoppers dataset.
        merge: if False (default) clears existing data first;
               if True the new rows are appended to existing data.
    """

    if not merge:
        clickstream_collection.delete_many({})
        sessions_collection.delete_many({})
        alerts_collection.delete_many({})

    # Cleaning
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)

    if 'Weekend' in df.columns:
        df['Weekend'] = df['Weekend'].astype(int)
    if 'Revenue' in df.columns:
        df['Revenue'] = df['Revenue'].astype(int)

    df['VisitorType'] = (
        df['VisitorType']
        .map({'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 2})
        .fillna(0)
        .astype(int)
    )

    clickstream_data = []
    session_data = []
    alerts_data = []

    for index, row in df.iterrows():

        user_id = f"U{index+1:05d}"
        session_id = f"S{index+1:06d}"

        pattern = detect_pattern(row)
        ml_prediction = predict_session(row)
        clicks_to_reject, dp_score, ethical_score = calculate_scores(row)

        path = ["Home", "Product", "Cart"]

        if pattern == "forced":
            path.append("Insurance popup")
        elif pattern == "loop":
            path.extend(["Cancel flow", "Confirmation", "Cancel flow"])
        elif pattern == "trap":
            path.append("Subscription trap")
        elif pattern == "hidden":
            path.append("Hidden opt-out")

        path.append("Payment")

        # Use plain ISO string — avoids pandas Timestamp JSON serialisation issues
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        clickstream_data.append({
            "user_id": user_id,
            "session_id": session_id,
            "page": path[-1],
            "action": "click",
            "time_spent": float(row['ProductRelated_Duration']),
            "timestamp": now_iso,
            "pattern": pattern
        })

        session_data.append({
            "user_id": user_id,
            "session_id": session_id,
            "pattern": pattern,
            "ml_prediction": ml_prediction,
            "path": path,
            "dp_score": dp_score,
            "ethical_score": ethical_score,
            "clicks_to_reject": clicks_to_reject,
            "session_length": int(row['ProductRelated'])
        })

        if pattern != "none":
            alerts_data.append({
                "severity": "high" if dp_score > 70 else "medium",
                "title": f"{pattern.title()} pattern detected",
                "desc": f"Suspicious behavior in session {session_id}",
                "icon": "ti-alert-triangle"
            })

    if clickstream_data:
        clickstream_collection.insert_many(clickstream_data)
    if session_data:
        sessions_collection.insert_many(session_data)
    if alerts_data:
        alerts_collection.insert_many(alerts_data)

    print("Dataset Processed Successfully!")


# -----------------------------------
# DEFAULT CSV
# -----------------------------------

def load_dataset():
    df = pd.read_csv(DEFAULT_CSV)
    process_dataset(df)


# -----------------------------------
# UPLOADED CSV
# -----------------------------------

def load_uploaded_dataset(df, merge=False):
    """Validate, process, and retrain the model on an uploaded dataframe.

    Returns:
        (ok: bool, error: str|None)
    """
    missing = validate_columns(df)
    if missing:
        return False, f"Missing required columns: {', '.join(sorted(missing))}"

    process_dataset(df, merge=merge)

    # Retrain the ML model on the new data
    try:
        retrain_model(df)
    except Exception as exc:
        print(f"Warning: model retrain failed — {exc}")

    return True, None
