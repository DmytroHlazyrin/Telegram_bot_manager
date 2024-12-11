from fastapi import FastAPI

from app.api.v1 import auth, users, requests

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])

app.include_router(users.router, tags=["Users"])

app.include_router(requests.router, tags=["Requests"])
