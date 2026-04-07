from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)

    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Float, primary_key=True)
    nome = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="produtos")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    itens_carrinho = relationship(
        "CarrinhoItem", back_populates="usuario", cascade="all, delete-orphan"
    )


class CarrinhoItem(Base):
    __tablename__ = "carrinho_itens"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    produto_id = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False, default="")

    usuario = relationship("Usuario", back_populates="itens_carrinho")
