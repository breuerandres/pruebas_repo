from pydantic import BaseModel


class SendSurvey(BaseModel):
    telefono: str
    vehiculo: str | None = None
    id_evento: int | None = None
    id_campania: int | None = None
    id_empresa: int | None = None


class SurveyResponse(BaseModel):
    id_encuesta: int
    id_evento: int
    id_pregunta: int
    id_respuesta: int
    id_empresa: int | None = None
    id_campania: int | None = None
    id_usuario: int | None = None
    id_template: int | None = None
    telefono: str | None = None
    vehiculo: str | None = None
    created_at: str | None = None
