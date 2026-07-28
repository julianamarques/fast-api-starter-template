import os

os.environ["SECRET_KEY"] = "test-secret-key-with-at-least-32-bytes!"
os.environ["ENVIRONMENT"] = "testing"
os.environ["TOKEN_ALGORITHM"] = "HS256"

os.environ["POSTGRES_SCHEME"] = "postgresql+psycopg"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DATABASE"] = "test"
