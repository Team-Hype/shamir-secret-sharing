from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from shard.master.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)