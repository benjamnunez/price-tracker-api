from pydantic import BaseModel
from datetime import datetime

class PriceHistoryResponse(BaseModel):
    price: float
    checked_at: datetime

    class Config:
        from_attributes = True