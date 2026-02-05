# Tabelas e Listas em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Listas Ordenadas e Não-Ordenadas, Listas Aninhadas, Task Lists (GFM), Tabelas com Alinhamento, Conteúdo Complexo em Tabelas

---

## Overview

Listas e tabelas são estruturas de dados fundamentais em documentação técnica. Listas organizam informações sequencialmente ou por categorias, enquanto tabelas apresentam dados em formato comparativo. O domínio da sintaxe e das regras de indentação é crítico para renderização correta entre plataformas.

---

## Listas Não Ordenadas

### Sintaxe Básica

```markdown
- Item A
- Item B
- Item C
```

Os marcadores aceitos são `-`, `*` ou `+`. Prefer usar `-` por consistência.

### Listas Aninhadas

A indentação controla o nível da hierarquia. Use **2 espaços** para cada nível (padrão mais compatível).

```markdown
- Linguagens de Programação
  - Compiladas
    - C
    - C++
    - Rust
  - Interpretadas
    - Python
    - JavaScript
    - Ruby
- Frameworks
  - Web
    - Django
    - React
    - Laravel
  - Mobile
    - Flutter
    - React Native
```

### Listas com Parágrafos

Para incluir múltiplos parágrafos em um item, indente o segundo parágrafo:

```markdown
- Primeiro item com um parágrafo longo que pode
  continuar na próxima linha.

  Este é o segundo parágrafo do mesmo item.
  Ele pertence ao item porque está indentado.

- Segundo item simples.
```

### Listas com Ênfase

```markdown
- **Importante:** Nunca use credenciais hardcoded
- *Nota:* Este campo é opcional
- **Dica:** Use `val` quando possível
```

---

## Listas Ordenadas

### Sintaxe Básica

```markdown
1. Primeiro passo
2. Segundo passo
3. Terceiro passo
```

### Numeração Automática

O CommonMark permite usar `1.` para todos os itens — a numeração é calculada automaticamente:

```markdown
1. Instalar dependências
1. Configurar ambiente
1. Executar testes
1. Deploy
```

**Renderiza como:** 1, 2, 3, 4

### Listas Ordenadas Aninhadas

```markdown
1. Fase de Planejamento
   1. Definir requisitos
   2. Estimar esforço
   3. Priorizar tarefas
2. Fase de Desenvolvimento
   1. Implementar features
   2. Escrever testes
   3. Code review
3. Fase de Deploy
   1. Ambiente staging
   2. Testes de integração
   3. Ambiente produção
```

### Começando em Número Diferente de 1

```markdown
3. Este item começa em 3
4. Este é o quarto
5. Este é o quinto
```

---

## Listas Mistas (Ordenadas + Não Ordenadas)

```markdown
1. **Configuração inicial**
   - Instalar Node.js
   - Instalar npm
   - Configurar PATH

2. **Instalação do projeto**
   - Clone do repositório
   - Instalação de dependências

3. **Execução**
   - Comando de start
   - Verificação no browser
```

---

## Task Lists (GFM)

Task lists são uma extensão do GitHub Flavored Markdown. Permitem criar listas com checkboxes interativos no GitHub.

### Sintaxe

```markdown
- [ ] Tarefa pendente
- [x] Tarefa concluída
- [ ] Outra tarefa pendente
```

### Exemplos Práticos

```markdown
## Checklist de Deploy

- [x] Código revisado e aprovado
- [x] Testes unitários passando
- [ ] Testes de integração validados
- [ ] Documentação atualizada
- [ ] Changelog atualizado
- [ ] Tag de versão criada
- [ ] Deploy em staging
- [ ] Aprovação do QA
- [ ] Deploy em produção
```

```markdown
## Features da versão 2.0

- [x] Autenticação OAuth2
- [x] API REST completa
- [ ] Dashboard de admin
- [ ] Exportação de relatórios
- [ ] Integração com Slack
```

### Task Lists Aninhadas

```markdown
- [ ] Implementar módulo de usuários
  - [x] Modelo de dados
  - [x] Endpoints CRUD
  - [ ] Validação de entrada
  - [ ] Testes unitários
- [ ] Implementar módulo de pedidos
  - [ ] Modelo de dados
  - [ ] Endpoints CRUD
```

### Compatibilidade de Task Lists

| Plataforma | Task Lists | Interativo no UI |
|------------|:----------:|:----------------:|
| GitHub     | Sim        | Sim              |
| GitLab     | Sim        | Sim              |
| Bitbucket  | Sim        | Não              |
| CommonMark | Não        | Não              |
| MkDocs     | Depende da extensão | Não    |

---

## Tabelas

Tabelas são uma extensão do GFM (não parte do CommonMark estrito).

### Sintaxe Básica

