from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    url: str

class ProductResponse(BaseModel):
    id: int
    name: Optional[str]
    url: str
    current_price: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True