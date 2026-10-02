from graph import graph
from session import sessions


def run_chat(session_id, question):

    previous_state = sessions.get(session_id)

    if previous_state:
        location_name = previous_state["location_name"]
        latitude = previous_state["latitude"]
        longitude = previous_state["longitude"]

        activity = previous_state["activity"]
        time_reference = previous_state["time_reference"]

    else:
        location_name = None
        latitude = None
        longitude = None

        activity = None
        time_reference = None

    initial_state = {
        "user_question": question,

        "location_name": location_name,
        "latitude": latitude,
        "longitude": longitude,

        "activity": activity,
        "time_reference": time_reference,
        "target_time": None,

        "weather": None,

        "matched_sops": [],
        "selected_sop": None,

        "answer": None,
        "error": None
    }

    result = graph.invoke(initial_state)

    sessions[session_id] = result

    return result


result = run_chat(
    "test-user",
    "Would it be okay to go for a bike ride in Bhopal this evening?"
)

print("\nFIRST ANSWER:")
print(result["answer"])


result = run_chat(
    "test-user",
    "What about tomorrow morning?"
)

print("\nSECOND ANSWER:")
print(result["answer"])

print("\nREMEMBERED ACTIVITY:")
print(result["activity"])

print("\nREMEMBERED LOCATION:")
print(result["location_name"])