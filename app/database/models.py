from sqlalchemy import Column, Float, Integer, String
from .base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Float, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria = Column(String(100), nullable=False)
