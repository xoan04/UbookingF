from enum import unique
from sqlalchemy import  Column
from sqlalchemy.sql.sqltypes import Integer, String,Boolean,Text
from config.db import Base



class edificios(Base):
    __tablename__ = 'Edificios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    code = Column(String(8), unique=True)


    
    def __repr__(self):
        return f"Edificios {self.name}"