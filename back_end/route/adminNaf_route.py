from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from back_end.models.adminNaf_models import AdminNaf
from back_end.create_db import get_db
from back_end.dtos.adminNaf_dtos import AdminNafCriar, AdminNafResposta
from back_end.utils.error_handlers import handle_create_user_error

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
    adminNaf = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()
    if not adminNaf:
        raise HTTPException(status_code=404, detail=f"Administrador NAF com ID {adminNaf_id} não encontrado.")
    return adminNaf

# Função para criar um novo administrador NAF
@router.post("/adminNaf/", response_model=AdminNafResposta)
async def criar_admin_naf(adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    try:
        # Verificar se a matrícula já existe
        matricula_existente = db.query(AdminNaf).filter(AdminNaf.matricula == adminNaf.matricula).first()
        if matricula_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Matrícula '{adminNaf.matricula}' já cadastrada em outro administrador.")
        
        # Criar novo administrador
        novo_admin = AdminNaf(
            nome=adminNaf.nome,
            matricula=adminNaf.matricula,
            email=adminNaf.email,
            senha=adminNaf.senha,
            perfil_admin=adminNaf.perfil_admin
        )

        # Adiciona administrador no banco de dados
        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)  # Atualiza o objeto com os dados salvos

        return novo_admin

    except HTTPException as e:
        raise e  # Relevanta a exceção HTTPException específica
    except Exception as e:
        handle_create_user_error(db, e)

        
# Função para atualizar um Administrador por id
@router.put("/adminNaf/{adminNaf_id}", response_model=AdminNafResposta)
def atualizar_adminNaf(adminNaf_id: int, adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    adminNaf_existente = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()

    if not adminNaf_existente:
        raise HTTPException(status_code=404, detail=f"Administrador NAF com ID {adminNaf_id} não encontrado.")

    # Atualiza os campos do administrador
    for field, value in adminNaf.dict(exclude_unset=True).items():
        setattr(adminNaf_existente, field, value)

    db.add(adminNaf_existente)
    db.commit()
    db.refresh(adminNaf_existente)

    return adminNaf_existente

# Função para deletar um Administrador por id
@router.delete("/adminNaf/{adminNaf_id}", status_code=200)
async def deletar_adminNaf(adminNaf_id: int, db: Session = Depends(get_db)):
    adminNaf = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()

    if not adminNaf:
        raise HTTPException(status_code=404, detail=f"Administrador NAF com ID {adminNaf_id} não encontrado.")

    db.delete(adminNaf)
    db.commit()

    return {"message": f"Administrador NAF com ID {adminNaf_id} deletado com sucesso!"}
