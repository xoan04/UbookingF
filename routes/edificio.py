from fastapi import APIRouter, Response, status, Depends
from models.edificio import edificios
from schemas.edificio import Edificio
from config.db import get_db
from sqlalchemy.orm import Session
from auth.auth_barrer import JWTBearer


# Creating a new router.
produc = APIRouter()


"""
        It takes a database session, queries the edificios table, and returns all the rows in the table
        
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: A list of edificios
"""
@produc.get("/edificios",tags=["edificios"])
def get_edificios(db:Session=Depends(get_db)):
        return  db.query(edificios).all()


        """
        It returns the edificio with the given id.
        
        :param id: int - The id of the edificio to retrieve
        :type id: int
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: The data is being returned if it is not None.
        """
@produc.get("/edificios/{id}",tags=["edificios"])
def get_edificio(id:int,db:Session=Depends(get_db)):
        data=db.query(edificios).filter(edificios.id==id).first()
        return (data,Response(status_code=status.HTTP_404_NOT_FOUND))[data is None]


        """
        It takes a code as a parameter, and returns the edificio with that code
        
        :param code: str - The code of the edificio to retrieve
        :type code: str
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: The first edificio with the code that is passed in the url
        """

@produc.get("/edificios/{code}",tags=["edificios"])
def get_edificio_byCode(code:str,db:Session=Depends(get_db)):
        data=db.query(edificios).filter(edificios.code==code).first()
        return db.query(edificios).filter(edificios.code==code).first()



        """
        It creates a new edificio in the database
        
        :param edificio: edificio is the input parameter
        :type edificio: edificio
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with the status code 201.
        """
@produc.post("/edificios",tags=["edificios"], status_code=status.HTTP_201_CREATED)
def create_edificio(edificio:Edificio,db:Session=Depends(get_db)):
        new_edificio = edificios(name=edificio.name,code=edificio.code)
        try:
                if(not(db.query(edificios).filter(edificios.code==new_edificio.code).first() is None)):
                        raise Exception
                db.add(new_edificio)
                db.commit()
                db.refresh(new_edificio)
                return Response(status_code=status.HTTP_201_CREATED)
        except Exception as e:
                return Response(status_code=status.HTTP_400_BAD_REQUEST, content="code or name already exists")

        """
        It takes the id of the edificio to be updated, the new edificio object and the database session as
        parameters
        
        :param id: The id of the edificio to be updated
        :type id: int
        :param edificio: edificio - This is the model that we created earlier
        :type edificio: edificio
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with a status code of 200 OK.
        """
@produc.put("/edificios/{id}",status_code=status.HTTP_200_OK,tags=["edificios"])
def update_edificio(id:int,edificio:Edificio,db:Session=Depends(get_db)):
        
        if db.query(edificios).filter(edificios.id==id).first() is None:
                Response(status_code=status.HTTP_404_NOT_FOUND)

        new_edificio = db.query(edificios).filter(edificios.id==id).first()
        new_edificio.name = edificio.name
        new_edificio.code = edificio.code
        
        db.commit()
        return Response(status_code=status.HTTP_200_OK)

        """
        It deletes a edificio from the database, if the edificio exists
        
        :param id: int - The id of the edificio to delete
        :type id: int
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with a status code of 204.
        """
@produc.delete("/edificios/{id}",tags=["edificios"], status_code=status.HTTP_204_NO_CONTENT)
def delete_edificio(id:int,db:Session=Depends(get_db)):
        data=db.query(edificios).filter(edificios.id==id)
        
        if db.query(edificios).filter(edificios.id==id).first() is None:
                return Response(status_code=status.HTTP_404_NOT_FOUND)
        
        data.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)