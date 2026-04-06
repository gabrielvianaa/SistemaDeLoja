from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash

from app.database.connection import SessionLocal
from app.database.models import Admin as AdminModel


def criar_admin(username: str, password: str, email: Optional[str] = None) -> AdminModel:
    session = SessionLocal()
    try:
        password_hash = generate_password_hash(password)
        admin = AdminModel(username=username, password_hash=password_hash, email=email)
        session.add(admin)
        session.commit()
        session.refresh(admin)
        return admin
    finally:
        session.close()


def autenticar_admin(username: str, password: str) -> Optional[AdminModel]:
    session = SessionLocal()
    try:
        admin = session.query(AdminModel).filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            return admin
        return None
    finally:
        session.close()


def listar_admins() -> list[AdminModel]:
    session = SessionLocal()
    try:
        return session.query(AdminModel).all()
    finally:
        session.close()


def buscar_admin_por_username(username: str) -> Optional[AdminModel]:
    session = SessionLocal()
    try:
        return session.query(AdminModel).filter_by(username=username).first()
    finally:
        session.close()