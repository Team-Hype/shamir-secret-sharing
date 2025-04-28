from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from shard.master.db.models.base import Base
from shard.master.db.models.secret2slave import secrets_to_slaves


class Slave(Base):
    __tablename__ = 'Slaves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String)

    secrets = relationship("Secret", secondary=secrets_to_slaves, back_populates="slaves")
