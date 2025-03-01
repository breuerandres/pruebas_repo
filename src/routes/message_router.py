from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from requests import Session
from src.utils.twilio_client import TwilioClient
from src.models.send_survey_model import SendSurvey
from src.auth.jwt_service import JWTService
from src.db.databases import local_session

message_router = APIRouter()

jwt = JWTService()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
auth_deps = Annotated[dict, Depends(jwt.verify_access_token)]


@message_router.post("/", status_code=status.HTTP_200_OK)
def send_survey(user: auth_deps, db: db_deps, body: SendSurvey):

    params = {
        "to": body.to_phone,
        "body": body.body if hasattr(body, "body") else None,
        "contentId": body.contentId if hasattr(body, "contentId") else None,

    }

    params = {k: v for k, v in params.items() if v is not None}

    # TwilioClient().send_message(**params)

    return JSONResponse(content="Message sent successfully.")
