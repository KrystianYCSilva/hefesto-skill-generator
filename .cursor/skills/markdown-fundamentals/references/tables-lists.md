# Tabelas e Listas em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Listas Ordenadas/Não-Ordenadas, Task Lists GFM, Tabelas, Limitações

---

## Overview

Listas e tabelas são as estruturas de organização mais usadas em documentação Markdown. Listas oferecem flexibilidade (ordenadas, não-ordenadas, aninhadas, task lists), enquanto tabelas permitem organizar dados comparativos de forma visual. Conhecer as limitações de cada um evita problemas de renderização.

---

## Listas Não Ordenadas

### Sintaxe Básica

```markdown
- Item um
- Item dois
- Item três
```

Variações de marcador (todos produzem o mesmo resultado):

```markdown
- usando traço
* usando asterisco
+ usando mais
```

**Convenção recomendada:** Use `-` consistentemente no mesmo documento.

### Listas Aninhadas

```markdown
- Item principal
  - Sub-item (2 espaços de indentação)
  - Outro sub-item
    - Sub-sub-item (4 espaços)
- Outro item principal
```

**Regra de indentação:** 2 espaços por nível em listas não ordenadas.

### Listas com Parágrafos

Para ter múltiplos parágrafos dentro de um item, adicione uma linha em branco e indente:

```markdown
- Primeiro item com um parágrafo.

  Este é o segundo parágrafo do mesmo item.
  Indentado com 2 espaços para pertencer ao item.

- Segundo item normal.
```

### Listas com Ênfase e Código

```markdown
- **Instalação:** execute `npm install` no diretório raiz
- *Configuração:* edite o arquivo `config.yaml`
- ~~Método antigo~~: usar `require()` (deprecated)
```

---

## Listas Ordenadas

### Sintaxe Básica

```markdown
1. Primeiro passo
2. Segundo passo
3. Terceiro passo
```

### Auto-Numeração

O Markdown aceita todos os números como `1.` e numera automaticamente:

```markdown
1. Primeiro
1. Segundo
1. Terceiro
<!-- Renderiza como: 1, 2, 3 -->
```

**Vantagem:** Adicionar ou remover itens não quebra a numeração.

### Listas Ordenadas Aninhadas

```markdown
1. Fase de Planejamento
   1. Levantar requisitos
   2. Definir arquitetura
   3. Estimar esforço
2. Fase de Implementação
   1. Setup do ambiente
   2. Desenvolvimento
   3. Testes
3. Fase de Deploy
   1. CI/CD configuração
   2. Deploy em staging
   3. Deploy em produção
```

**Regra de indentação:** 3 espaços por nível em listas ordenadas (alinha com o texto após `1. `).

### Número Inicial Customizado

```markdown
3. Este item começa em 3
4. Este é 4
5. Este é 5
<!-- Renderiza a partir de 3 -->
```

---

## Listas Mistas

Combinando listas ordenadas e não ordenadas:

```markdown
1. **Instalação**
   - Instale Node.js (>= 18)
   - Instale npm ou yarn

2. **Configuração**
   - Clone o repositório
   - Copie `.env.example` para `.env`
   - Configure as variáveis necessárias:
     - `DATABASE_URL`
     - `API_KEY`
     - `PORT`

3. **Execução**
   - Instale dependências: `npm install`
   - Inicie: `npm start`
```

---

## Task Lists (GFM)

Task lists permitem criar checklists interativos. Disponíveis no GitHub, GitLab e algumas outras plataformas.

### Sintaxe Básica

```markdown
- [ ] Tarefa pendente
- [x] Tarefa concluída
- [ ] Outra tarefa pendente
```

### Exemplos Práticos

**Checklist de Deploy:**
```markdown
## Deploy v2.1.0

- [x] Testes unitários passando
- [x] Code review aprovado
- [x] CHANGELOG atualizado
- [ ] Deploy em staging
- [ ] Smoke tests em staging
- [ ] Deploy em produção
- [ ] Monitoramento verificado
```

**Checklist de Feature:**
```markdown
## Feature: Login com OAuth

- [x] Especificação de requisitos
- [x] Design da UI
- [x] Implementação do backend
- [x] Implementação do frontend
- [ ] Testes de integração
- [ ] Documentação da API
- [ ] Revisão de segurança
```

### Task Lists Aninhadas

```markdown
- [ ] Implementar autenticação
  - [x] Criar modelo de usuário
  - [x] Endpoint de registro
  - [ ] Endpoint de login
  - [ ] Token refresh
- [ ] Implementar autorização
  - [ ] Roles e permissões
  - [ ] Middleware de proteção
```

### Compatibilidade de Task Lists

| Plataforma | Suporta Task Lists | Interativo (click para toggle) |
|------------|:------------------:|:------------------------------:|
| GitHub | ✅ | ✅ |
| GitLab | ✅ | ✅ |
| Bitbucket | ✅ | ❌ |
| VS Code Preview | ✅ | ❌ |
| CommonMark padrão | ❌ | ❌ |

---

## Tabelas

