# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from create_db import Base

# class HorarioDisponivel(Base):
#     __tablename__ = 'horarios_disponiveis'

#     id = Column(Integer, primary_key=True)
#     ano = Column(Integer, nullable=False)  # Ano do horário disponível
#     mes = Column(Integer, nullable=False)  # Mês do horário disponível
#     dia = Column(Integer, nullable=False)  # Dia do horário disponível
#     turno = Column(String, nullable=False)  # Manhã, Tarde
#     hora = Column(Integer, nullable=False)  # Hora disponível (válido para o turno selecionado)

#     # Relacionamento com Funcionario
#     funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=False)
    
#     # Relacionamento com Funcionario
#     funcionario = relationship('Funcionario', back_populates='horarios_disponiveis')
