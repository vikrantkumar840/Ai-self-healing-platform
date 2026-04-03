from fastapi import FastAPI
import requests

app = FastAPI()
AI_ENGINE_URL = "http://ai-engine-service:8000/analyze"  # URL of the AI Engine service

@app.post("/alert")
async def receive_alert(alert: dict):
    print(f"Received alert: {alert}")
    # Forward the alert to the AI Engine for analysis

    response = requests.post(AI_ENGINE_URL, json=alert)
    return {"status": "sent to AI Engine", "response": response.json()}