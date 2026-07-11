from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from . import routes
from .schemas import CreateTransaction
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)
@app.get("/app")
def frontend():
    return FileResponse("frontend/index.html")