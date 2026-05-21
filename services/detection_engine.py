def detect_pattern(row):

    pattern = "none"

    if row['BounceRates'] > 0.15:
        pattern = "hidden"

    if row['ExitRates'] > 0.20:
        pattern = "loop"

    if row['ProductRelated'] > 50:
        pattern = "forced"

    if (
        row['ProductRelated_Duration'] > 2000
        and row['Revenue'] == 0
    ):
        pattern = "trap"

    return pattern


def calculate_scores(row):

    clicks_to_reject = int(row['ProductRelated'] // 10) + 1

    dp_score = min(100, clicks_to_reject * 10)

    ethical_score = max(0, 100 - dp_score)

    return clicks_to_reject, dp_score, ethical_score