from langgraph.graph import StateGraph, START, END

from backend.graph.state import SafetyState

from backend.graph.nodes import (
    understand_query,
    resolve_location,
    determine_time,
    fetch_weather,
    match_safety_procedures,
    generate_answer,
    validate_answer,
    no_sop
)


def location_check(state):
    if state["error"]:
        return "location_failure"

    return "determine_time"


def weather_check(state):
    if state["error"]:
        return "weather_failure"

    return "match_sops"


def sop_check(state):
    if state["error"]:
        return "weather_failure"

    if not state["matched_sops"]:
        return "no_sop"

    return "generate_answer"


def answer_check(state):
    if state["error"]:
        return "safe_fallback"

    return "end"


builder = StateGraph(SafetyState)


builder.add_node(
    "understand_query",
    understand_query
)

builder.add_node(
    "resolve_location",
    resolve_location
)

builder.add_node(
    "determine_time",
    determine_time
)

builder.add_node(
    "fetch_weather",
    fetch_weather
)

builder.add_node(
    "match_sops",
    match_safety_procedures
)

builder.add_node(
    "generate_answer",
    generate_answer
)

builder.add_node(
    "validate_answer",
    validate_answer
)

builder.add_node(
    "no_sop",
    no_sop
)

builder.add_node(
    "location_failure",
    lambda state: {
        "answer": state["error"]
    }
)

builder.add_node(
    "weather_failure",
    lambda state: {
        "answer": state["error"]
    }
)

builder.add_node(
    "safe_fallback",
    lambda state: {
        "answer": (
            "I could not verify that the generated answer "
            "was fully grounded in the available weather data "
            "and applicable SOP. I will not provide an "
            "unverified safety recommendation."
        )
    }
)


builder.add_edge(
    START,
    "understand_query"
)

builder.add_edge(
    "understand_query",
    "resolve_location"
)


builder.add_conditional_edges(
    "resolve_location",
    location_check,
    {
        "determine_time": "determine_time",
        "location_failure": "location_failure"
    }
)


builder.add_edge(
    "determine_time",
    "fetch_weather"
)


builder.add_conditional_edges(
    "fetch_weather",
    weather_check,
    {
        "match_sops": "match_sops",
        "weather_failure": "weather_failure"
    }
)


builder.add_conditional_edges(
    "match_sops",
    sop_check,
    {
        "generate_answer": "generate_answer",
        "no_sop": "no_sop",
        "weather_failure": "weather_failure"
    }
)


builder.add_edge(
    "generate_answer",
    "validate_answer"
)


builder.add_conditional_edges(
    "validate_answer",
    answer_check,
    {
        "end": END,
        "safe_fallback": "safe_fallback"
    }
)


builder.add_edge(
    "no_sop",
    END
)

builder.add_edge(
    "location_failure",
    END
)

builder.add_edge(
    "weather_failure",
    END
)

builder.add_edge(
    "safe_fallback",
    END
)


graph = builder.compile()