from pydantic import BaseModel


class CrearEncuesta(BaseModel):
    id_encuesta: int
    id_usuario: int
    id_empresa: int
    id_template: int
    id_campania: int


class CrearRespuesta(BaseModel):
    id_encuesta: int
    id_evento: int
    id_pregunta: int
    id_respuesta: int
    id_mensaje: int
