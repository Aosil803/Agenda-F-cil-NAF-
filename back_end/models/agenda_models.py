from datetime import datetime
from sqlalchemy import Column, Date, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(String, nullable=False)
    dia = Column(Integer, nullable=False)
    turno = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True) 
    data_criacao = Column(Date, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    administrador_id = Column(Integer, ForeignKey("adminNaf.id"), nullable=True)

    # Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="agendas")

    # Relacionamento com Administrador
    administrador = relationship("AdminNaf", back_populates="agendas")
