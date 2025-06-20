# app/db/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.db.models import User

def get_user_by_username(db: Session, username: str):
    """
    Busca um usuário no banco pelo nome de usuário.
    """
    return db.query(User).filter(User.username == username).first()
