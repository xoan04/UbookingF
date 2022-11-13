from pydantic import BaseModel
from typing import Optional

# The `edificio` class is a `BaseModel` that has an `id` that is an `Optional[int]`, a `name` that is a
# `str`, a `code` that is an `int`, a `Quantity` that is an `int`, and a `price` that is a `float`
class Edificio(BaseModel):
    id: Optional[int]
    name: str
    code: int

  

    class Config:
        orm_mode = True