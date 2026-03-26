from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    price = Column(Float, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    #Relacion inversa
    product = relationship("Product", back_populates="price_history")