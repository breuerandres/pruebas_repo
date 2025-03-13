from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.responses import JSONResponse
from src.db.schemas import Surveys, Templates
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

cache: dict[str, str] = {}


@message_router.post("/", status_code=status.HTTP_200_OK)
def send_survey(user: auth_deps, db: db_deps, body: SendSurvey):
    survey_model = Surveys(
        id_encuesta=int(body.id_encuesta),
        id_empresa=int(user["id_empresa"]),
        id_campania=int(body.id_campania),
        id_grupo=int(body.id_grupo),
        id_subgrupo=int(body.id_subgrupo)
    )
    try:
        db.add(survey_model)
        db.commit()
    except:
        raise HTTPException(
            status_code=400, detail="No se pudo almacenar la encuesta en la base de datos")

    cookie_dic = {
        "nombre": body.nombre,
        "vehiculo": body.vehiculo,
        "sucursal": body.sucursal,
        "id_evento": body.id_evento

    }

    cache[f"{body.telefono}"] = json.dumps(cookie_dic)

    try:
        saludo_bienvenida = db.query(Templates)\
            .filter(Templates.id_set_preguntas == body.id_set_preguntas, Templates.descripcion == 'saludo_bienvenida')\
            .first()

        pregunta_1 = db.query(Templates)\
            .filter(Templates.id_set_preguntas == body.id_set_preguntas, Templates.descripcion == 'encuesta_pregunta_1')\
            .first()
    except:
        raise HTTPException(
            status_code=400, detail="No se encuentran los templates buscados")

    # Orden de Variables en Twilio: 1: Nombre, 2: Vehiculo, 3: Sucursal

    variables_param = {"1": f"{body.nombre}",
                       "2": f"{body.vehiculo}", "3": f"{body.sucursal}"}

    twilio_params = {

        "to": body.telefono,
        "msg_sid": saludo_bienvenida.id_servicio_mensajeria,
        "content_sid": f"{saludo_bienvenida.id_contenido}",
        "content_variables": json.dumps(variables_param)
    }

    TwilioClient().send_message(**twilio_params)

    twilio_params["content_sid"] = f"{pregunta_1.id_contenido}"

    TwilioClient().send_message(**twilio_params)

    return JSONResponse(content="Message sent successfully.")


@message_router.post("/response", status_code=status.HTTP_200_OK)
async def response(db: db_deps, req: Request):
    # Extraigo data del cuerpo del request

    form_data = await req.form()

    # Traigo info de cookies del cache

    # Traigo set de preguntas

    # Valido respuesta desde menu

    # Guardo rta de pregunta i

    # Si ultima pregunta -> msg despedida -> borrar cookies

    # SINO Envio pregunta i+1
    '''
    print("Datos recibidos en el webhook:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    twilio_params = {
        "to": form_data['From'],
    }
    if "ListId" not in form_data.keys():

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
    '''
    return "OK"
