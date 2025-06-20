# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.models import user as user_schemas
from app.core.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schemas.UserCreate, summary="Registrar novo usuário")
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um usuário com o mesmo nome ou email
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário com este nome ou email já existe"
        )

    # Cria novo usuário com senha protegida
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return user
