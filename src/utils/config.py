from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_SENDER_NUMBER: str
    MY_PHONE_NUMBER: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"
