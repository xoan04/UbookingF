from sqlalchemy import  Column
from sqlalchemy.sql.sqltypes import Integer,Text,Boolean,String
from config.db import Base


class courses(Base):
    __tablename__ = 'Salones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_course = Column(Text)
    busy=Column(Boolean,default=False)
    horario=Column(String)
    edificio_id=Column(Integer)


    def __repr__(self):
        return f"Curso {self.id}"