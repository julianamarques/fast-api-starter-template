## Migrações com Alembic

* Criar migração:

```sh
alembic revision --autogenerate -m "Create table x"
```

* Aplicar migrações pendentes:

```sh
alembic upgrade head
```

* Aplica um número específico de migrações:

```sh
alembic upgrade +2
```

* Volta um número específico de migrações:

```sh
alembic downgrade +2
```

* Volta todas as migrações:

```sh
alembic downgrade base
```

* Mostra todas as migrações pendentes:

```sh
alembic current
```

* Mostra o histórico de migrações:

```sh
alembic history
```
