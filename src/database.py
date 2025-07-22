import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

CURRENT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'data'))
DATABASE_URL = f"sqlite:///{DATA_DIR}/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_create():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

