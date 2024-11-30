from calendar import monthrange
import logging
from fastapi import HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status

# Configuração do logging
logger = logging.getLogger(__name__)

# Novo handler para erro de banco de dados
def handle_database_error(db: Session, exception: Exception):
    try:
        db.rollback()
        logger.error(f"Erro ao processar a requisição: {str(exception)}")
    except Exception as e:
        logger.error(f"Erro ao fazer rollback: {str(e)}")
    finally:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro {status.HTTP_500_INTERNAL_SERVER_ERROR} ao processar a requisição! {str(exception)}"
        )

# Handler genérico para HTTPException (qualquer erro 400, 404, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.detail}"}
    )

# Handler para capturar erros de validação
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Captura mensagens diretamente do erro
    error_messages = [
        f"Campo '{err['loc'][-1]}' {err['msg']}."
        for err in exc.errors()
    ]

    mensagem_formatada = " ".join(error_messages)  # Concatena mensagens

    logger.error(f"Erro de validação: {mensagem_formatada}")

    return JSONResponse(
        status_code=422,
        content={
            "message": f"Erro 422 ao processar a requisição! {mensagem_formatada}"
        }
    )

# Handler específico para erros de validação de dados personalizados
async def validation_exception_handler_data(request: Request, exc: ValidationError):
    errors = []
    
    for error in exc.errors():
        loc = error.get("loc")  # Exemplo: loc pode ter 'mes' ou 'dia'
        if loc:
            field = loc[0]
            message = error.get("msg")
            
            # Se a mensagem de erro contiver 'value_error', remova ou trate esse erro
            if 'value_error' in message.lower():
                # Exemplo: Se for erro de valor do 'dia', remova ou personaliza
                if field == 'dia':
                    message = "O dia não é válido para o mês e ano fornecidos. Dias válidos de 1 a 29."
            
            # Personalização da mensagem de erro para 'dia'
            if field == 'dia':
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. {message}"
                })
            elif field == 'mes':
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']." 
                })
            else:
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. {message}."
                })
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )
    
    # Aqui estamos retornando uma resposta personalizada
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )
