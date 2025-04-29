from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import sessionmaker

from shard.master.db.models.base import Base

engine = create_engine('sqlite:///slave.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


