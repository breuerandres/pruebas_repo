from fastapi import FastAPI
from src.routes.user_router import user_router
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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(message_router, prefix="/survey", tags=["Survey"])
