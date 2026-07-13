# Configuração de ambiente dos testes. Este módulo executa antes de qualquer
# import de `app.*` (o pytest importa o pacote antes do conftest), garantindo
# que o `settings` seja criado com valores determinísticos mesmo sem .env —
# variáveis de ambiente têm precedência sobre o .env local de quem roda.
import os

os.environ["SECRET_KEY"] = "test-secret-key-with-at-least-32-bytes!"
os.environ["ENVIRONMENT"] = "testing"
os.environ["TOKEN_ALGORITHM"] = "HS256"

# O engine é criado no import de app.core.database_config, mas nunca conecta:
# os testes substituem a dependência de sessão por um SQLite em memória
os.environ["POSTGRES_SCHEME"] = "postgresql+psycopg"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DATABASE"] = "test"
