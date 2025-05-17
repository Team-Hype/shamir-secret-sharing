import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shard.master.db.models import *
from shard.master.db.models.base import Base

_engine = None
_Session = None


def init_database(db_path, log_file):
    global _engine, _Session

    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(logging.INFO)

    # Create File Logger is not exists
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    _engine = create_engine(
        f'sqlite:///{db_path}',
        echo=False  # Output only to logger, True for stdout
    )
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
