from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from back_end.create_db import get_db
from back_end.dtos.agenda_dtos import Agendamento, AgendamentoResposta
from back_end.models.agenda_models import Agenda
from back_end.utils.error_handlers import handle_database_error


router = APIRouter()

@router.post("/agenda/", response_model=AgendamentoResposta)
def criar_agendamento(agenda: Agendamento, db: Session = Depends(get_db)):
    try:
        # Converte o mês para o número correspondente usando o DTO
        data_verificada = agenda.converte_str_datetime()  # Usa a função do DTO para converter para datetime

        # Verifica se o horário já existe
        horario = db.query(Agenda).filter(
            Agenda.ano == agenda.ano,
            Agenda.mes == agenda.mes,
            Agenda.dia == agenda.dia,
            Agenda.turno == agenda.turno,
            Agenda.hora == agenda.hora
        ).first()

        if horario is not None:
            # Lança uma exceção genérica para ser tratada no handler
            raise HTTPException(status_code=400, detail="Horário já existe na base de dados.")

        # Cria novo horário
        novo_horario = Agenda(
            ano=agenda.ano,
            mes=agenda.mes,
            dia=agenda.dia,
            turno=agenda.turno,
            hora=agenda.hora,
            status=True,
        )
        db.add(novo_horario)
        db.commit()
        db.refresh(novo_horario)

        return novo_horario

    except HTTPException as e:
        # Em caso de erro de data ou de horário, retorna o erro adequado
        raise e  # Levanta novamente o erro de validação

    except Exception as e:
        # Qualquer outro erro é tratado pelo handler de banco de dados
        handle_database_error(db, e)

        
# @router.post("/agendamento/", response_model=AgendaOcupadaResposta)
# def criar_agendamento(agenda: UsuarioAgendamento, db: Session = Depends(get_db)):
#     #hora_formatada = validar_hora(agenda.hora)
    
#     # Verificar se o horário está disponível
#     horario = db.query(Agenda).filter(
#         Agenda.ano == agenda.ano,
#         Agenda.mes == agenda.mes,
#         Agenda.dia == agenda.dia,
#         Agenda.hora == agenda.hora,
#         Agenda.turno == agenda.turno
#     ).first()

#     if  horario.status == False:  # Verificar status diretamente
#         raise HTTPException(status_code=400, detail="Esse horário já está ocupado ou não existe.")
            

#     # Atualizar o status do horário para ocupado e associar o usuário ao horário
#     horario.status = False
#     if agenda.usuario_id:
#         horario.usuario_id = agenda.usuario_id
#     db.commit()
#     db.refresh(horario)

#     return horario