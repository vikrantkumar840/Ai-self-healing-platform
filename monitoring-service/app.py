# AFTER (fixed)
from fastapi import FastAPI
import httpx             # ✅ fix 1: was missing → NameError crash
import os               # ✅ fix 2: needed for os.getenv
import logging
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ fix 3: reads env var + correct service name + correct endpoint /alert
AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://ai-engine:8000/alert")

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/alert")
async def receive_alert(alert: dict):
    logger.info(f"Received alert: {alert}")  # ✅ proper logging
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(AI_ENGINE_URL, json=alert)
    return {"status": "sent to AI Engine", "response": response.json()}