from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.graph.graph import graph
from backend.session import sessions

from pathlib import Path


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/")
def home():
    frontend_file = (
        Path(__file__).resolve().parent.parent
        / "frontend"
        / "index.html"
    )

    return FileResponse(frontend_file)


@app.post("/chat")
def chat(request: ChatRequest):

    previous_state = sessions.get(request.session_id)

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
        "user_question": request.message,

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


    sessions[request.session_id] = result


    return {
        "answer": result["answer"],
        "activity": result["activity"],
        "location": result["location_name"],
        "time_reference": result["time_reference"],
        "selected_sop": result["selected_sop"]
    }