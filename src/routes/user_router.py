from fastapi import APIRouter
from fastapi.responses import JSONResponse

user_router = APIRouter()


@user_router.get("/")
def users():
    hello = {"rta": "Hello User"}
    return JSONResponse(content=hello)
