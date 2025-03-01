from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.utils.config import Settings
from jose import JWTError, jwt

settings = Settings()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


class JWTService:
    def __init__(self):
        self.secret = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.expiration = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, user_data) -> str:

        expires = datetime.now(timezone.utc) + \
            timedelta(minutes=self.expiration)
        encode = {"sub": f"id: {user_data.id}", "user": user_data.user,
                  "id_empresa": user_data.id_empresa,
                  "razon_social": user_data.razon_social
                  }
        encode.update({"exp": expires})
        return jwt.encode(encode, self.secret, algorithm=self.algorithm)

    def decode_access_token(self, token: str):
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def verify_access_token(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, self.secret,
                                 algorithms=[self.algorithm])

            if not payload.get("user") or not payload.get("sub"):
                raise HTTPException(
                    status_code=401, detail="Could not validate user")
            return payload

        except JWTError as e:
            print("Error al decodificar token:", str(e))
            raise HTTPException(
                status_code=401, detail="Bardo aca")
