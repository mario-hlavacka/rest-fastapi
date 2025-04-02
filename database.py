from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session


# DATABASE_URL = os.environ.get("DATABASE_URL") # TODO: extract to env
DATABASE_URL = 'postgresql://postgres:mysecretpassword@localhost:5432/fastapi'
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]