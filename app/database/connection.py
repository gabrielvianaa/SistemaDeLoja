from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

base_dir = Path(__file__).resolve().parent
database_file = base_dir / "database.db"

engine = create_engine(
    f"sqlite:///{database_file}",
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
