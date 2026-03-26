from fastapi import FastAPI
from routes import auth, products
from core.database import engine, Base
from models import user



Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(auth.router),
app.include_router(products.router)

