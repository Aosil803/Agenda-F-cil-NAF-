from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from back_end.models.adminNaf_models import AdminNaf
from back_end.create_db import get_db
from back_end.dtos.adminNaf_dtos import AdminNafCriar, AdminNafResposta

router = APIRouter()

# Função para retornar todos os administradores Naf
@router.get("/adminNaf/", response_model=list[AdminNafResposta])
async def get_adminNaf(db: Session = Depends(get_db)):
   adminNaf = db.query(AdminNaf).all()
   if not adminNaf:
        raise HTTPException(status_code=404, detail="Nenhum Administrador NAF encontrado.")
   return adminNaf

@router.get("/adminNaf/{adminNaf_id}", response_model=AdminNafResposta)
async def get_adminNaf(adminNaf_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    adminNaf = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()
    if not adminNaf:
        raise HTTPException(status_code=404, detail=f"Usuário Id {adminNaf_id}")
    return adminNaf
    
# Função para criar um novo administrador NAF
@router.post("/adminNaf/", response_model=AdminNafResposta)
async def criar_admiNaf(adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    try:
        # Verificar se a matrícula já existe
        matricula_existente = db.query(AdminNaf).filter(AdminNaf.matricula == adminNaf.matricula).first()
        if matricula_existente:
             raise HTTPException(status_code=400, detail="Matricula já cadastrado em outro usuario")

        # Criar novo administrador
        novo_admin = AdminNaf(
            nome=adminNaf.nome,
            matricula=adminNaf.matricula,
            email=adminNaf.email,
            senha=adminNaf.senha,
            perfil=adminNaf.perfil,
        )

        # Adiciona administrador no banco de dados
        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)  # Atualiza o objeto com os dados salvos

       # Retorna a resposta com o DTO de saída (AdminNafResposta)
        return novo_admin 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)} ao criar Administrador!")


# Função para atualizar um Administrador por id  
@router.put("/adminNaf/{adminNaf_id}", response_model=AdminNafResposta)
def atualizar_adminNaf(adminNaf_id: int, adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    # Busca o usuário pelo ID
    adminNaf_existente = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()

    if not adminNaf_existente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza os campos do usuário
    for field, value in adminNaf.dict(exclude_unset=True).items():
        setattr(adminNaf_existente, field, value)

    db.add(adminNaf_existente)
    db.commit()
    db.refresh(adminNaf_existente)

    return adminNaf_existente  # Retorna o usuário atualizado

# Função para deletar um Administrador por id 
@router.delete("/adminNaf/{adminNaf_id}", status_code=200)
async def deletar_adminNaf(adminNaf_id: int, db: Session = Depends(get_db)):
    adminNaf = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()
    
    if not adminNaf:
        # Lançando a exceção que será tratada no error_handlers.py
        raise HTTPException(status_code=404, detail=f"Usuário com ID {adminNaf_id} não encontrado")

    # Remove o usuário
    db.delete(adminNaf)
    db.commit()
    
    # Retorna apenas uma mensagem de sucesso
    return {"message": f"Usuário com ID {adminNaf_id} deletado com sucesso!"}