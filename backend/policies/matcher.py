SEVERITY_ORDER = {
    "low": 1,
    "moderate": 2,
    "high": 3,
    "critical": 4
}


class MissingWeatherDataError(Exception):
    pass


def evaluate_condition(condition, weather):
    field = condition["field"]
    operator = condition["operator"]
    expected = condition["value"]

    if field not in weather:
        raise MissingWeatherDataError(
            f"Missing weather field: {field}"
        )

    actual = weather[field]

    if operator == ">":
        return actual > expected

    if operator == ">=":
        return actual >= expected

    if operator == "<":
        return actual < expected

    if operator == "<=":
        return actual <= expected

    if operator == "==":
        return actual == expected

    if operator == "!=":
        return actual != expected

    return False


def evaluate_rule(rule, weather):
    if "all" in rule:
        return all(
            evaluate_rule(item, weather)
            if "all" in item or "any" in item
            else evaluate_condition(item, weather)
            for item in rule["all"]
        )

    if "any" in rule:
        return any(
            evaluate_rule(item, weather)
            if "all" in item or "any" in item
            else evaluate_condition(item, weather)
            for item in rule["any"]
        )

    return False


def activity_matches(sop, activity):
    activities = sop.get("applies_to", {}).get("activities", [])

    return activity in activities


def match_sops(sops, activity, weather):
    matched = []

    for sop in sops:
        if not activity_matches(sop, activity):
            continue

        for field in sop.get("required_weather_fields", []):
            if field not in weather:
                raise MissingWeatherDataError(
                    f"Missing required weather field: {field}"
                )

        if evaluate_rule(sop["rule"], weather):
            matched.append(sop)

    return matched


def select_sop(matched_sops):
    if not matched_sops:
        return None

    return max(
        matched_sops,
        key=lambda sop: SEVERITY_ORDER.get(
            sop["severity"],
            0
        )
    )