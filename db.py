import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./bordados.db")

# Neon / Supabase usan "postgres://" pero SQLAlchemy necesita "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite necesita connect_args especial; PostgreSQL no
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def init_db():
    """Crea todas las tablas si no existen."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency de FastAPI para inyectar sesión."""
    with Session(engine) as session:
        yield session
