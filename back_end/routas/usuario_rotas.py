import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from back_end.models.usuario_models import Usuario
from back_end.dtos.usuario_dtos import UsuarioCriar, UsuarioBase
from back_end.create_db import get_db

# Configurar logs para exibir erros 
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


router = APIRouter()

# Função para retornar todos os usuários
@router.get("/usuarios/", response_model=list[UsuarioBase])
async def get_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()  
        if not usuarios:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")

# Função para retornar um usuário específico por ID
@router.get("/usuarios/{usuario_id}", response_model=UsuarioBase)
async def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuário Id {usuario_id}")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro {str(e)} não existe no Banco de Dados.")
    
# Função para criar um novo usuario
@router.post("/usuarios/", response_model=UsuarioBase)
async def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        # Criação do usuário com os campos de endereço diretamente
        novo_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            telefone=usuario.telefone,
            perfil=usuario.perfil,
            senha=usuario.senha,
            data_criacao=datetime.now(),
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            bairro=usuario.bairro,
            complemento=usuario.complemento,
            cidade=usuario.cidade,
            estado=usuario.estado,
        )

        # Adiciona o usuário ao banco
        db.add(novo_usuario)
        db.commit()

        logger.info(f"Novo usuário criado com sucesso id: {novo_usuario.id}")
        return novo_usuario

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar usuário: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro {str(e)} ao criar usuário!")


# Função para atualizar um usuario por ID
@router.put("/usuarios/{usuario_id}", response_model=UsuarioCriar)
def atualizar_usuario(usuario_id: int, usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        # Verificar se o usuário existe
        usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario_existente:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
                
        usuario_existente.nome = usuario.nome
        usuario_existente.perfil = usuario.perfil
        usuario_existente.email = usuario.email
        usuario_existente.cpf = usuario.cpf
        usuario_existente.senha = usuario.senha
        usuario_existente.cep = usuario.cep
        usuario_existente.rua = usuario.rua
        usuario_existente.numero = usuario.numero
        usuario_existente.bairro = usuario.bairro
        usuario_existente.complemento = usuario.complemento
        usuario_existente.cidade = usuario.cidade
        usuario_existente.estado = usuario.estado
        usuario_existente.telefone = usuario.telefone
        
        # Salvar no banco de dados
        db.commit()
        db.refresh(usuario_existente)
        
        return usuario_existente
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário: " + str(e))
    
    from fastapi import HTTPException

# Função para deletar um usuario por ID
@router.delete("/usuarios/{usuario_id}", status_code=200)
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Busca o usuário pelo ID
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Remove o usuário
    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso!"}

   
