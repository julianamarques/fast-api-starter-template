# Como Contribuir?

Obrigado pelo interesse contribuir com o Fast API Starter Template. Este guia descreve o fluxo recomendado para propor correções, melhorias e ajustes de documentação.

## Fluxo de Trabalho

- Faça um fork do repositório e clone o projeto.
- Crie uma branch a partir da branch principal.
- Use nomes de branch objetivos, como `feature/nome-da-feature` ou
  `fix/descricao-do-ajuste`.
- Consulte o `README.md` para configurações locais e execução da aplicação.
- Mantenha pull requests pequenos e focados em uma mudança principal.
- Explique no pull request o problema resolvido, a solução aplicada e como a
  alteração foi validada.

## Commits

Prefira mensagens curtas, no imperativo e com um prefixo que indique o tipo da
mudança:

```text
feat: adiciona endpoint de cadastro de usuário
fix: corrige validação de token expirado
docs: atualiza instruções de contribuição
chore: atualiza dependências do projeto
db: cria migration para tabela de usuários
```

## Padrões de Código

- Siga a organização existente em `app/api`, `app/services`, `app/schemas`,
  `app/models`, `app/core` e `app/utils`.
- Prefira tipagem explícita, nomes claros e funções pequenas.
- Não inclua credenciais, tokens, arquivos `.env` ou dados sensíveis no
  controle de versão.
- Ao alterar contratos de API, atualize schemas, services e exemplos de
  requests relacionados.
- Ao alterar modelos persistidos, crie ou atualize migrations do Alembic.

## Validação

Antes de abrir um pull request, rode as verificações aplicáveis:

```sh
poetry run flake8 app tests
poetry run pylint app
```

Também revise se:

- A alteração está limitada ao escopo proposto.
- Novas regras de negócio possuem testes quando aplicável.
- Nenhuma credencial, token ou dado sensível foi versionado.
- A documentação foi atualizada quando a alteração muda o uso do projeto.
- Se a alteração envolver rotas HTTP, valide o comportamento localmente e atualize os exemplos em `tests/*.http` quando necessário.

## Pull Requests

Ao abrir um pull request, inclua:

- Um resumo curto da alteração.
- O motivo da mudança.
- Os comandos executados para validação.
- Observações sobre migrations, variáveis de ambiente ou impactos de
  compatibilidade, se existirem.

## Issues

Ao abrir uma issue, informe:

- Descrição clara do problema ou melhoria.
- Passos para reproduzir, quando for um bug.
- Comportamento esperado e comportamento atual.
- Versões de Python, Poetry e banco utilizadas.
- Logs ou stack traces relevantes.
