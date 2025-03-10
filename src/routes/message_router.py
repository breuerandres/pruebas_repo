from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from src.db.schemas import Surveys
from requests import Session
from src.utils.twilio_client import TwilioClient
from src.models.send_survey_model import SendSurvey
from src.auth.jwt_service import JWTService
from src.db.databases import local_session
import json

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
def send_survey(user: auth_deps, db: db_deps, body: SendSurvey, response: Response):
    survey_model = Surveys(
        id_encuesta=int(body.id_encuesta),
        id_empresa=int(user["id_empresa"]),
        id_campania=int(body.id_campania)
    )

    db.add(survey_model)
    db.commit()

    cookie_dic = {
        "nombre": body.nombre,
        "vehiculo": body.vehiculo,
        "sucursal": body.sucursal

    }

    variables_param_1 = {"1": f"{body.nombre}", "2": f"{body.sucursal}"}
    variables_param_2 = {"1": f"{body.vehiculo}"}

    twilio_params_1 = {

        "to": f"whatsapp:{body.telefono}",
        "content_sid": "HXcc7b0205fce2cf89d8373ba5adc6d3b2",
        "content_variables": json.dumps(variables_param_1)
    }
    twilio_params_2 = {

        "to": f"whatsapp:{body.telefono}",
        "content_sid": "HX4f5d7038e7eddb005bacf74870863df2",
        "content_variables": json.dumps(variables_param_2)
    }

    TwilioClient().send_message(**twilio_params_1)
    TwilioClient().send_message(**twilio_params_2)

    response = JSONResponse(content="Message sent successfully.")

    response.set_cookie(key=f"{body.telefono}",
                        value=json.dumps(cookie_dic))

    return response


@message_router.post("/response", status_code=status.HTTP_200_OK)
async def response(req: Request):
    form_data = await req.form()

    print("Datos recibidos en el webhook:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    twilio_params = {
        "to": form_data['From'],
    }
    if "ListId" not in form_data.keys():

        print("No habia listid")
        twilio_params["content_sid"] = "HX36a645432d650430b76ac3d77b0daa27"
        print("ok con param")
        try:
            TwilioClient().send_message(**twilio_params)

        except Exception as e:
            print(e)

        return "OK con error de input"

    nro_pregunta, puntaje = form_data["ListId"].split("-")
    print(form_data['From'])

    if (nro_pregunta == "pregunta_1"):
        twilio_params["content_sid"] = "HX804140b99b23eeb9b26cdc5c27dc1d23"
        TwilioClient().send_message(**twilio_params)
        return "OK Pregunta 1"

    elif (nro_pregunta == "pregunta_2"):
        twilio_params["content_sid"] = "HX61f3f5adaf444d5672eb50b868a18756"
        TwilioClient().send_message(**twilio_params)
        return "OK Pregunta 2"

    elif (nro_pregunta == "pregunta_3"):
        twilio_params["content_sid"] = "HX7f7f50fd90601a03d0fb9ecc6cd7390c"
        twilio_params["content_variables"] = '{"1": "Gustavo"}'
        TwilioClient().send_message(**twilio_params)

        return "OK Pregunta 3"

    return "OK"
