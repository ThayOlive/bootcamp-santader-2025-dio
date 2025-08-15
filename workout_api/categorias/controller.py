from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.models import CategoriaModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate


router = APIRouter()

@router.post( 
        path="/",
        summary="Create new Categoria",
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut,
        )
async def post( 
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)

    try:
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback() # limpa a sessão após erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe uma categoria com o nome '{categoria_in.nome}'"
        )
    
    return categoria_out

@router.get(
    path="/",
    summary="List all Categorias",
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def list_categorias(db_session: DatabaseDependency) -> Page[CategoriaOut]:
    categorias = (await db_session.execute(select(CategoriaModel))).scalars().all()
    categorias_out = [CategoriaOut(id=c.id, nome=c.nome) for c in categorias] 
    return paginate(categorias_out)

@router.get( 
        "/{id}",
        summary="List Categorias by ID",
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut,
        )
async def query(id:UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")

    return categoria



add_pagination(router)