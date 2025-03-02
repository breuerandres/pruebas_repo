from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from src.utils.preguntas import preguntas
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
    '''
    template db.query(templates).(id)

    twilio_params = {
        "messagingServiceSid": template.messagingServiceSid
        "to": f'whatsapp:{body.telefono}', dspues no...
        "contentId": template.contentId,
        "variables": {"1":body.vehiculo}
    }




    TwilioClient().send_message(**twilio_params)
    '''
    twilio_params_1 = {

        "to": body.telefono,
        "content_sid": "HXcc7b0205fce2cf89d8373ba5adc6d3b2",
        "content_variables": '{"1": "Gustavo Veliz","2": "audi"}'
    }
    twilio_params_2 = {

        "to": body.telefono,
        "content_sid": "HX6e6403003036e8cdc717ca432d033783",
        "content_variables": '{"1": "audi"}'
    }
    TwilioClient().send_message(**twilio_params_1)
    TwilioClient().send_message(**twilio_params_2)

    return JSONResponse(content="Message sent successfully.")


@message_router.post("/rta", status_code=status.HTTP_200_OK)
async def response(req: Request):
    form_data = await req.form()

    print("Datos recibidos en el webhook:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    print("llegao algo")
    return "OK"
