import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from config import DEFAULT_CSV


model = None

VISITOR_MAP = {
    'Returning_Visitor': 1,
    'New_Visitor': 0,
    'Other': 2
}


def _prepare_features(df):
    """Clean and extract feature columns from a dataframe."""
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)

    if 'Weekend' in df.columns:
        df['Weekend'] = df['Weekend'].astype(int)
    if 'Revenue' in df.columns:
        df['Revenue'] = df['Revenue'].astype(int)

    # Map VisitorType; unmapped / NaN values fall back to 0
    df['VisitorType'] = (
        df['VisitorType']
        .map(VISITOR_MAP)
        .fillna(0)
        .astype(int)
    )

    df['Suspicious'] = (
        (df['BounceRates'] > 0.15) |
        (df['ExitRates'] > 0.20) |
        (df['ProductRelated'] > 50)
    ).astype(int)

    return df


def _fit(df):
    """Train the decision tree on a prepared dataframe and return the model."""
    df = _prepare_features(df)

    feature_cols = [
        'BounceRates',
        'ExitRates',
        'ProductRelated',
        'ProductRelated_Duration',
        'VisitorType'
    ]

    X = df[feature_cols]
    y = df['Suspicious']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, clf.predict(X_test))
    print(f"Decision Tree Accuracy: {accuracy:.2f}")

    return clf


def train_model():
    """Train the model on the default CSV."""
    global model
    df = pd.read_csv(DEFAULT_CSV)
    model = _fit(df)
    return model


def retrain_model(df):
    """Retrain the model on a new (uploaded) dataframe."""
    global model
    model = _fit(df)
    return model


def predict_session(row):
    global model
    if model is None:
        train_model()

    # Ensure VisitorType is numeric (handle string values in raw rows)
    visitor_type = row.get('VisitorType', 0)
    if isinstance(visitor_type, str):
        visitor_type = VISITOR_MAP.get(visitor_type, 0)
    try:
        if pd.isna(visitor_type):
            visitor_type = 0
    except (TypeError, ValueError):
        visitor_type = 0

    features = [[
        row['BounceRates'],
        row['ExitRates'],
        row['ProductRelated'],
        row['ProductRelated_Duration'],
        visitor_type
    ]]

    prediction = model.predict(features)[0]
    return "suspicious" if prediction == 1 else "normal"
