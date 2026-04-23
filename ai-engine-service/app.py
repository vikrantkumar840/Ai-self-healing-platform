from fastapi import FastAPI, Request
import time
import httpx
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-engine")

# ---------------------------
# Metrics
# ---------------------------
alerts_total = Counter("ai_alerts_total", "Total alerts received")

# ---------------------------
# Config
# ---------------------------
EXECUTION_URL = "http://execution:8000/execute"

ALLOWED_ALERTS = [
    "AIAlertsIncreasing",
    "KubePodNotReady"
]

COOLDOWN_SECONDS = 60
last_executed = {}

# ---------------------------
# Helpers
# ---------------------------
def should_execute(key: str):
    now = time.time()
    if key in last_executed:
        if now - last_executed[key] < COOLDOWN_SECONDS:
            return False
    last_executed[key] = now
    return True

async def call_execution(payload):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.post(EXECUTION_URL, json=payload)
            logger.info(f"Execution response: {res.status_code}")
    except Exception as e:
        logger.error(f"Execution call failed: {e}")

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def root():
    return {"message": "AI Engine is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/alert")
async def receive_alert(request: Request):
    data = await request.json()
    logger.info(f"Received alerts: {data.get('alerts', [])}")

    alerts = data.get("alerts", [])

    for alert in alerts:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        alertname = labels.get("alertname", "unknown")
        namespace = labels.get("namespace", "unknown")
        pod = labels.get("pod", "unknown")
        severity = labels.get("severity", "unknown")

        # ---------------------------
        # FILTERING (CRITICAL)
        # ---------------------------
        if alertname == "Watchdog":
            logger.info("Ignoring Watchdog")
            continue

        if alertname not in ALLOWED_ALERTS:
            logger.info(f"Ignoring alert: {alertname}")
            continue

        if namespace != "ai-self-healing":
            logger.info(f"Ignoring external namespace: {namespace}")
            continue

        # ---------------------------
        # COOLDOWN (ANTI-SPAM)
        # ---------------------------
        key = f"{alertname}:{pod}"

        if not should_execute(key):
            logger.info(f"Cooldown active for {key}, skipping")
            continue

        # ---------------------------
        # METRIC UPDATE
        # ---------------------------
        alerts_total.inc()

        # ---------------------------
        # DECISION LOGIC
        # ---------------------------
        action_payload = {
            "alert": alertname,
            "pod": pod,
            "namespace": namespace,
            "severity": severity,
            "summary": annotations.get("summary", "")
        }

        logger.info(f"Processing alert: {action_payload}")

        # ---------------------------
        # ACTION (EXECUTION SERVICE)
        # ---------------------------
        await call_execution(action_payload)

    return {"status": "processed"}