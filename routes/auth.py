from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import hash_password, verify_password, create_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from core.database import SessionLocal
from models.user import User
from schemas.user import UserCreate

router = APIRouter()
security = HTTPBearer()


db = SessionLocal()

@router.post("/register")
def register(user: UserCreate):
    
    existing_user = db.query(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = hash_password(user.password)
    new_user = User(email=user.email, password=hashed)
    db.add(new_user)
    db.commit()


    return {"message": "usuario creado"}



@router.post("/login")
def login(email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no existe")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}






def get_current_user(credentials: HTTPAuthorizationCredentials =  Depends(security)):
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")




@router.get("/me")
def get_me(user: str= Depends(get_current_user)):
    
    return {"email": user.email}