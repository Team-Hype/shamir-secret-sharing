from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table
)

from shard.master.db.models.base import Base

secrets_to_slaves = Table(
    'SecretsToSlaves', Base.metadata,
    Column('secret_id', Integer, ForeignKey('Secrets.id'), nullable=False),
    Column('slave_id', Integer, ForeignKey('Slaves.id'), nullable=False)
)