```markdown
| Cabeçalho A | Cabeçalho B | Cabeçalho C |
|-------------|-------------|-------------|
| Valor 1     | Valor 2     | Valor 3     |
| Valor 4     | Valor 5     | Valor 6     |
```

### Alinhamento de Colunas

O segundo row (separador) controla o alinhamento:

```markdown
| Esquerda | Centro   | Direita  |
|:---------|:--------:|---------:|
| texto    | texto    | texto    |
```

- `:---` ou `:------` → alinhamento à esquerda (padrão)
- `:---:` ou `:------:` → alinhamento centralizado
- `---:` ou `------:` → alinhamento à direita

### Exemplos com Alinhamento

```markdown
| Comando          | Descrição                    | Exemplo          |
|:-----------------|:----------------------------:|:-----------------|
| `git clone`      | Clona um repositório         | `git clone URL`  |
| `git pull`       | Atualiza o repositório local | `git pull origin main` |
| `git push`       | Envia mudanças para remoto   | `git push`       |
| `git status`     | Mostra estado do working dir | `git status`     |
```

### Tabela de Comparação com Indicadores

```markdown
| Recurso              | Versão 1.x | Versão 2.x | Versão 3.x |
|:---------------------|:----------:|:----------:|:----------:|
| Autenticação básica  | Sim        | Sim        | Sim        |
| OAuth2               | Não        | Sim        | Sim        |
| Rate limiting        | Não        | Não        | Sim        |
| Webhooks             | Não        | Sim        | Sim        |
| GraphQL              | Não        | Não        | Sim        |
| Versionamento da API | Não        | Sim        | Sim        |
```

### Conteúdo Formatado em Tabelas

Tabelas suportam formatação inline dentro das células:

```markdown
| Elemento     | Sintaxe                          | Exemplo                   |
|:-------------|:--------------------------------|:--------------------------|
| Negrito      | `**texto**`                     | **negrito**               |
| Itálico      | `*texto*`                       | *itálico*                 |
| Código       | `` `código` ``                  | `código`                  |
| Link         | `[texto](url)`                  | [GitHub](https://github.com) |
```

### Tabela com Código em Célula

```markdown
| Método   | Retorno    | Descrição                              |
|:---------|:-----------|:---------------------------------------|
| `GET`    | `200 OK`   | Retorna lista de recursos              |
| `POST`   | `201 Created` | Cria um novo recurso                |
| `PUT`    | `200 OK`   | Atualiza recurso existente             |
| `DELETE` | `204 No Content` | Remove o recurso especificado    |
```

---

## Limitações de Tabelas

### O que NÃO funciona dentro de tabelas

```markdown
<!-- NÃO funciona: blocos de código multi-linha -->
| Exemplo | Código |
|---------|--------|
| Python  | ```python ... ``` |   <!-- QUEBRA a tabela -->

<!-- NÃO funciona: quebras de linha dentro da célula -->
| Ítem | Descrição |
|------|-----------|
| A    | Linha 1   |
|      | Linha 2   |   <!-- Não é continuação, é nova linha da tabela -->
```

### Alternativas para Conteúdo Complexo

Quando uma tabela não é suficiente, use uma lista estruturada ou seções separadas:

```markdown
<!-- Alternativa: lista com detalhes -->
- **GET /api/usuarios**
  - Retorno: `200 OK`
  - Corpo: Lista de usuários
  - Autenticação: Obrigatória

- **POST /api/usuarios**
  - Retorno: `201 Created`
  - Corpo: Novo usuário criado
  - Autenticação: Obrigatória (admin)
```

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Consistência no marcador de lista -->
- Item A
- Item B
- Item C

<!-- Indentação com 2 espaços para listas aninhadas -->
- Pai
  - Filho
    - Neto

<!-- Task lists para checklists no GitHub/GitLab -->
- [x] Conclusão
- [ ] Pendente

<!-- Tabelas para dados comparativos com poucas colunas -->
| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
```

### Evitar

```markdown
<!-- Marcadores inconsistentes na mesma lista -->
- Item A
* Item B      <!-- mistura - e * -->
+ Item C      <!-- mistura com + -->

<!-- Indentação com tabs (comportamento inconsistente entre renderizadores) -->
-	Item com tab

<!-- Tabelas com muitas colunas (difícil de ler no código fonte) -->
<!-- Preferir lista estruturada ou dividir em múltiplas tabelas -->

<!-- Task lists fora do GitHub/GitLab onde não são suportadas -->
```

---

## Referências

- [CommonMark Spec — Lists](https://spec.commonmark.org/0.31.2/#lists) — Regras de indentação e listas
- [GitHub Docs — Task Lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables) — Task lists interativas
- [GFM Spec — Tables](https://github.github.com/gfm/#tables-extension-) — Especificação de tabelas GFM
- [GitLab Docs — Tables](https://docs.gitlab.com/ee/user/markdown.html#tables) — Tabelas no GitLab
