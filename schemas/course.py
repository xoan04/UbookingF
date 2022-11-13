from pydantic import BaseModel
from typing import Optional

# `OrderDetails` is a `BaseModel` with `id`, `order_id`, `course_id`, `quantity`, `price`,
# `name_course`, and `total` fields

class Course(BaseModel):
    id: Optional[int]
    name_course:str
    busy:bool
    horario:str
    edificio_id:int
    


    class Config:
        orm_mode = True