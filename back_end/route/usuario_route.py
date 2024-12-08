from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from back_end.models.usuario_models import Usuario
from back_end.dtos.usuario_dtos import UsuarioCriar, UsuarioResposta
from back_end.create_db import get_db
from back_end.utils.error_handlers import handle_create_user_error
 

router = APIRouter()

# Função para retornar todos os usuários
@router.get("/usuarios/", response_model=list[UsuarioResposta])
async def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    if not usuarios:
        raise HTTPException(status_code=404, detail="Erro ao processar a requisição! Nenhum usuário encontrado.")
    return [UsuarioResposta.from_orm(usuario) for usuario in usuarios]

# Função para retornar o usuário por id
@router.get("/usuarios/{usuario_id}", response_model=UsuarioResposta)
async def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuário Id {usuario_id} não encontrado.")
    return UsuarioResposta.from_orm(usuario)

# Função para criar um usuario
@router.post("/usuarios/", response_model=UsuarioResposta)
async def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        cpf_existente = db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()
        if cpf_existente:
            raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição! CPF N° '{usuario.cpf}' já cadastrado em outro usuário.")
                
        novo_usuario = Usuario(**usuario.dict())
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        resposta_sucesso = UsuarioResposta.from_orm(novo_usuario)
        return resposta_sucesso
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_create_user_error(db, e)

# Função para atualizar um usuario
@router.put("/usuarios/{usuario_id}", response_model=UsuarioResposta)
async def atualizar_usuario(usuario_id: int, usuario: UsuarioCriar, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for field, value in usuario.dict(exclude_unset=True).items():
        setattr(usuario_existente, field, value)

    db.add(usuario_existente)
    db.commit()
    db.refresh(usuario_existente)

    resposta_sucesso = UsuarioResposta.from_orm(usuario_existente)
    return resposta_sucesso

# Função para deletar um usuário por id   
@router.delete("/usuarios/{usuario_id}", status_code=200)
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Erro ao processar a requisição! Usuário com ID {usuario_id} não encontrado.")
    
    db.delete(usuario)
    db.commit()
    
    return {"message": f"Usuário com ID {usuario_id} deletado com sucesso!"}
