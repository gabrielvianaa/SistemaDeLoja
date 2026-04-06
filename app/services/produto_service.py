from typing import List, Optional, Dict
from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import Produto, Categoria


def criarProduto(categoria_nome: str, nome: str, preco: float, estoque: int):
    session = SessionLocal()
    try:
        categoria = session.query(Categoria).filter_by(nome=categoria_nome).first()
        if not categoria:
            raise ValueError("Categoria não encontrada")
        
        max_id = session.query(func.max(Produto.id)).filter(Produto.categoria_id == categoria.id).scalar()
        if max_id is None:
            new_id = float(categoria.id) + 0.1
        else:
            new_id = max_id + 0.1
        
        produto = Produto(id=new_id, nome=nome, preco=preco, estoque=estoque, categoria_id=categoria.id)
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()


def listarProdutos() -> List[Dict]:
    session = SessionLocal()
    try:
        produtos = session.query(Produto).join(Categoria).order_by(Produto.id).all()
        result = []
        for p in produtos:
            result.append({
                'id': p.id,
                'nome': p.nome,
                'preco': p.preco,
                'estoque': p.estoque,
                'categoria': p.categoria.nome
            })
        return result
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []
    finally:
        session.close()


def buscar_produto_por_id(id: float) -> Optional[Dict]:
    session = SessionLocal()
    try:
        p = session.query(Produto).join(Categoria).filter(Produto.id == id).first()
        if p:
            return {
                'id': p.id,
                'nome': p.nome,
                'preco': p.preco,
                'estoque': p.estoque,
                'categoria': p.categoria.nome
            }
        return None
    finally:
        session.close()


def atualizar_estoque(id: float, novo_estoque: int):
    session = SessionLocal()
    try:
        produto = session.query(Produto).filter_by(id=id).first()
        if produto is None:
            return None
        produto.estoque = novo_estoque
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()


def atualizar_preco(id: float, novo_preco: float):
    session = SessionLocal()
    try:
        produto = session.query(Produto).filter_by(id=id).first()
        if produto is None:
            return None
        produto.preco = novo_preco
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()


def deletar_produto(id: float) -> bool:
    session = SessionLocal()
    try:
        produto = session.query(Produto).filter_by(id=id).first()
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
