# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core import auth
from app.db.base import get_db
from app.db.crud_users import get_user_by_username, get_user_by_email, create_user
from app.models.user import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Response model for Swagger
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Login endpoint with database verification
@router.post("/login", response_model=TokenResponse, summary="Login Authentication")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Register new user endpoint
@router.post("/register", response_model=Token, summary="Register new user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_created = create_user(db, user)
    token = auth.create_access_token({"sub": user_created.username})
    return Token(access_token=token)