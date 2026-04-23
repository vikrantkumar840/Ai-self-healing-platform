from fastapi import FastAPI
import httpx
import os
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from k8s_client import get_k8s_client

app = FastAPI()
logger = logging.getLogger(__name__)

Notification_URL = os.getenv(
    "NOTIFICATION_URL",
    "http://notification-service:8000/notify"
)

v1 = get_k8s_client()

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/execute")
async def execute(action: dict):
    logger.info(f"Execution action: {action}")

    result = "no action"

    if action.get("action") == "restart_pod":
        pod_name = action.get("pod")
        namespace = os.getenv("NAMESPACE", "ai-self-healing")
        

        try:
            logger.info(f"Restarting pod {pod_name} in namespace {namespace}")
            v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            result = f"Pod {pod_name} restarted"
        except Exception as e:
            result = str(e)

    # notify
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(Notification_URL, json={"result": result})
    except Exception as e:
        logger.error(f"Notification failed: {e}")

    return {"status": result}