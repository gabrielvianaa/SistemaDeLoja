from sqlalchemy import Column, Float, Integer, String
from .base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Float, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria = Column(String(100), nullable=False)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
