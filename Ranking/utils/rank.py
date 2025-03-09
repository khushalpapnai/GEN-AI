from utils.rank_property import rank_property

def rank(properties):
    # Compute score for each property
    for prop in properties:
        prop["rankingScore"] = rank_property(prop)

    # Sort by score (descending -> best first)
    sorted_properties = sorted(properties, key=lambda x: x["rankingScore"], reverse=True)

    return sorted_properties