def recommend_destinations(destinations, budget, duration_days, interests, climate="Any", limit=6):
    """Explainable content-based scoring; returns (destination, score, reasons) tuples."""
    wanted = {x.strip().lower() for x in (interests or "").split(",") if x.strip()}
    results = []
    for destination in destinations:
        score = 0
        reasons = []
        cost = destination.estimated_cost or 0
        if cost <= budget:
            score += 35
            reasons.append("fits your budget")
        elif budget > 0:
            ratio = budget / max(cost, 1)
            score += max(0, int(20 * ratio))
            reasons.append("may need a higher budget")
        else:
            reasons.append("budget not provided")

        if destination.min_days <= duration_days <= destination.max_days:
            score += 25
            reasons.append("matches your trip duration")
        else:
            gap = min(abs(duration_days - destination.min_days), abs(duration_days - destination.max_days))
            score += max(0, 15 - gap * 5)
            if gap <= 1:
                reasons.append("duration is close to your preference")

        available = {x.strip().lower() for x in (destination.activities or "").split(",")}
        matches = wanted & available
        if wanted:
            score += int(30 * len(matches) / len(wanted))
            if matches:
                reasons.append("matches interests: " + ", ".join(sorted(matches)))
        else:
            score += 15
            reasons.append("broad-interest match")

        if climate and climate.lower() != "any":
            if (destination.climate or "").lower() == climate.lower():
                score += 10
                reasons.append("matches your climate preference")

        results.append((destination, min(score, 100), reasons))
    return sorted(results, key=lambda item: (-item[1], item[0].estimated_cost))[:limit]
