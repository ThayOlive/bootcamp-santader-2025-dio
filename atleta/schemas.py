from typing import Annotated
from pydantic import BaseModel, PositiveFloat, Field

class atleta(BaseModel):
    nome: Annotated[str, Field(description="Nome do atleta", examples="Mary", max_length=50)]
    cpf: Annotated[str, Field(description="CPF", examples="12345678910", max_length=11)]
    idade: Annotated[int, Field(description="Idade", examples=26)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", examples=66.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", examples=1.61)]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples="F", max_length=1)]
