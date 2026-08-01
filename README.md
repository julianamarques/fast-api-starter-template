# ⚡ FastAPI Starter Template

[![CI](https://github.com/julianamarques/fast-api-starter-template/actions/workflows/github-ci.yml/badge.svg)](https://github.com/julianamarques/fast-api-starter-template/actions/workflows/github-ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

Projeto template com algumas configurações comuns já feitas e autenticação JWT implementada para ser usado como base em outros projetos.

## 💻 Requisitos Necessários

* Python 3.12
* Poetry 2.4.1+

## 📂 Estrutura do Projeto

```text
├── .github/workflows/     # CI: pylint, flake8 e pytest a cada push/PR
├── alembic/               # Migrações do banco de dados
├── app/
│   ├── api/
│   │   ├── routes/        # Endpoints da API (auth, health)
│   │   ├── main.py        # Agregador de rotas
│   │   └── responses.py   # Envelope padrão das respostas
│   ├── core/              # Configurações (variáveis de ambiente, engine do banco)
│   ├── models/            # Modelos do ORM (SQLAlchemy)
│   ├── schemas/           # Schemas de entrada e saída (Pydantic)
│   ├── services/          # Regras de negócio (autenticação, usuários)
│   ├── utils/             # Token JWT, hash de senha e exceções HTTP
│   ├── depends.py         # Dependências injetáveis (sessão, usuário autenticado)
│   ├── enums.py           # Mensagens padronizadas da API
│   ├── handlers.py        # Tratamento global de exceções
│   └── main.py            # Bootstrapping do FastAPI (CORS, handlers, rotas)
├── tests/                 # Testes de integração com pytest
├── .env.example           # Modelo das variáveis de ambiente
├── Dockerfile             # Build multi-stage da imagem da API
├── docker-compose.yml     # Sobe migrações e API em containers
└── pyproject.toml         # Dependências e configurações (Poetry)
```

## 🛠️ Como Configurar?

Renomeie o arquivo `.env.example` para `.env`, altere as configurações para as da sua máquina local e gere uma `SECRET_KEY` com o comando:

```sh
sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')|" .env # LINUX
sed -i '' "s|^SECRET_KEY=.*|SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')|" .env # MACOS
```

### 📦 Instalando Dependências

Instale as dependências e em seguida ative o ambiente virtual com os comandos:

```sh
poetry install && source "$(poetry env info --path)/bin/activate"
```

### 💾 Inicializando a Base de Dados

Configure o banco de dados na sua máquina e execute as migrações

```sh
alembic upgrade head
```

### 🚀 Executando o Projeto

#### Opção 1: Executando Localmente

```sh
uvicorn app.main:app --reload
```

#### Opção 2: Executando com Docker

```sh
docker compose up -d --build
```

O serviço `migrations` executa `alembic upgrade head` automaticamente antes da API subir. Para rodar apenas as migrações, sem subir a API

```sh
docker compose run --rm migrations
```

## 🧪 Executando os Testes

Você pode executar os testes da aplicação com o comando:

```sh
poetry run pytest
```

## ✅ Lint

Você pode verificar a qualidade e o padrão de formatação do código através do comando:

```sh
poetry run pylint app tests && poetry run flake8
```

## 📖 Documentação da API (Swagger)

A documentação interativa (OpenAPI 3) é gerada automaticamente pelo FastAPI. Com a aplicação no ar, acesse:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/application_name/openapi.json`

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request para propor melhorias ou correções. Leia o [CONTRIBUTING](CONTRIBUTING.md) para orientações.
