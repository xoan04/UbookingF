from pydantic import BaseModel
from typing import Optional

# `Order` is a class that inherits from `BaseModel` and has the following fields: `id`, `user_id`,
# `client_name`, `client_phone`, `client_address`, `quantity_per_edificios`, `edificios`, `status`,
# `date`, `total`
class Order(BaseModel):
    id: Optional[int]
    user_id: int
    client_name: str
    client_phone: str
    client_address: str
    edificio:str
    course:str
    status: str
    date: str

    class Config:
        orm_mode = True