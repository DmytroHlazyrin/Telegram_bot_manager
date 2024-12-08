from fastapi import FastAPI

from app.api.v1 import auth

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
