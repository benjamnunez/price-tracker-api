from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.product import ProductCreate, ProductResponse
from services.product_service import create_product
from routes.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProductResponse)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        new_product = create_product(
            db=db,
            user_id=current_user.id,
            url=product.url
        )
        return new_product

    except Exception as e:
        print("ERROR REAL:", e)  # 👈 PARA DEBUG
        raise HTTPException(status_code=400, detail=str(e))