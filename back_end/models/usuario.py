from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from create_db import Base  # Aqui apenas a importação de Base para herdar de Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    cpf = Column(Integer, unique=True)
    telefone = Column(Integer)
    endereco = Column(String)  # Caso você queira manter como simples string
    perfil = Column(String)
    senha = Column(String)  # Será necessário um hash da senha
    data_criacao = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com Endereco
    endereco_relacionado = relationship('Endereco', back_populates='usuario', uselist=False)

class Endereco(Base):
    __tablename__ = "enderecos"  # Nome plural em minúsculo

    id = Column(Integer, primary_key=True)
    cep = Column(String)  # Alterando para String para lidar com CEPs com zeros à esquerda
    rua = Column(String)
    numero = Column(Integer)
    bairro = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    estado = Column(String)

    # Chave estrangeira referenciando o usuário
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    # Relacionamento com Usuario
    usuario = relationship('Usuario', back_populates='endereco_relacionado')
    agendamentos = relationship("Agenda", back_populates="usuario")

    

    
