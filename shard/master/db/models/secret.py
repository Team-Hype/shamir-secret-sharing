from sqlalchemy import (
    Column,
    Integer,
    String,
    CheckConstraint
)
from sqlalchemy.orm import relationship

from shard.master.db.models import Base


class Secret(Base):
    __tablename__ = 'Secrets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    required_parts = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('required_parts > 1'),
    )

    slaves = relationship("Slave", secondary=secrets_to_slaves, back_populates="secrets")
