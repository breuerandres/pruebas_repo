from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(Integer, nullable=False)
    razon_social = Column(String(100), nullable=False)
    user = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Templates(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False)
    id_set_preguntas = Column(Integer, nullable=False)
    id_contenido = Column(String(100), nullable=False)
    id_servicio_mensajeria = Column(String(100), nullable=True)


class Surveys(Base):
    __tablename__ = "encuestas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    encuesta_iniciada = Column(Boolean, nullable=False, default=False)
    id_encuesta = Column(Integer, nullable=False)
    id_empresa = Column(Integer, nullable=False)
    id_campania = Column(Integer, nullable=False)
    id_grupo = Column(Integer, nullable=False)
    id_subgrupo = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        default=datetime.now(timezone.utc))


class SurveyQuestions(Base):
    __tablename__ = "encuestas_respuestas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_encuesta = Column(Integer, ForeignKey('encuestas.id'), nullable=False)
    id_template = Column(Integer, ForeignKey('templates.id'), nullable=False)
    id_evento = Column(Integer, nullable=False)
    id_pregunta = Column(Integer, nullable=False)
    id_respuesta = Column(Integer, nullable=False)
    id_mensaje = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        default=datetime.now(timezone.utc))
