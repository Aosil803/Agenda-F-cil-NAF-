import logging
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Configuração do logging
logger = logging.getLogger(__name__)

# Função para tratar erro de horário não disponível
def horario_nao_disponivel():
    raise HTTPException(status_code=404, detail="Horário não disponível ou já reservado.")

# Novo handler para erro de banco de dados
def handle_database_error(db: Session, exception: Exception):
    db.rollback()  # Faz o rollback da transação em caso de erro
    logger.error(f"Erro ao processar a requisição: {str(exception)}")  # Log do erro
    raise HTTPException(
        status_code=500,
        detail=f"Erro ao processar a requisição: {str(exception)}"  # Detalhe do erro
    )

# Handler genérico para HTTPException (outros erros 400, 404, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro {exc.status_code}: {exc.detail}")
    
    # Customização para erro 404
    if exc.status_code == 404:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"Recurso solicitado não encontrado. Detalhes: {exc.detail}"}
        )

    # Para outros erros 500 ou 400, pode ser mais genérico
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Handler para erros de validação de requisição faltando campo
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extraímos os erros diretamente, sem a necessidade de um loop
    error_messages = [f"Campo '{err['loc'][-1]}' inválido ou inexistente: {err['msg']}" for err in exc.errors()]
    
    logger.error(f"Erro de validação: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages}
    )
