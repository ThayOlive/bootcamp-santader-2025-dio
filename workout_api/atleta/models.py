from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from workout_api.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[int] = mapped_column(String(11), unique=True , nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    data_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped["CategoriaModel"] = relationship(back_populates="atleta")
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.pk_id"))   
    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(back_populates="atleta")
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centros_treinamento.pk_id"))


from workout_api.centro_treinamento.models import CentroTreinamentoModel 
