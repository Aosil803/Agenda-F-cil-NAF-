from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from back_end.models.usuario_models import Usuario, Endereco
from back_end.dtos.usuario_dtos import UsuarioCriar, UsuarioBase
from back_end.create_db import get_db
router = APIRouter()

# Função para criar um novo usuário
@router.post("/usuarios/", response_model=UsuarioBase)
async def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        # Criação do objeto Endereco
        endereco = Endereco(
            cep=usuario.endereco.cep,
            rua=usuario.endereco.rua,
            numero=usuario.endereco.numero,
            bairro=usuario.endereco.bairro,
            complemento=usuario.endereco.complemento,
            cidade=usuario.endereco.cidade,
            estado=usuario.endereco.estado,
        )
        
        # Criação do objeto Usuario
        novo_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            telefone=usuario.telefone,
            perfil=usuario.perfil,
            senha=usuario.senha,
            data_criacao=datetime.now(),  # Ajuste se for necessário
            endereco=endereco  # Associe o endereço ao usuário
        )

        # Adiciona o novo usuário ao banco de dados
        db.add(novo_usuario)
        db.commit()

        # Retorna o usuário com o endereço associado
        return novo_usuario
    
    except Exception as e:
        db.rollback()  # Caso haja erro, faz o rollback
        raise HTTPException(status_code=500, detail="Erro ao criar usuário.")  # Retorna o erro 500

