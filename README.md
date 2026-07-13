# Fast API Starter Template

Projeto template com algumas configurações comuns já feitas e autenticação JWT implementada para ser usado como base em outros projetos

## Requisitos Necessários 💻

* Python 3.12
* Poetry 2.x

## Como usar? ⚙️

Renomeie o arquivo `.env.example` para `.env` e altere as configurações para as da sua máquina local

### Instalando Dependências

```sh
poetry install
```

### Inicializando a Base de Dados

Configure o banco de dados na sua máquina e execute as migrações

```sh
alembic upgrade head
```

### Executando o Projeto ▶️

```sh
uvicorn app.main:app --reload
```

### Executando os Testes 🧪

```sh
poetry run pytest
```

## Contribuições 🤝

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request para propor melhorias ou correções.
