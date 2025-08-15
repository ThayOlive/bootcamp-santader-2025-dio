from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate


router = APIRouter()

@router.post( 
        path="/",
        summary="Create new Centro Treinamento",
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,
        )
async def post( 
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn= Body(...)) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    try:
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()  

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um centro de treinamento com o nome '{centro_treinamento_in.nome}'"
        )
    return centro_treinamento_out

@router.get(
    path="/",
    summary="List all Centros de Treinamento",
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def list_centros(db_session: DatabaseDependency) -> Page[CentroTreinamentoOut]:
    centros = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    centros_out = [ CentroTreinamentoOut(id=c.id, nome=c.nome, endereco=c.endereco, proprietario=c.proprietario) for c in centros]
    return paginate(centros_out)


@router.get( 
        "/{id}",
        summary="List Centros de treinamento by ID",
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut,
        )
async def query(id:UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=404, detail="Centro de treinamento not found")

    return centro_treinamento


add_pagination(router)