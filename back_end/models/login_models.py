from sqlalchemy import Column, Date, Integer, String, DateTime
from datetime import datetime, timedelta
from back_end.create_db import Base

class Login(Base):
    __tablename__ = "login"
    id_login = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    matricula = Column(String, unique=False, nullable=True)
    tipo_usuario = Column(String, nullable=False)
    data_criacao = Column(Date, default=datetime.utcnow)
    token_recuperacao = Column(String, nullable=True)
    expiracao_token_recuperacao = Column(DateTime, nullable=True)