Tabelas são uma extensão GFM (não parte do CommonMark padrão). Suportadas pelo GitHub, GitLab, e a maioria dos docs sites.

### Sintaxe Básica

```markdown
| Cabeçalho A | Cabeçalho B | Cabeçalho C |
|-------------|-------------|-------------|
| dado 1      | dado 2      | dado 3      |
| dado 4      | dado 5      | dado 6      |
```

### Alinhamento de Colunas

```markdown
| Esquerda | Centro | Direita |
|:---------|:------:|--------:|
| texto    | texto  |   texto |
| texto    | texto  |   texto |
```

- `:---` → alinha à esquerda (padrão)
- `:---:` → alinha ao centro
- `---:` → alinha à direita

### Tabela de Comparação com Indicadores

```markdown
| Recurso              | Python | Java | Kotlin | Go   |
|----------------------|:------:|:----:|:------:|:----:|
| Tipagem estática     | ❌     | ✅   | ✅     | ✅   |
| Garbage Collection   | ✅     | ✅   | ✅     | ✅   |
| Coroutines nativas   | ✅     | ❌   | ✅     | ✅   |
| Compilação AOT       | ❌     | ✅   | ✅     | ✅   |
| Ecossistema maduro   | ✅     | ✅   | ✅     | ✅   |
```

### Conteúdo Formatado em Células

```markdown
| Comando              | Descrição                          | Exemplo                          |
|----------------------|------------------------------------|----------------------------------|
| `git clone`          | Clona um repositório               | `git clone <url>`                |
| `git checkout`       | Muda de branch                     | `git checkout -b nova-branch`    |
| `git commit`         | Salva alterações **locais**        | `git commit -m "mensagem"`       |
| `git push`           | Envia para o repositório *remoto*  | `git push origin main`           |
```

### Código em Células da Tabela

```markdown
| Método          | Retorno   | Exemplo                    |
|-----------------|-----------|----------------------------|
| `lista.size`    | `Int`     | `listOf(1,2,3).size` → 3   |
| `lista.first()` | `T`       | `listOf("a","b").first()`  |
| `lista.last()`  | `T`       | `listOf("a","b").last()`   |
```

---

## Limitações de Tabelas

### O Que NÃO Funciona em Tabelas

```markdown
<!-- ❌ NÃO funciona: blocos de código multi-linha em células -->
| Comando | Código |
|---------|--------|
| Instalar | ```bash
npm install
``` |

<!-- ❌ NÃO funciona: quebra de linha dentro de célula (padrão) -->
| Nome | Descrição |
|------|-----------|
| X    | Linha 1
         Linha 2 |
```

### Alternativas para Conteúdo Complexo

Quando a tabela não é suficiente, use listas estruturadas:

```markdown
<!-- Alternativa: lista detalhada ao invés de tabela complexa -->
### Comandos Disponíveis

- **`install`** — Instala dependências do projeto
  - Uso: `npm install [pacote]`
  - Sem argumento: instala tudo do `package.json`

- **`test`** — Executa a suite de testes
  - Uso: `npm test [-- --coverage]`
  - Flag `--coverage`: gera relatório de cobertura

- **`build`** — Compila para produção
  - Uso: `npm run build`
  - Saída: diretório `dist/`
```

### Quebra de Linha em Células (Workaround)

Alguns renderizadores suportam `<br>` dentro de células:

```markdown
| Ponto | Descrição |
|-------|-----------|
| 1     | Primeira linha<br>Segunda linha |
| 2     | Apenas uma linha |
```

**Compatibilidade:** GitHub ✅, GitLab ✅, CommonMark ❌

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Marcador consistente nas listas -->
- Item um
- Item dois

<!-- Auto-numeração para listas ordenadas -->
1. Primeiro
1. Segundo
1. Terceiro

<!-- Task lists para checklists -->
- [ ] Pendente
- [x] Concluído

<!-- Tabelas para comparações objetivas -->
| Feature | Valor |
|---------|-------|
| X       | ✅    |
```

### Evitar

```markdown
<!-- Marcadores mistos na mesma lista -->
- Item com traço
* Item com asterisco

<!-- Números errados em listas ordenadas -->
1. Primeiro
3. Segundo  <!-- pula para 3 -->
2. Terceiro <!-- volta para 2 -->

<!-- Tabelas com conteúdo muito longo por célula -->
<!-- Se uma célula precisa de > 2 linhas, use lista ao invés -->

<!-- Indentação inconsistente em listas aninhadas -->
- Pai
    - Filho com 4 espaços  <!-- pode não renderizar como esperado -->
  - Filho com 2 espaços    <!-- forma correta -->
```

---

## Referências

- [CommonMark Spec — Lists](https://spec.commonmark.org/0.31.2/#lists) — Especificação oficial de listas
- [GFM Spec — Tables](https://github.github.com/gfm/#tables-extension-) — Especificação de tabelas GFM
- [GFM Spec — Task List Items](https://github.github.com/gfm/#task-list-items-extension-) — Task lists
- [GitHub Docs — Tables](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables) — Tabelas no GitHub
