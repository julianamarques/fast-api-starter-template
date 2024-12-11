# fast-api-starter-template

Projeto template com algumas configurações comuns já feitas e autenticação JWT implementada para ser usado como base em outros projetos

## Requisitos Necessários 💻

* Python 3.10
* Poetry 1.8.4

## Como usar? ⚙️

Renomeie o arquivo `.env.example` para `.env` e altere as configurações para as da sua máquina local

### Instalando Dependências

```sh
poetry install
```

### Inicializando a Base de Dados

Caso o projeto esteja sendo executado pela primeira vez, execute as migrações usando:

```sh
alembic upgrade head
```

### Executando o Projeto ▶️

```sh
uvicorn app.main:app --reload
```

## Contribuições 🤝

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma pull request para propor melhorias ou correções.
