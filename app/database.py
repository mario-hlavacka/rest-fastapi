import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session


DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]