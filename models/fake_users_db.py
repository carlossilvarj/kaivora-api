from app.core.security import hash_password

fake_users_db = {
    "kai": {
        "username": "kai",
        "full_name": "Kai da Kaivora",
        "email": "kai@kaivora.com",
        "hashed_password": hash_password("senha123"),
        "disabled": False,
    }
}