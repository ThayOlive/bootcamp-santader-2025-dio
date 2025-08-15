from datetime import datetime
from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, Body, HTTPException, status
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from fastapi_pagination import Page, paginate, add_pagination

router = APIRouter()

@router.post( 
        path="/",
        summary="Create Atleta",
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut,
        )
async def post( 
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail=f"A categoria '{categoria_nome}' não foi encontrada."
            )
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
    )).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A centro de treinamento '{centro_treinamento_nome}' não foi encontrado."
        )
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude= {'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
    return atleta_out

@router.get(
        path="/",
        summary="Get Atletas list",
        response_model=Page[AtletaListOut],
        status_code=status.HTTP_200_OK,
        )
async def query(db_session: DatabaseDependency, nome: Optional[str]=None, cpf: Optional[str]=None) -> Page[AtletaListOut]:
    query_stmt = select(AtletaModel)
    if nome:  # filtra pelo nome se enviado
        query_stmt = query_stmt.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:   # filtra pelo cpf se enviado
        query_stmt = query_stmt.filter(AtletaModel.cpf == cpf)

    atletas: list[AtletaModel] = (await db_session.execute(query_stmt)).scalars().all()
    atletas_out = [AtletaListOut(
        nome=a.nome,
        categoria=a.categoria.nome,
        centro_treinamento=a.centro_treinamento.nome
    ) for a in atletas]

    return paginate(atletas_out)
add_pagination(router)
@router.get(
        path="/atleta",
        summary="Get Atleta by CPF or Nome",
        response_model=AtletaListOut,
        status_code=status.HTTP_200_OK,
        )
async def get_atleta(db_session: DatabaseDependency, nome: Optional[str]=None, cpf: Optional[str]=None) -> AtletaListOut:
    if not nome and not cpf:
        raise HTTPException(status_code=400, detail="Informe nome ou cpf para consultar o atleta")
    if nome:  # consulta por nome
        atleta = (await db_session.execute(select(AtletaModel).filter(AtletaModel.nome.ilike(f"%{nome}%")))).scalars().first()
    elif cpf:  # consulta por CPF
        atleta = (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))).scalars().first()        
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta not found")

    return AtletaListOut(
        nome=atleta.nome,
        categoria=atleta.categoria.nome,
        centro_treinamento=atleta.centro_treinamento.nome
    )    

@router.patch(
        path="/",
        summary="Update Atleta by CPF or Nome",
        response_model=AtletaOut,
        status_code=status.HTTP_200_OK,
        )
async def patch(db_session: DatabaseDependency, nome: Optional[str] = None,
    cpf: Optional[str] = None, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:

    if not nome and not cpf:
        raise HTTPException(status_code=400, detail="Informe nome ou cpf para atualizar o atleta")
    if nome:
        atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter(AtletaModel.nome.ilike(f"%{nome}%")))).scalars().first()
    elif cpf:
        atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta not found")

    atleta_update = atleta_up.model_dump(exclude_unset=True) 
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(
        path="/",
        summary="Delete Atleta by ID",
        status_code=status.HTTP_204_NO_CONTENT,
        )
async def delete( db_session: DatabaseDependency, id: Optional[UUID4] = None, nome: Optional[str]=None, cpf: Optional[str]=None) -> None:
    if not id and not nome and not cpf:
        raise HTTPException(status_code=400, detail="Informe id, nome ou cpf para deletar o atleta")
    if id:
        atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
        if not atleta:
            raise HTTPException(status_code=404, detail="Atleta not found")
    elif nome:
        atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter(AtletaModel.nome.ilike(f"%{nome}%")))).scalars().first()
        if not atleta:
            raise HTTPException(status_code=404, detail="Atleta not found")
    elif cpf:
        atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))).scalars().first()
        if not atleta:
            raise HTTPException(status_code=404, detail="Atleta not found") 
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta not found")
    await db_session.delete(atleta)
    await db_session.commit()
    
    