# create_db.py

from app.db.base import Base
from app.db.session import engine
from app.models.user import User

print("🎉 Criando tabelas no banco...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso.")
