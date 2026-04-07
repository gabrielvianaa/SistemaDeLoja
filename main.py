from app.database.base import Base
from app.database.connection import engine, database_file
from app.services import produto_service
from app.services import admin_service
from app.database.models import Categoria
from app.database.connection import SessionLocal


def ensure_produtos_schema():
    import sqlite3

    conn = sqlite3.connect(str(database_file))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'")
    if cur.fetchone() is not None:
        cur.execute("PRAGMA table_info(produtos)")
        columns = cur.fetchall()
        for column in columns:
            if column[1] == 'id' and column[2].upper() != 'FLOAT':
                conn.close()
                Base.metadata.drop_all(engine)
                Base.metadata.create_all(engine)
                return
    conn.close()

ensure_produtos_schema()
# create_all uses checkfirst=True per table — only creates tables that are missing,
# so existing data (users, saved carts, etc.) is never lost on restart.
Base.metadata.create_all(engine)

session = SessionLocal()
try:
    categorias_data = [
        (1, "Processadores"),
        (2, "Placas de Vídeo"),
        (3, "Memórias RAM"),
        (4, "Air Coolers"),
        (5, "Water Coolers"),
        (6, "Armazenamento"),
        (7, "Fontes de Alimentação"),
        (8, "Gabinetes"),
    ]
    for cat_id, nome in categorias_data:
        existing = session.query(Categoria).filter_by(id=cat_id).first()
        if not existing:
            cat = Categoria(id=cat_id, nome=nome)
            session.add(cat)
    session.commit()
finally:
    session.close()

if not produto_service.listarProdutos():
    produto_service.criarProduto("Processadores", "i7 12700k", 1500.00, 10)
    produto_service.criarProduto("Placas de Vídeo", "RTX 4070", 2500.00, 5)
    produto_service.criarProduto("Memórias RAM", "16GB DDR4", 300.00, 20)
    produto_service.criarProduto("Air Coolers", "Air Cooler XYZ", 200.00, 15)
    produto_service.criarProduto("Water Coolers", "Water Cooler ABC", 400.00, 8)
    produto_service.criarProduto("Armazenamento", "SSD 1TB", 500.00, 12)
    produto_service.criarProduto("Fontes de Alimentação", "Fonte 650W", 350.00, 10)
    produto_service.criarProduto("Gabinetes", "Gabinete Gamer", 250.00, 7)

if not admin_service.listar_admins():
    admin_service.criar_admin("admin", "admin123", "admin@loja.com")

if __name__ == "__main__":
    import customtkinter as ctk
    from app.ui.app import LojaApp

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = LojaApp(root)
    root.mainloop()
