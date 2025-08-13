from typing import Annotated
from pydantic import UUID4, BaseModel, Field
from datetime import datetime 

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid' # Não riá aceitar campos extras
        from_attributes = True


class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description="ID do registro")]
    created_at: Annotated[datetime, Field(description="Data de criação do registro")]