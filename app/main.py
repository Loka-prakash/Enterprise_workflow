from fastapi import FastAPI

from app.database import Base, engine

from app.models.user import User
from app.models.task import Task

from app.routers import auth_router, task_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(task_router.router)

@app.get("/")
def home():

    return {
        "message": "API Running"
    }