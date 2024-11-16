from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from create_db import Base

class Funcionario(Base):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String, unique=True, nullable=False)  # Garantindo que matrícula seja obrigatória
    email = Column(String, unique=True, nullable=False)  # Email obrigatório
    senha = Column(String, nullable=False)  # Garantindo que a senha seja obrigatória

    # Relacionamento com horários disponíveis
    horarios_disponiveis = relationship('HorarioDisponivel', back_populates='funcionario')
    agendamentos = relationship("Agenda", back_populates="funcionario")