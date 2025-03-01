from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, BigInteger, Column, Date, ForeignKey, Integer, String
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
    contentId = Column(String(100), nullable=False)
    messagingServiceSid = Column(String(100), nullable=False)


class Surveys(Base):
    __tablename__ = "encuestas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_empresa = Column(Integer, nullable=False)
    id_template = Column(Integer, ForeignKey('templates.id'), nullable=False)
    id_campania = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        default=datetime.now(timezone.utc))


class SurveyQuestions(Base):
    __tablename__ = "encuestas_respuestas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_encuesta = Column(Integer, ForeignKey('encuestas.id'), nullable=False)
    id_evento = Column(Integer, nullable=False)
    id_pregunta = Column(Integer, nullable=False)
    id_respuesta = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        default=datetime.now(timezone.utc))
