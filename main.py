from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, os, openai
from database import init_db, save_trip, get_all_trips

init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    destination: str
    dates: str
    interests: str
    budget: str

@app.get("/trips")
def list_trips():
    return get_all_trips()

@app.post("/generate")
def generate_itinerary(req: TripRequest):
    try:
        prompt = f"Plan a {req.budget} budget trip to {req.destination} from {req.dates} focusing on {req.interests}. Provide a daily itinerary with activities and food suggestions."
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful trip planner."},
                      {"role": "user", "content": prompt}]
        )
        itinerary = response['choices'][0]['message']['content']
        save_trip(req.destination, req.dates, req.interests, req.budget, itinerary)
        return {"itinerary": itinerary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))