from typing import TypedDict, Optional


class SafetyState(TypedDict):
    user_question: str

    location_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    activity: Optional[str]
    time_reference: Optional[str]
    target_time: Optional[object]

    weather: Optional[dict]

    matched_sops: list
    selected_sop: Optional[dict]

    answer: Optional[str]
    error: Optional[str]