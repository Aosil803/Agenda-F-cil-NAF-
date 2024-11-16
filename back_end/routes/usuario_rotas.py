# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from ..dtos.usuario import UsuarioCriar, Usuario
# from ..models.usuario import Usuario
# from ..create_db import obter_db

# router = APIRouter()

# @router.post("/usuarios/", response_model=Usuario)
# def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(obter_db)):
#     db_usuario = Usuario(nome=usuario.nome, email=usuario.email, telefone=usuario.telefone,
#                           endereco=usuario.endereco, senha=usuario.senha)  # Lembre-se de fazer o hash da senha
#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario
