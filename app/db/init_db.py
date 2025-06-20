"""
Database initialization script
"""

from app.db.base import engine, Base
from app.db.models import Item, User

def init_database():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()