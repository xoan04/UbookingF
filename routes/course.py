from fastapi import APIRouter, Response, status, Depends
from models.course import courses
from schemas.course import Course
from config.db import get_db
from sqlalchemy.orm import Session
from auth.auth_barrer import JWTBearer


# Creating a new router.
produc = APIRouter()


"""
        It takes a database session, queries the courses table, and returns all the rows in the table
        
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: A list of courses
"""
@produc.get("/courses",tags=["courses"])
def get_courses(db:Session=Depends(get_db)):
        return  db.query(courses).all()


        """
        It returns the course with the given id.
        
        :param id: int - The id of the course to retrieve
        :type id: int
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: The data is being returned if it is not None.
        """
@produc.get("/courses/{id}",tags=["courses"])
def get_course(id:int,db:Session=Depends(get_db)):
        data=db.query(courses).filter(courses.id==id).first()
        return (data,Response(status_code=status.HTTP_404_NOT_FOUND))[data is None]


        """
        It takes a code as a parameter, and returns the course with that code
        
        :param code: str - The code of the course to retrieve
        :type code: str
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: The first course with the code that is passed in the url
        """

@produc.get("/courses/{code}",tags=["courses"])
def get_course_byCode(code:str,db:Session=Depends(get_db)):
        data=db.query(courses).filter(courses.code==code).first()
        return db.query(courses).filter(courses.code==code).first()



        """
        It creates a new course in the database
        
        :param course: course is the input parameter
        :type course: course
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with the status code 201.
        """
@produc.post("/courses",tags=["courses"], status_code=status.HTTP_201_CREATED)
def create_course(course:Course,db:Session=Depends(get_db)):
        new_course = courses(name=course.name,code=course.code,busy=False,)
        try:
                if(not(db.query(courses).filter(courses.code==new_course.code).first() is None)):
                        raise Exception
                db.add(new_course)
                db.commit()
                db.refresh(new_course)
                return Response(status_code=status.HTTP_201_CREATED)
        except Exception as e:
                return Response(status_code=status.HTTP_400_BAD_REQUEST, content="code or name already exists")

        """
        It takes the id of the course to be updated, the new course object and the database session as
        parameters
        
        :param id: The id of the course to be updated
        :type id: int
        :param course: course - This is the model that we created earlier
        :type course: course
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with a status code of 200 OK.
        """
@produc.put("/courses/{id}",status_code=status.HTTP_200_OK,tags=["courses"])
def update_course(id:int,course:Course,db:Session=Depends(get_db)):
        
        if db.query(courses).filter(courses.id==id).first() is None:
                Response(status_code=status.HTTP_404_NOT_FOUND)

        new_course = db.query(courses).filter(courses.id==id).first()
        new_course.name = course.name
        new_course.code = course.code
        new_course.Quantity = course.Quantity
        new_course.price = course.price
        
        db.commit()
        return Response(status_code=status.HTTP_200_OK)

        """
        It deletes a course from the database, if the course exists
        
        :param id: int - The id of the course to delete
        :type id: int
        :param db: Session = Depends(get_db)
        :type db: Session
        :return: a response object with a status code of 204.
        """
@produc.delete("/courses/{id}",tags=["courses"], status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id:int,db:Session=Depends(get_db)):
        data=db.query(courses).filter(courses.id==id)
        
        if db.query(courses).filter(courses.id==id).first() is None:
                return Response(status_code=status.HTTP_404_NOT_FOUND)
        
        data.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)