from models import Base
from sqlalchemy import create_engine
from constants import DATABASE_URL
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)