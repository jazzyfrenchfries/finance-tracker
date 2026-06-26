from fastapi import FastAPI
from .database import engine
from . import models
from . import routes
from .schemas import CreateTransaction
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(routes.router)
@app.get("/")
def home():
    return {"message": "Finance Tracker is running!"}
@app.post("/transaction")
def teat_transaction(transaction: CreateTransaction):
    return crud.create_transaction(Ses)