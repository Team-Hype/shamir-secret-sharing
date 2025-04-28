from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Модель User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

