from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from src.db.schemas import Surveys, Templates, SurveyQuestions
from requests import Session
from src.utils.twilio_client import TwilioClient
from src.utils.config import Settings
from src.models.send_survey_model import SendSurvey
from src.utils.id_mapping import id_respuestas_map
from src.auth.jwt_service import JWTService
from src.utils.chaching import AsyncCache
from src.db.databases import local_session
from src.db.db_service import add_model, get_all_models_by_attribute, get_model_by_attribute
import json

message_router = APIRouter()

jwt = JWTService()

settings = Settings()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
auth_deps = Annotated[dict, Depends(jwt.verify_access_token)]

cache: AsyncCache = AsyncCache()


@message_router.post("/", status_code=status.HTTP_200_OK)
async def send_survey(user: auth_deps, db: db_deps, body: SendSurvey):
    survey_model = Surveys(
        id_encuesta=int(body.id_encuesta),
        id_empresa=int(user["id_empresa"]),
        id_campania=int(body.id_campania),
        id_grupo=int(body.id_grupo),
        id_subgrupo=int(body.id_subgrupo)
    )
    survey_model = add_model(db, survey_model)

    cookie = {
        "nombre": body.nombre,
        "vehiculo": body.vehiculo,
        "sucursal": body.sucursal,
        "id_evento": body.id_evento,
        "id_set_preguntas": body.id_set_preguntas,
        "id_survey": survey_model.id

    }

    await cache.set(f"{body.telefono}", cookie)

    # try:
    #     saludo_bienvenida = db.query(Templates)\
    #         .filter(Templates.id_set_preguntas == body.id_set_preguntas, Templates.descripcion == 'inicio_encuesta')\
    #         .first()

    # except:
    #     raise HTTPException(
    #         status_code=400, detail="No se encuentran los templates buscados")

    # Orden de Variables en Twilio: 1: Nombre, 2: Vehiculo, 3: Sucursal

    variables_param = {"1": f"{body.nombre}",
                       "2": f"{body.vehiculo}", "3": f"{body.sucursal}"}

    twilio_params = {

        "to": body.telefono,
        "msg_sid": 'MGcd9cd1e41032a3faa74640c02bd7ae4c',
        # "content_sid": f"{saludo_bienvenida.id_contenido}",
        "content_sid": "HX597a969cf5bcd2187a4c09f7656fcba6",
        "content_variables": json.dumps(variables_param)
    }

    TwilioClient().send_message(**twilio_params)

    # twilio_params["content_sid"] = f"{pregunta_1.id_contenido}"

    # TwilioClient().send_message(**twilio_params)

    return JSONResponse(content="Message sent successfully.")


@message_router.post("/status", status_code=status.HTTP_200_OK)
async def status_callback(req: Request):
    return await cache.get("+5491154746516")


@message_router.post("/response", status_code=status.HTTP_200_OK)
async def response(db: db_deps, req: Request):
    print("Datos recibidos en el webhook:")
    form_data = await req.form()
    # for key, value in form_data.items():
    #     print(f"{key}: {value}")

    # Traigo set de templates

    if form_data["From"] != f"whatsapp:{settings.TWILIO_SENDER_NUMBER}":
        # Traigo info de cookies del cache

        cookie = await cache.get(f"+{form_data['WaId']}")

        templates = get_all_models_by_attribute(
            db, Templates, Templates.id_set_preguntas, cookie['id_set_preguntas'])

        print("------Templates:------")
        print(templates[0].descripcion)
    '''
        if "ButtonPayload" in form_data.keys():
            # Envio pregunta 1

            variables_param = {
                "1": f"{cookie['nombre']}", "2": f"{cookie['vehiculo']}", "3": f"{cookie['sucursal']}"}

            twilio_params = {

                "to": f"+{form_data['WaId']}",
                "msg_sid": form_data['MessagingServiceSid'],
                # "content_sid": f"{saludo_bienvenida.id_contenido}",
                "content_sid": "HXcf95300b91bde467ad1626013600b310",  # Pregunta 1
                "content_variables": json.dumps(variables_param)
            }

            TwilioClient().send_message(**twilio_params)

        else:
            set_preguntas, nro_pregunta, puntaje = form_data["ListId"].split(
                "-")
            # Valido respuesta desde menu

            # Valido respuesta no respondida

            # Guardo respuesta de pregunta nro_pregunta
            respuesta_model = SurveyQuestions(
                id_encuesta=cookie['id_encuesta'],
                id_template=set_preguntas,
                id_evento=cookie['id_evento'],
                id_pregunta=nro_pregunta,
                id_respuesta=id_respuestas_map[puntaje],
                id_mensaje=form_data["MessageSid"]
            )

            respuesta_model = add_model(db, respuesta_model)
    '''
    # Si ultima pregunta -> msg despedida -> borrar cookies

    # SINO Envio pregunta i+1
    '''
    

    if "ButtonPayload" in form_data.keys():
        contador_encuesta = form_data["ButtonPayload"].split("-")[1]

    else:
        set, contador_encuesta, rta = form_data["ListId"].split("-")

    proxima_pregunta = f"encuesta_pregnunta{int(contador_encuesta) + 1}"

    

    '''

    return "OK"
