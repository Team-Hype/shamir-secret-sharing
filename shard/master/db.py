from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

secrets_to_slaves = Table(
    'SecretsToSlaves', Base.metadata,
    Column('secret_id', Integer, ForeignKey('Secrets.id'), nullable=False),
    Column('slave_id', Integer, ForeignKey('Slaves.id'), nullable=False)
)

class Slave(Base):
    __tablename__ = 'Slaves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String)

    secrets = relationship("Secret", secondary=secrets_to_slaves, back_populates="slaves")

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


engine = create_engine('sqlite:///master.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
