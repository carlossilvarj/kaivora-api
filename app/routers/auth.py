# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.base import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

# Basic token response model
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Basic login endpoint 
@router.post("/login", response_model=TokenResponse, summary="Login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simple demo authentication
    if form_data.username != "admin" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Return a simple token for demo purposes
    token = f"demo_token_{form_data.username}"
    return {"access_token": token, "token_type": "bearer"}

