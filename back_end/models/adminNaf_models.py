from datetime import datetime
from sqlalchemy import CHAR, Column, Date, ForeignKey, Integer, String
from back_end.create_db import Base
from sqlalchemy.orm import relationship

class AdminNaf(Base):
    __tablename__ = "adminNaf"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    polo = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    perfil_admin = Column(CHAR(25), nullable=False)
    data_criacao = Column(Date, default=datetime.utcnow)
    login_id = Column(Integer, ForeignKey('login.id_login'))  # Atualizar referência para login.id_login
    login = relationship("Login")  # Relacionamento com Credenciais
    agendas = relationship("Agenda", back_populates="administrador")  # Relacionamento com Agenda (1:N)

