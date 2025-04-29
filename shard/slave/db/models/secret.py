from sqlalchemy import (
    Column,
    String
)

from shard.slave.db.models.base import Base


class Secret(Base):
    __tablename__ = 'Secrets'

    key = Column(String, primary_key=True, nullable=False)
    part = Column(String, nullable=False)
