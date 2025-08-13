from typing import Annotated
from pydantic import PositiveFloat, Field
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Mary", max_length=50)]
    cpf: Annotated[str, Field(description="CPF", example="12345678910", max_length=11)]
    idade: Annotated[int, Field(description="Idade", example=26)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=66.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.61)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="F", max_length=1)]

class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass