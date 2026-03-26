from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Product(Base):
    __tablename__= "products"
    
    id = Column(Integer, primary_key=True, index=True)
    
    #relacion con usuario
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    #Datos producto
    url = Column(String, nullable=False)
    name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    store = Column(String, nullable=True)
    
    #precio actual
    current_price=Column(Float, nullable=True)
    
    #Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, nullable=True)
    
    #Relaciones
    price_history = relationship("PriceHistory", back_populates="product")