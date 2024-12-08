from fastapi import FastAPI

from app.api.v1 import auth, users

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])

app.include_router(users.router, tags=["Users"])
