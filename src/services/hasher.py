import bcrypt


class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw((password).encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hash_password.encode())
