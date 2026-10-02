# Outdoor Safety Agent

An outdoor activity safety assistant that combines a user's activity, location, and time with live weather data and a local set of safety procedures (SOPs). The application is intentionally conservative: it only gives a recommendation when an applicable SOP is found and the final answer can be verified against the selected SOP and weather response.

## What It Does

The agent accepts natural-language questions such as:

> Is it safe to cycle in Bhopal right now?

It then:

1. Extracts the activity, location, and time reference from the question.
2. Resolves the location through the Open-Meteo geocoding API.
3. Resolves the requested time, defaulting to the current time.
4. Retrieves current or hourly weather from Open-Meteo.
5. Matches the weather and activity against the local SOP catalogue.
6. Generates an answer containing the relevant weather values and SOP guidance.
7. Validates that the answer is grounded in the selected SOP and API response.

If the location, weather, or safety procedure cannot be verified, the agent returns a safe failure message instead of inventing advice.

## Features

- Natural-language activity and location extraction using Google Gemini.
- Session-aware follow-up questions through a browser-generated session ID.
- Current-weather and future-hour weather queries.
- Local, deterministic SOP matching from `backend/policies/sops.json`.
- Grounding validation for SOP IDs and weather values in generated answers.
- Safe handling for missing locations, unavailable weather, missing weather fields, and unmatched activities.
- Simple browser UI served directly by the FastAPI backend.
- Deterministic graph tests with mocked Gemini and weather responses.


### External services

- **Google Gemini**: extracts structured fields from the user's question. It does not directly decide the safety recommendation.
- **Open-Meteo Geocoding API**: resolves a city or place name to coordinates.
- **Open-Meteo Forecast API**: provides current and hourly weather data.

### Local policy data

Safety rules are stored in `backend/policies/sops.json`. The matcher evaluates activity-specific conditions and weather thresholds, then selects the highest-priority applicable SOP. The generated recommendation is based on the selected SOP's guidance.

## Supported Activities

The query-understanding step normalizes common wording to these activity names:

- `cycling`
- `running`
- `walking`
- `hiking`
- `motorcycle`
- `scooter`
- `picnic`
- `park_visit`

The available SOPs and their exact thresholds are defined in `backend/policies/sops.json`; that file is the source of truth.

## Requirements

- Python 3.10 or newer recommended
- A Google Gemini API key
- Internet access for Gemini and Open-Meteo requests

Install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The key is loaded by `backend/llm/client.py`. Do not commit `.env` or expose the API key in the frontend.

## Run the Application

From the project root, start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

Open the web interface at [http://127.0.0.1:8000](http://127.0.0.1:8000).

The frontend stores a UUID in browser `localStorage` and sends it with every request, allowing follow-up questions to reuse the previous activity, location, and time context.

## API

### `GET /`

Returns the browser frontend from `frontend/index.html`.

### `POST /chat`

Request body:

```json
{
	"session_id": "a-browser-session-uuid",
	"message": "Is it safe to cycle in Bhopal right now?"
}
```

Response body:

```json
{
	"answer": "...",
	"activity": "cycling",
	"location": "Bhopal",
	"time_reference": "right now",
	"selected_sop": {
		"id": "SOP-001"
	}
}
```

The complete selected SOP object is returned when a procedure applies. When no SOP applies or a dependency fails, `selected_sop` may be `null` and `answer` contains the safe failure message.

Example request with `curl`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
	-H "Content-Type: application/json" \
	-d '{"session_id":"demo-session","message":"Should I hike in Bhopal tomorrow morning?"}'
```

## Testing

The primary reproducible test suite is the deterministic evaluation script. Run it from the project root:

```bash
python evals/run_evals.py
```

It covers the graph workflow, paraphrased activity matching, severe-weather handling, no-SOP behavior, and missing-weather safety behavior. External Gemini and weather calls are mocked, so the results are reproducible.

The repository also contains component smoke scripts. Run each one from its containing directory because the scripts use local-module imports:

```bash
(cd backend/policies && python test_matcher.py)
(cd backend/policies && python test_missing_weather.py)
(cd backend/weather && python test_time_resolver.py)
(cd backend/weather && python test_hourly_selector.py)
(cd backend/weather && python test_weather.py)
```

The weather smoke scripts call Open-Meteo and therefore require internet access. `backend/llm/test_client.py` calls Gemini directly and requires `GEMINI_API_KEY`.

The files are currently script-style checks rather than pytest test functions, so running `python -m pytest` from the repository root is not the supported validation command.

For an optional live Open-Meteo check:

```bash
python evals/live_weather_evals.py
```

The live check depends on changing real-world weather and is not a substitute for the deterministic tests. It may report `NOT APPLICABLE` when current conditions do not meet the severe-weather thresholds.

## Deploy on Render

The repository includes `render.yaml` for deployment as a single Render Web Service.

1. Sign in to [Render](https://render.com) and select **New +** -> **Blueprint**.
2. Connect the GitHub repository `Kulkarni-arnav/Brainwave`.
3. Select the `main` branch and apply the blueprint.
4. Open the service's **Environment** settings and add `GEMINI_API_KEY`.
5. Deploy the service and open the generated `onrender.com` URL.

Render uses the following commands from `render.yaml`:

```text
Build: pip install -r requirements.txt
Start: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

The Open-Meteo APIs do not require an API key. The Gemini key must be configured as a Render environment variable; never commit it to GitHub. The current frontend calls `http://127.0.0.1:8000/chat`, so after deploying the backend, update that URL in `frontend/index.html` to the Render service URL and push the change, or serve the frontend locally while pointing it at the deployed API.

## Project Structure

```text
.
├── backend/
│   ├── main.py                 FastAPI app and /chat endpoint
│   ├── session.py              In-memory conversation state
│   ├── graph/
│   │   ├── graph.py            LangGraph workflow and routing
│   │   ├── nodes.py            Query, weather, SOP, and validation nodes
│   │   └── state.py            Shared graph state schema
│   ├── llm/
│   │   └── client.py           Gemini client setup
│   ├── policies/
│   │   ├── sops.json           Safety procedures and thresholds
│   │   ├── loader.py            SOP file loading
│   │   └── matcher.py           SOP matching and selection
│   └── weather/
│       ├── open_meteo.py       Geocoding and weather API calls
│       ├── hourly_selector.py  Weather selection for a target time
│       └── time_resolver.py    Natural-language time resolution
├── evals/                      Deterministic and live evaluation scripts
├── frontend/index.html         Browser chat interface
├── requirements.txt            Python dependencies
└── README.md                   Project documentation
```

## Design and Safety Notes

- The system is a decision-support prototype, not a replacement for official weather alerts, emergency services, or professional judgment.
- Weather data can become stale or unavailable. The application fails closed when it cannot verify the required inputs.
- Session state is stored in process memory, so it is lost when the server restarts and is not suitable for multi-process production deployment without a shared session store.
- CORS is currently configured to allow all origins for local development. Production deployments should restrict `allow_origins` to trusted frontend origins.
- The frontend currently expects the backend at `http://127.0.0.1:8000`; update that URL before deploying the frontend separately.
- API calls use a 10-second timeout, but retries, authentication, rate limiting, and observability would be needed for production hardening.

## Future Improvements

- Persist sessions in a database or shared cache.
- Add structured API error responses and request validation for production clients.
- Add authentication, rate limiting, logging, and metrics.
- Expand location support beyond city-name geocoding.
- Add a richer frontend with visible weather details and selected SOP metadata.
- Add timezone-aware testing for more time references and edge cases.

## License

No license has been specified for this project yet.
