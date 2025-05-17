import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shard.slave.db.models.base import Base
from shard.slave.db.models import *


_engine = None
_Session = None
log_file = "/var/log/shard/sqlalchemy.log"


def init_database(name: str):
    global _engine, _Session

    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(logging.INFO)

    # Create File Logger is not exists
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    _engine = create_engine(
        f'sqlite:///slave_{name}.db',
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