from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from requests import Session
from src.models.user_model import CreateUserRequest
from src.db.schemas import User
from src.db.databases import local_session
from src.utils.security import Hash
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwt_service import JWTService
auth_router = APIRouter()

hash = Hash()
jwt = JWTService()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]


def authenticate_user(user: str, password: str, db):
    user = db.query(User).filter(User.user == user).first()
    if not user or not hash.verify_password(password, user.password):
        return False

    return user


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_deps, req: CreateUserRequest):
    user_model = User(
        id_empresa=req.id_empresa,
        razon_social=req.razon_social,
        user=req.user,
        password=hash.get_password_hash(req.password)
    )
    db.add(user_model)
    db.commit()
    return JSONResponse(content={"message": "User created successfully"})


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(db: db_deps, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=401, detail="Could not validate user")

    token = jwt.create_access_token(user)

    return {"message": "User logged in successfully", "access_token": token}
