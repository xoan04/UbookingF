from enum import unique
from sqlalchemy import  Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import Base



class users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100))
        email = Column(String(150), unique=True)
        phone = Column(String(20))
        password = Column(String(255))
        address = Column(String(255))

        def __repr__(self):
                return f"User {self.name}"