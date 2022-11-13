from fastapi import APIRouter, Response, status,  Depends
from models.user import users
from schemas.user import User
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from passlib.context import CryptContext
from config.db import get_db
from sqlalchemy.orm import Session
from auth.auth_barrer import JWTBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

user = APIRouter()

@user.get("/users",tags=["users"])
def get_users(db:Session=Depends(get_db)):
        return  db.query(users).all()
    
@user.get("/users/{id}",tags=["users"])
def get_user(id:int,db:Session=Depends(get_db)):
        data=db.query(users).filter(users.id==id).first()
        return (data,Response(status_code=status.HTTP_404_NOT_FOUND))[data is None]
    
@user.post("/users",tags=["users"], status_code=HTTP_201_CREATED)
def post_user(user:User,db:Session=Depends(get_db)):
        new_user = users(name=user.name,email=user.email,password=get_password_hash(user.password),phone=user.phone, address=user.address)
        try:
            if(not(db.query(users).filter(users.email==user.email).first() is None)):
                raise Exception
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return Response(status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="email or phone already exists")
            raise
    
@user.put("/users/{id}",tags=["users"],status_code=HTTP_200_OK)
def update_user(id:int,user:User,db:Session=Depends(get_db)):
        if db.query(users).filter(users.id==id).first() is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        
        new_user = db.query(users).filter(users.id==id).first()
        new_user.name = user.name
        new_user.email = user.email
        new_user.password = get_password_hash(user.password)
        new_user.phone = user.phone
        db.commit()
        return Response(status_code=status.HTTP_200_OK)

@user.delete("/users/{id}",tags=["users"], status_code=HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session=Depends(get_db)):
        data=db.query(users).filter(users.id==id)
        if db.query(users).filter(users.id==id).first() is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        data.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)