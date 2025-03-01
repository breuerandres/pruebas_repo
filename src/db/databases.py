from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.config import Settings

settings = Settings()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

local_session = sessionmaker(
    autoflush=False, autocommit=False, bind=engine)

# class Database:
#     def __init__(self):
#         self.engine = create_engine(
#             settings.SQLALCHEMY_DATABASE_URL, echo=True)
#         self.local_session = sessionmaker(
#             autoflush=False, autocommit=False, bind=self.engine)

#     def get_session(self):
#         return self.local_session()

#     def get_engine(self):
#         return self.engine
