from fastapi import FastAPI
from src.routers import summary_router

app = FastAPI()

app.include_router(summary_router.router)

