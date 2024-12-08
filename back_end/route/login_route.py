from fastapi import APIRouter, HTTPException, Depends, logger
from sqlalchemy.orm import Session
from back_end.create_db import get_db
from back_end.dtos.login_dtos import UsuarioLoginCriar, UsuarioLoginRespostaComToken, UsuarioLoginRespostaSemToken
from datetime import datetime, timedelta
from back_end.models.login_models import Login
from back_end.dtos.login_dtos import criar_access_token


router = APIRouter()


# Função para retornar todos os registros login
@router.get("/login/", response_model=list[UsuarioLoginRespostaSemToken])
async def get_login(db: Session = Depends(get_db)):
    logins = db.query(Login).all()
    if not logins:
        raise HTTPException(status_code=404, detail="Erro ao processar a requisição! Nenhum registro encontrado.")
    
    return logins
from fastapi import HTTPException


#Função para reuperar senha de login 
@router.get("/recuperar-senha")
def recuperar_senha(token: str, db: Session = Depends(get_db)):
    # Buscar o usuário pelo token
    login = db.query(Login).filter(Login.token_recuperacao == token).first()

    if login:
        # Verificar se o token não expirou
        if login.expiracao_token_recuperacao > datetime.utcnow():
            return {"message": "Token válido. Você pode alterar sua senha agora."}
        else:
            raise HTTPException(status_code=400, detail="Token expirado.")
    else:
        raise HTTPException(status_code=404, detail="Token inválido.")

# Função para retornar um registro login pelo ID
@router.get("/login/{id_login}", response_model=UsuarioLoginRespostaSemToken)
async def get_login_by_id(id_login: int, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id_login == id_login).first()
    if not login:
        raise HTTPException(status_code=404, detail=f"Erro ao processar a requisição! Registro com ID {id_login} não encontrado.")
    return login


# Função para criar um novo registro login
@router.post("/login/", response_model=UsuarioLoginRespostaSemToken)
async def criar_login(login: UsuarioLoginCriar, db: Session = Depends(get_db)):
    try:
        # Verifique se o email já existe
        email_existente = db.query(Login).filter(Login.email == login.email).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="Erro ao processar a requisição! Email já está em uso.")
        if login.matricula:
            matricula_existente = db.query(Login).filter(
                Login.matricula == login.matricula,
                Login.tipo_usuario == "adminNaf"
            ).first()
            if matricula_existente:
                raise HTTPException(
                    status_code=400,
                    detail="Erro ao processar a requisição! Matrícula já está em uso por outro adminNaf."
                )

        tipo_usuario = "adminNaf" if login.matricula else "usuario"
        data_criacao = datetime.utcnow()

        novo_login = Login(
            usuario=login.usuario,
            email=login.email,
            senha=login.senha,
            tipo_usuario=tipo_usuario,
            matricula=login.matricula,
            data_criacao=data_criacao
        )
        db.add(novo_login)
        db.commit()
        db.refresh(novo_login)

        # access_token_expires = timedelta(minutes=30)
        # access_token = criar_access_token(
        #     dados={"sub": novo_login.email, "usuario_id": novo_login.id_login, "tipo_usuario": novo_login.tipo_usuario},
        #     expires_delta=access_token_expires
        # )
              
        resposta_sucesso = UsuarioLoginRespostaSemToken.from_orm(novo_login)
       
        return resposta_sucesso
    except HTTPException as e:
        raise e 
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")

#Função para recuperação de senha usando email
@router.put("/login/recuperar-senha", response_model=UsuarioLoginRespostaSemToken)
async def recuperar_senha(token: str, nova_senha: str, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.token_recuperacao == token).first()

    if not login:
        raise HTTPException(status_code=404, detail="Token inválido ou expirado.")

    if datetime.utcnow() > login.expiracao_token_recuperacao:
        raise HTTPException(status_code=400, detail="Token expirado.")

    login.senha = nova_senha
    login.token_recuperacao = None  # Limpar o token de recuperação após o uso
    login.expiracao_token_recuperacao = None  # Limpar a expiração do token
    db.commit()

    return UsuarioLoginRespostaSemToken.from_orm(login)


# Função para deletar um login por id_login
@router.delete("/login/{id_login}", status_code=200)
async def deletar_login(id_login: int, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id_login == id_login).first()
    
    if not login:
        raise HTTPException(status_code=404, detail=f"Erro ao processar a requisição! Registro com ID {id_login} não encontrado.")

    # Remove o login
    db.delete(login)
    db.commit()
    
    # Retorna uma mensagem de sucesso
    return {"message": f"Registro com ID {id_login} deletado com sucesso!"}
