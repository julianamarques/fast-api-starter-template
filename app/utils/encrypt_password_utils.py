import bcrypt

MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")

    if len(password_bytes) > MAX_PASSWORD_BYTES:
        return False

    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
