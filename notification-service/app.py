from fastapi import FastAPI

app = FastAPI()

@app.post("/notify")
async def notify(data: dict):
    print("NOTIFICATION:", data)
    return {"status": "notification received"}

