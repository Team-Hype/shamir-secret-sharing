from sqlalchemy import (
    create_engine,
    Column,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Secret(Base):
    __tablename__ = 'Secrets'

    key = Column(String, primary_key=True, nullable=False)
    part = Column(String, nullable=False)


engine = create_engine('sqlite:///slave.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
