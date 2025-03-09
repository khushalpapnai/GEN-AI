import numpy as np
from datetime import datetime, UTC
from utils.freshness_score import compute_freshness_score
from utils.sentiment import predict_sentiment
from utils.wilson_score import wilson_score


def rank_property(property_data):
    reviews = property_data.get("reviews", [])
    if not reviews:
        return 0  # no reviews → neutral score

    comments = [r["reviewComment"] for r in reviews]
    ratings = [r["rating"] for r in reviews]

    sentiment_preds = predict_sentiment(comments)
    sentiment_score = np.mean(sentiment_preds)
    avg_rating = np.mean(ratings) / 5.0
    freshness_score = compute_freshness_score(reviews)

    pos_count = int(sum(sentiment_preds))
    conf_score = wilson_score(pos_count, len(reviews))

    # ✅ Recent negative review penalty
    now = datetime.now(UTC)
    recent_reviews = [
        r for r in reviews
        if (now - datetime.fromisoformat(r["createdAt"].replace("Z", "")).replace(tzinfo=UTC)).days <= 30
    ]

    if recent_reviews:
        neg_recent = sum(
            1 for r in recent_reviews
            if predict_sentiment([r["reviewComment"]])[0] == 0
        )
        penalty = 0.7 if neg_recent / len(recent_reviews) > 0.6 else 1.0
    else:
        penalty = 1.0

    final_score = (
        0.4 * sentiment_score +
        0.3 * avg_rating +
        0.2 * freshness_score +
        0.1 * conf_score
    ) * penalty

    return round(final_score, 3)


def rank_properties(property_list):
    """
    Takes a list of properties, ranks them using rank_property,
    and returns them sorted in descending order of score.
    """
    scored = [(prop, rank_property(prop)) for prop in property_list]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
