from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    id_empresa: int
    razon_social: str
    user: str
    password: str
