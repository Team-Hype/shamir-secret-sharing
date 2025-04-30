from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shard.master.db.models import *
from shard.master.db.models.base import Base

_engine = None
_Session = None


def init_database():
    global _engine, _Session
    _engine = create_engine('sqlite:///master.db', echo=True)
    _Session = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)


def get_db():
    if _Session is None:
        raise RuntimeError("Database not initialized. Call init_database(name) first.")
    db = _Session()
    try:
        yield db
    finally:
        db.close()
