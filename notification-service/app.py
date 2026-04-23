from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-service")

# App init
app = FastAPI()

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Health endpoint (used by K8s probes)
@app.get("/health")
def health():
    return {"status": "ok"}

# Notification endpoint
@app.post("/notify")
async def notify(data: dict):
    logger.info(f"NOTIFICATION RECEIVED: {data}")
    return {"status": "notification received"}