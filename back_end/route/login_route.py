import jwt
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from back_end.create_db import get_db
from back_end.dtos.login_dtos import UsuarioLoginCriar, UsuarioLoginRespostaComToken, UsuarioLoginRespostaSemToken
from datetime import datetime, timedelta
from back_end.models.login_models import Login

SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"

router = APIRouter()

def criar_access_token(dados: dict, expires_delta: timedelta = None):
    to_encode = dados.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para retornar todos os logins
@router.get("/login/", response_model=list[UsuarioLoginRespostaSemToken])
async def get_login(db: Session = Depends(get_db)):
    logins = db.query(Login).all()
    if not logins:
        raise HTTPException(status_code=404, detail="Erro ao processar a requisição! Nenhum registro encontrado.")
    
    return logins

# Função para retornar um login pelo ID
@router.get("/login/{id_login}", response_model=UsuarioLoginRespostaSemToken)
async def get_login_by_id(id_login: int, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id_login == id_login).first()
    if not login:
        raise HTTPException(status_code=404, detail=f"Erro ao processar a requisição! Registro com ID {id_login} não encontrado.")
    return login

# Função para criar um novo login
@router.post("/login/", response_model=UsuarioLoginRespostaComToken)
async def criar_login(login: UsuarioLoginCriar, db: Session = Depends(get_db)):
    try:
        # Verifique se o email já existe
        email_existente = db.query(Login).filter(Login.email == login.email).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="Erro ao processar a requisição! Email já está em uso.")
        
        tipo_usuario = "adminNaf" if login.matricula else "usuario"
        data_criacao = datetime.utcnow()  

        novo_login = Login(
            usuario=login.usuario,
            email=login.email,
            senha=login.senha,
            tipo_usuario=tipo_usuario,
            data_criacao=data_criacao  
        )
        db.add(novo_login)
        db.commit()
        db.refresh(novo_login)

        access_token_expires = timedelta(minutes=30)
        access_token = criar_access_token(
            dados={"sub": novo_login.email, "usuario_id": novo_login.id_login, "tipo_usuario": novo_login.tipo_usuario},
            expires_delta=access_token_expires
        )

        resposta_sucesso = UsuarioLoginRespostaComToken(
            id_login=novo_login.id_login,
            usuario=novo_login.usuario,
            email=novo_login.email,
            senha="*******(Sem visualização)",
            access_token=access_token,
            token_type="bearer",
            data_criacao=novo_login.data_criacao.strftime('%d/%m/%Y')  
        )

        return resposta_sucesso
    except HTTPException as e:
        raise e
    finally:
        db.close()


# Função para atualizar um registro por id        
@router.put("/login/{id_login}", response_model=UsuarioLoginRespostaSemToken)
async def atualizar_login(id_login: int, login: UsuarioLoginCriar, db: Session = Depends(get_db)):
    login_existente = db.query(Login).filter(Login.id_login == id_login).first()

    if not login_existente:
        raise HTTPException(status_code=404, detail=f"Registro com ID {id_login} não encontrado.")

    # Atualiza os campos do login existente
    login_existente.usuario = login.usuario
    login_existente.email = login.email
    login_existente.senha = login.senha
    login_existente.matricula = login.matricula

    db.add(login_existente)
    db.commit()
    db.refresh(login_existente)

    return UsuarioLoginRespostaSemToken.from_orm(login_existente)

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
