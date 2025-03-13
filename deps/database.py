from fastapi import Depends
import os
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

POSTGRES_URL = os.getenv("POSTGRES_URL")

# Create database connection
engine = create_engine(POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
