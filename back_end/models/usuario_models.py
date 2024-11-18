from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from back_end.create_db import Base  # Certifique-se de importar o Base correto para herdar de Base

# Definição do modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)  # Alterado de Integer para String
    telefone = Column(String, nullable=True)
    perfil = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.utcnow)  # Alterado para DateTime e valor padrão

    # Relacionamento com Endereco
    endereco_relacionado = relationship("Endereco", back_populates="usuario", uselist=False)

# Definição do modelo Endereco
class Endereco(Base):
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True)
    cep = Column(String)
    rua = Column(String)
    numero = Column(Integer)
    bairro = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    estado = Column(String)

    # Chave estrangeira para o relacionamento com Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))  
    usuario = relationship('Usuario', back_populates='endereco_relacionado', single_parent=True)
