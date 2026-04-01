from typing import List, Optional

from app.database.connection import SessionLocal
from app.database.models import Produto as ProdutoModel


def criarProduto(id: float, nome: str, preco: float, estoque: int, categoria: str) -> ProdutoModel:
    session = SessionLocal()
    try:
        produto = ProdutoModel(id=id, nome=nome, preco=preco, estoque=estoque, categoria=categoria)
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()


def listarProdutos() -> List[ProdutoModel]:
    session = SessionLocal()
    try:
        return session.query(ProdutoModel).order_by(ProdutoModel.id).all()
    finally:
        session.close()


def buscar_produto_por_id(id: float) -> Optional[ProdutoModel]:
    session = SessionLocal()
    try:
        return session.query(ProdutoModel).filter_by(id=id).first()
    finally:
        session.close()


def atualizar_estoque(id: float, novo_estoque: int) -> Optional[ProdutoModel]:
    session = SessionLocal()
    try:
        produto = session.query(ProdutoModel).filter_by(id=id).first()
        if produto is None:
            return None
        produto.estoque = novo_estoque
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()


def deletar_produto(id: float) -> bool:
    session = SessionLocal()
    try:
        produto = session.query(ProdutoModel).filter_by(id=id).first()
        if produto is None:
            return False
        session.delete(produto)
        session.commit()
        return True
    finally:
        session.close()


def atualizar_preco(id: float, novo_preco: float) -> Optional[ProdutoModel]:
    session = SessionLocal()
    try:
        produto = session.query(ProdutoModel).filter_by(id=id).first()
        if produto is None:
            return None
        produto.preco = novo_preco
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()
