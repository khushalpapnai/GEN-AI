import math

# ---------------- Wilson Score ----------------
def wilson_score(pos, total, z=1.96):
    """
    Wilson score confidence interval lower bound.
    z=1.96 → 95% confidence
    """
    if total == 0:
        return 0
    phat = 1.0 * pos / total
    return (phat + z*z/(2*total) - z * math.sqrt((phat*(1-phat)+z*z/(4*total))/total)) / (1+z*z/total) 