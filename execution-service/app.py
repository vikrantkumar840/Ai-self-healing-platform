from fastapi import FastAPI
import subprocess
import requests

app = FastAPI()
Notification_URL = "http://notification-service:8000/notify"  # URL of the Notification service

@app.post("/execute")
async def execute(action: dict):
    print("Execution action:", action)

    result = "no action"

    if action["action"] == "restart_pod":
        pod_name = action.get("pod")
        try:
            subprocess.run(
                ["kubectl", "delete", "pod", pod_name],
                check=True
            )
            result = f"Pod {pod_name} restarted"
        except Exception as e:
            result = str(e)

    #notify 
    requests.post(NOTIFICATION_URL, json={"result": result })

    return {"status": result}

