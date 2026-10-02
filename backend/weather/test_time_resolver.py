from time_resolver import resolve_time


test_times = [
    "right now",
    "this morning",
    "this afternoon",
    "this evening",
    "tonight",
    "tomorrow morning",
    "tomorrow afternoon",
    "tomorrow evening",
    "tomorrow night"
]


for time_reference in test_times:
    result = resolve_time(time_reference)

    print(
        time_reference,
        "->",
        result
    )