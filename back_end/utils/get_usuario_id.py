import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from back_end.create_db import get_db

SECRET_KEY = "sua_chave_secreta"

async def get_usuario_id(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Token de autenticação é necessário")
    
    try:
        token = token.split(" ")[1]  # Remove "Bearer" do token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get('usuario_id')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")



