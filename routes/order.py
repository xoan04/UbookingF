from fastapi import APIRouter, Response, status, Depends
from models.order import orders
from models.edificio import edificios
from models.course import courses
from schemas.order import Order
from config.db import get_db
from sqlalchemy.orm import Session
from auth.auth_barrer import JWTBearer
from routes.edificio import delete_edificio

# It creates a new router.
ordersRouter = APIRouter()


"""
    It takes a database session (db) as an argument, and returns all the orders in the database
    
    :param db: This is the database session that we'll use to query the database
    :type db: Session
    :return: All the orders in the database
"""
@ordersRouter.get("/orders",tags=["orders"])
def get_orders(db:Session=Depends(get_db)):
        return  db.query(orders).all()
    

"""
    It returns the orders of a client if the client exists, otherwise it returns a 404 error
    
    :param id_client: The id of the client whose orders we want to get
    :type id_client: int
    :param db: Session = Depends(get_db)
    :type db: Session
    :return: the data if it is not None, otherwise it returns a response with status code 404.
"""
@ordersRouter.get("/orders/client{id_client}",tags=["orders"])
def get_order_by_client(id_client:int,db:Session=Depends(get_db)):
        data=db.query(orders).filter(orders.user_id==id_client).all()
        return (data,Response(status_code=status.HTTP_404_NOT_FOUND))[data is None]


"""
    If the data is not None, return the data, otherwise return a 404 response
    
    :param id: The id of the order to be retrieved
    :type id: int
    :param db: This is the database session that we will use to query the database
    :type db: Session
    :return: The data or a 404 response
"""
@ordersRouter.get("/orders/{id}",tags=["orders"])
def get_order(id:int,db:Session=Depends(get_db)):
    data = db.query(orders).filter(orders.id==id).first()
    return (data,Response(status_code=status.HTTP_404_NOT_FOUND))[data is None]

    """
    It takes an order object, adds it to the database, and returns a response with a 201 status code
    
    :param order: This is the Order object that we created earlier
    :type order: Order
    :param db: This is the database session that we will use to query the database
    :type db: Session
    :return: a response with a status code of 201.
    """
@ordersRouter.post("/orders",tags=["orders"],status_code=status.HTTP_201_CREATED)
def create_order(order:Order,db:Session=Depends(get_db)):
    new_order = orders(user_id=order.user_id,client_name=order.client_name,client_phone=order.client_phone,client_address=order.client_address,edificios=order.edificios,quantity_per_edificios=order.quantity_per_edificios,total=order.total,status=order.status, date=order.date)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    newlist=new_order.edificios.split(",")
    return Response(status_code=status.HTTP_201_CREATED)

##TODO
#@ordersRouter.put("/orders/{id}",tags=["orders"])

    """
    It deletes an order from the database
    
    :param id: The id of the order to be deleted
    :type id: int
    :param db: This is the database session that we will use to query the database
    :type db: Session
    """
@ordersRouter.delete("/orders/{id}",tags=["orders"])
def delete_order(id:int,db:Session=Depends(get_db)):
    data=db.query(orders).filter(orders.id==id)
    
    if db.query(orders).filter(orders.id==id).first():
        Response(status_code=status.HTTP_404_NOT_FOUND)
        
    data.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)