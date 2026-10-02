from datetime import datetime, timedelta


TIME_MAPPING = {
    "this morning": 9,
    "this afternoon": 15,
    "this evening": 18,
    "tonight": 21,
    "tomorrow morning": 9,
    "tomorrow afternoon": 15,
    "tomorrow evening": 18,
    "tomorrow night": 21
}


def resolve_time(time_reference):
    now = datetime.now()

    if time_reference == "right now":
        return now

    if time_reference in TIME_MAPPING:
        hour = TIME_MAPPING[time_reference]

        target_date = now.date()

        if time_reference.startswith("tomorrow"):
            target_date = target_date + timedelta(days=1)

        return datetime.combine(
            target_date,
            datetime.min.time()
        ).replace(hour=hour)

    return now