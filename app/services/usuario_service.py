import re
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app.database.connection import SessionLocal
from app.database.models import CarrinhoItem, Usuario


def validar_cpf(cpf: str) -> bool:

    digits = re.sub(r"\D", "", cpf)

    if len(digits) != 11:
        return False

    if len(set(digits)) == 1:
        return False

    return True


def formatar_cpf(cpf: str) -> str:
    """Returns CPF formatted as XXX.XXX.XXX-XX."""
    digits = re.sub(r"\D", "", cpf)
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"


def cadastrar_usuario(
    nome: str, sobrenome: str, email: str, cpf: str, senha: str
) -> Usuario:
    cpf_formatado = formatar_cpf(cpf)
    session = SessionLocal()
    try:
        password_hash = generate_password_hash(senha)
        usuario = Usuario(
            nome=nome,
            sobrenome=sobrenome,
            email=email.lower().strip(),
            cpf=cpf_formatado,
            password_hash=password_hash,
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        session.expunge(usuario)
        return usuario
    finally:
        session.close()


def autenticar_usuario(email: str, senha: str) -> Optional[Usuario]:
    session = SessionLocal()
    try:
        usuario = (
            session.query(Usuario).filter_by(email=email.lower().strip()).first()
        )
        if usuario and check_password_hash(usuario.password_hash, senha):
            session.expunge(usuario)
            return usuario
        return None
    finally:
        session.close()


def buscar_usuario_por_email(email: str) -> Optional[Usuario]:
    session = SessionLocal()
    try:
        u = session.query(Usuario).filter_by(email=email.lower().strip()).first()
        if u:
            session.expunge(u)
        return u
    finally:
        session.close()


def buscar_usuario_por_cpf(cpf: str) -> Optional[Usuario]:
    cpf_fmt = formatar_cpf(cpf)
    session = SessionLocal()
    try:
        u = session.query(Usuario).filter_by(cpf=cpf_fmt).first()
        if u:
            session.expunge(u)
        return u
    finally:
        session.close()




def salvar_carrinho(usuario_id: int, itens: list) -> None:

    session = SessionLocal()
    try:
        session.query(CarrinhoItem).filter_by(usuario_id=usuario_id).delete()
        for item in itens:
            ci = CarrinhoItem(
                usuario_id=usuario_id,
                produto_id=item["produto_id"],
                quantidade=item["quantidade"],
                preco=item["preco"],
                categoria=item.get("categoria", ""),
            )
            session.add(ci)
        session.commit()
    finally:
        session.close()


def carregar_carrinho(usuario_id: int) -> list:

    session = SessionLocal()
    try:
        rows = (
            session.query(CarrinhoItem).filter_by(usuario_id=usuario_id).all()
        )
        return [
            {
                "produto_id": row.produto_id,
                "categoria": row.categoria,
                "quantidade": row.quantidade,
                "preco": row.preco,
                "subtotal": row.preco * row.quantidade,
            }
            for row in rows
        ]
    finally:
        session.close()


def limpar_carrinho_db(usuario_id: int) -> None:
    session = SessionLocal()
    try:
        session.query(CarrinhoItem).filter_by(usuario_id=usuario_id).delete()
        session.commit()
    finally:
        session.close()
