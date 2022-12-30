import os
from pathlib import Path
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app import crud, database, schemas
from app.database import SessionLocal, engine
from app.database.base_class import Base as DB_Base
from app.api.routes import api_router
from app.core.config import settings

DB_Base.metadata.create_all(bind=engine)


BASE_PATH = Path(__file__).resolve().parent

app = FastAPI(
    title="Blog API", openapi_url="/openapi.json"
)


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="client/dist/static"), name="static")
templates = Jinja2Templates(directory="client/dist")


root_router = APIRouter()


origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@root_router.get("/", tags=['root'], status_code=200)
async def root(request: Request):
    """
    Health check endpoint
    """
    return templates.TemplateResponse("index.html", {"request": request})


@root_router.get("/ping", status_code=200)
async def root(request: Request) -> dict:
    """
    Health check endpoint
    """
    return {
        "message": "OK",
        "timestamp": str(datetime.now().isoformat()),
    }


app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_STR)
