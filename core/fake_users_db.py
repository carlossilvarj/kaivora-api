from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    hashed_password: str
    disabled: bool | None = None
E uma simulação de banco (para teste) em app/db/fake_users_db.py: