import numpy as np
from datetime import datetime

# ---------------- Freshness ----------------
half_life_days = 30
def compute_freshness_score(reviews):
    """
    Recent reviews have more weight.
    half_life_days → after this many days, weight ≈ 0.5
    """
    now = datetime.now()
    scores = []
    for r in reviews:
        created_at = datetime.fromisoformat(r["createdAt"].replace("Z", ""))
        days_diff = (now - created_at).days
        freshness = 0.5 ** (days_diff / half_life_days)  # exponential decay
        scores.append(freshness)
    return np.mean(scores) if scores else 0