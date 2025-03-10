from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.message_router import message_router
from src.routes.auth_router import auth_router
from src.utils.http_error_handler import HttpErrorHandler
import src.db.schemas as Schemas
from src.db.databases import engine


app = FastAPI()

app.title = "Encuestas Whastapp API"
app.version = "0.0.1"

Schemas.Base.metadata.create_all(bind=engine)


app.add_middleware(HttpErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(message_router, prefix="/survey", tags=["Survey"])


@app.get("/")
def healthcheck():
    return {"status": "ok"}
