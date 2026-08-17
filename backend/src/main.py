from fastapi import FastAPI
from src.routers import summary_router
from fastapi.middleware.cors import CORSMiddleware
from src.utils.env_variables import get_cors_origins

app = FastAPI()

CORS_ORIGINS = get_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary_router.router)

