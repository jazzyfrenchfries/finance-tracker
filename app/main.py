from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Finance Tracker is running!"}