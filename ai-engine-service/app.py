from fastapi import FastAPI
import requests

app = FastAPI()

EXECUTION_URL = "http://execution-service:8000/execute"  # URL of the Execution service

@app.post("/analyze")
async def analyze(alert: dict):
    print("Analyzing alert:", alert)
          
    #simple rule-based analysis
    if "CrashLoopBackOff" in str(alert):
        action = {"action": "restart_pod", "pod": "demo-pod"}
    else:
        action = {"action": "none"}
    
    response = requests.post(EXECUTION_URL, json=action)

    return {"decision": action, "execution": response.json()}
