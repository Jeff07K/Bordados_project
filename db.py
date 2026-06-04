from dotenv import load_dotenv
load_dotenv()

from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session