import logging
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime

# Configuração do logging
logger = logging.getLogger(__name__)

# Função de validação de hora
def validar_hora(hora: str) -> str:
    try:
        # Valida e converte a hora para time usando datetime
        hora_valida = datetime.strptime(hora, '%H:%M').time()
        return hora_valida.strftime('%H:%M')  # Retorna a hora como string formatada
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de hora inválido. Use HH:MM.")

# Função para tratar erro de horário não disponível
def horario_nao_disponivel():
    raise HTTPException(status_code=404, detail="Horário não disponível ou já reservado.")

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

# Handler para erros de validação de requisição
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extraímos os erros diretamente, sem a necessidade de um loop
    error_messages = [f"Campo '{err['loc'][-1]}' inválido ou inexistente: {err['msg']}" for err in exc.errors()]
    
    logger.error(f"Erro de validação: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages}
    )
