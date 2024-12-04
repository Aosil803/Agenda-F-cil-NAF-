import logging
from fastapi.exceptions import RequestValidationError
from sqlalchemy import values
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, status  
from fastapi.responses import JSONResponse
from pydantic import ValidationError


logger = logging.getLogger(__name__)



def handle_create_user_error(db: Session, exception: Exception):
    try:
        db.rollback()
        logger.error(f"Erro ao criar usuário: {str(exception)}")
    except Exception as e:
        logger.error(f"Erro ao fazer rollback: {str(e)}")
    finally:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(exception)}"
        )

# Handler para erro de banco de dados
def handle_database_error(db: Session, exception: Exception):
    try:
        db.rollback()
        logger.error(f"Erro ao processar a requisição: {str(exception)}")
    except Exception as e:
        logger.error(f"Erro ao fazer rollback: {str(e)}")
    finally:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a requisição! " + str(exception)
        )

# Handler genérico para HTTPException (qualquer erro 400, 404, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f" {exc.detail}"}
    )

async def validation_exception_handler(request: Request, exc: Exception):
    errors = []

    if isinstance(exc, RequestValidationError) or isinstance(exc, ValidationError):
        for error in exc.errors():
            loc = error.get("loc")  # Exemplo: loc pode ter 'mes' ou 'hora'
            if loc:
                field = loc[-1] if loc else "corpo da requisição"  # Campo onde ocorreu o erro
                message = error.get("msg").replace("Value error, ", "")  # Mensagem de erro, removendo "Value error,"

                # Captura do campo específico e mensagem com código de status
                if field == 'mes':
                    errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'].")
                elif field == 'perfil_usuario':
                    errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: ['Morador Local', 'Colaborador Unifeso', 'Aluno Unifeso', 'Incrito no MEI', 'Micro Prod. Rural'].")
                elif field == 'perfil_admin':
                    errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: ['Estudante', 'Professor', 'Colaborador'].")
                elif field == 'turno':
                    errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido. Deve ser 'manhã' ou 'tarde'.")
                elif field == 'hora':
                    turno = error.get('ctx', {}).get('turno', None)
                    hora = error.get('input', None)  # Obtém a hora do input

                    # Replicar a lógica do DTO
                    if turno == "manhã" and not ("09:00" <= hora < "12:00"):
                        errors.append(f"Erro ao processar a requisição! Hora '{hora}' inválida para o turno da manhã. Deve ser entre 9:00 e 11:59.")
                    elif turno == "tarde" and not ("12:00" <= hora <= "18:00"):
                        errors.append(f"Erro ao processar a requisição! Hora '{hora}' inválida para o turno da tarde. Deve ser entre 12:00 e 18:00.")
                    else:
                        errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido ou inexistente. {message}")
                else:
                    errors.append(f"Erro ao processar a requisição! Campo '{field}' inválido ou inexistente. {message}")

    # Combina todas as mensagens em uma única string
    mensagem_erro = " | ".join(errors)

    # Registra a mensagem de erro no log
    logger.error(f"Erro de validação detectado: {mensagem_erro}")

    # Retorna o JSON com a mensagem diretamente
    return JSONResponse(
        status_code=422,
        content={"message": mensagem_erro},
    )


