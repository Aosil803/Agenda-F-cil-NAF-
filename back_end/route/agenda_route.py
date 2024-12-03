from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from back_end.create_db import get_db
from back_end.dtos.agenda_dtos import AgendaBase, AgendaCriar, AgendaOcupadaResposta, AgendaResposta
from back_end.models.agenda_models import Agenda
from back_end.utils.error_handlers import handle_database_error

router = APIRouter()

# Função para retornar todos os agendamentos
@router.get("/agenda/", response_model=list[AgendaResposta])
async def get_agendamentos(db: Session = Depends(get_db)):
    agendamentos = db.query(Agenda).all()
    if not agendamentos:
        raise HTTPException(status_code=404, detail="Nenhum horário encontrado.")
    return agendamentos

# Função para retornar agendamento por id
@router.get("/agenda/{agenda_id}", response_model=AgendaResposta)
async def get_agenda(agenda_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    agenda = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not agenda:
        raise HTTPException(status_code=404, detail=f"Agendamento Id {agenda_id}")
    return agenda

# Função para criar uma data de agendamento
@router.post("/agenda/", response_model=AgendaResposta)
def criar_horario(agenda: AgendaCriar, db: Session = Depends(get_db)):
    try:
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
        raise e  # Levanta novamente o erro de validação

    except ValueError as e:
        # Tratar o erro de validação do DTO (por exemplo, hora inválida)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        handle_database_error(db, e)


# Função para deletar uma data de agendamento por id 
@router.delete("/agenda/{agenda_id}", status_code=200)
async def deletar_agendamento(agenda_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    
    if not agendamento:
        # Lançando a exceção que será tratada no error_handlers.py
        raise HTTPException(status_code=404, detail=f"Agendamento com ID {agenda_id} não encontrado")

    # Remove o usuário
    db.delete(agendamento)
    db.commit()
    
    # Retorna apenas uma mensagem de sucesso
    return {"message": f"Agendamento com ID {agenda_id} deletado com sucesso!"}  


@router.post("/agendamento/", response_model=AgendaOcupadaResposta)
def criar_agendamento(agenda: AgendaBase, db: Session = Depends(get_db)):
    try:
        data_verificada = agenda.converte_str_datetime()

        horario = db.query(Agenda).filter(
            Agenda.ano == agenda.ano,
            Agenda.mes == agenda.mes,
            Agenda.dia == agenda.dia,
            Agenda.hora == agenda.hora,
            Agenda.turno == agenda.turno
        ).first()

        if not horario:
            raise HTTPException(status_code=404, detail="Horário não encontrado para agendamento.")
        if horario.status == False:
            raise HTTPException(status_code=400, detail="Horário já ocupado.")

        horario.status = False
        usuario_agendado = db.query(Agenda).filter(Agenda.usuario_id == agenda.usuario_id, Agenda.status == False).first()
        if usuario_agendado:
            raise HTTPException(status_code=400, detail="Usuário já possui um horário agendado.")

        horario.usuario_id = agenda.usuario_id
        db.commit()
        db.refresh(horario)

        response_data = horario.__dict__.copy()
        response_data['data_criacao'] = horario.data_criacao.strftime('%d/%m/%Y')
        response = AgendaOcupadaResposta(**response_data)

        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_database_error(db, e)
