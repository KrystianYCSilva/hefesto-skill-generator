# Blocos de Código em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Código Inline, Blocos Cercados, Realce de Sintaxe, Diff, Código em Listas

---

## Overview

Blocos de código são um dos elementos mais usados em documentação técnica. O Markdown oferece duas formas principais: código inline (para trechos curtos dentro de um parágrafo) e blocos cercados (para trechos maiores com realce de sintaxe). Dominar ambas e suas variações garante documentação clara e renderizada corretamente em todas as plataformas.

---

## Código Inline

Usado para referências curtas a código dentro de texto corrido.

```markdown
<!-- Sintaxe básica: um par de backticks -->
Use o método `getData()` para recuperar os dados.

<!-- Variável e tipo -->
A variável `count` é do tipo `int`.

<!-- Comando terminal -->
Instale com `npm install pacote-nome`.

<!-- Caminho de arquivo -->
Configure o arquivo `config/settings.yaml` antes de iniciar.
```

### Backtick dentro de Código Inline

Se o trecho de código contém um backtick, use dois backticks para delimitar:

```markdown
<!-- Um backtick dentro: usar dois backticks como delimitador -->
Use `` ` `` para delimitar código inline.

<!-- Exemplo prático -->
O template literal usa `` `texto ${variavel}` `` no JavaScript.

<!-- Três backticks dentro: usar quatro como delimitador -->
```` Para bloco cercado, use ``` ````
```

---

## Blocos de Código Cercados

A forma principal para trechos de código multi-linha com realce de sintaxe.

### Sintaxe Básica

````markdown
<!-- Bloco cercado com linguagem especificada -->
```python
def saudacao(nome: str) -> str:
    return f"Olá, {nome}!"

resultado = saudacao("Alice")
print(resultado)  # Olá, Alice!
```
````

### Exemplos por Linguagem

**Bash / Shell:**
````markdown
```bash
# Instalar dependências
npm install

# Executar testes
npm test

# Build para produção
npm run build
```
````

**SQL:**
````markdown
```sql
-- Buscar usuários ativos com seus pedidos
SELECT u.nome, COUNT(p.id) AS total_pedidos
FROM usuarios u
LEFT JOIN pedidos p ON p.usuario_id = u.id
WHERE u.ativo = true
GROUP BY u.nome
HAVING COUNT(p.id) > 0
ORDER BY total_pedidos DESC;
```
````

**JSON:**
````markdown
```json
{
  "nome": "meu-projeto",
  "versao": "1.0.0",
  "dependencias": {
    "express": "^4.18.0",
    "typescript": "^5.0.0"
  },
  "scripts": {
    "iniciar": "node index.js",
    "teste": "jest"
  }
}
```
````

**YAML:**
````markdown
```yaml
nome: meu-workflow
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```
````

**TypeScript:**
````markdown
```typescript
interface Usuario {
  id: number;
  nome: string;
  email: string;
  ativo: boolean;
}

async function buscarUsuario(id: number): Promise<Usuario | null> {
  const resposta = await fetch(`/api/usuarios/${id}`);
  if (!resposta.ok) return null;
  return resposta.json();
}
```
````

### Identificadores de Linguagem Suportados

Praticamente todos os renderizadores suportam as linguagens abaixo (via highlight.js ou similar):

| Linguagem | Identificador | Linguagem | Identificador |
|-----------|---------------|-----------|---------------|
| Python | `python` ou `py` | JavaScript | `javascript` ou `js` |
| TypeScript | `typescript` ou `ts` | Java | `java` |
| Kotlin | `kotlin` ou `kt` | C# | `csharp` ou `cs` |
| C++ | `cpp` | Rust | `rust` |
| Go | `go` | Ruby | `ruby` |
| PHP | `php` | Swift | `swift` |
| SQL | `sql` | HTML | `html` |
| CSS | `css` | JSON | `json` |
| YAML | `yaml` | TOML | `toml` |
| Bash | `bash` ou `sh` | Dockerfile | `dockerfile` |
| Markdown | `markdown` ou `md` | XML | `xml` |
| GraphQL | `graphql` | Terraform | `hcl` ou `terraform` |
| Docker Compose | `yaml` | INI | `ini` |

### Bloco sem Linguagem Especificada

```markdown
<!-- Sem identificador: sem realce de sintaxe, mas ainda formatado como bloco -->
```
Texto simples sem realce.
Útil para saída de terminal ou texto genérico.
```
```

---

## Código Indentado (Estilo Antigo)

Blocos de código podem ser criados com 4 espaços ou 1 tab de indentação. **Evite este estilo** — não suporta especificação de linguagem.

```markdown
    # Isto é um bloco de código indentado
    # Sem realce de sintaxe
    def exemplo():
        pass
```

**Por que evitar:**
- Sem suporte a realce de sintaxe
- Conflita com listas aninhadas (indentação ambígua)
- Blocos cercados são mais explícitos e portáveis

---

## Blocos com Quatro Backticks

Para mostrar **sintaxe de Markdown** dentro de um bloco de código, use quatro backticks como delimitador:

`````markdown
<!-- Usando 4 backticks para mostrar um bloco cercado com 3 -->
````markdown
```python
print("Isto é um exemplo dentro de um bloco")
```
````
`````

---

## Código em Listas

Inserir blocos de código dentro de listas requer indentação correta.

### Em Listas Não Ordenadas

````markdown
- **Passo 1:** Instale as dependências

  ```bash
  npm install
  ```

- **Passo 2:** Configure o ambiente

  ```bash
  cp .env.example .env
  ```

- **Passo 3:** Inicie o servidor

  ```bash
  npm start
  ```
````

**Regra:** O bloco de código deve estar indentado com **2 espaços** (alinhado ao conteúdo do item de lista) e ter uma linha em branco antes.

### Em Listas Ordenadas

````markdown
1. Clone o repositório:

   ```bash
   git clone https://github.com/usuario/repo.git
   ```

2. Instale dependências:

   ```bash
   cd repo && npm install
   ```

3. Execute os testes:

   ```bash
   npm test
   ```
````

**Regra:** Em listas ordenadas, a indentação é de **3 espaços** (alinhado ao texto após `1. `).

### Em Blockquotes

````markdown
> Para instalar, execute:
>
> ```bash
> npm install pacote-nome
> ```
>
> E depois configure com:
>
> ```yaml
> nome: valor
> ```
````

---

## Blocos Diff

Blocos `diff` mostram alterações entre versões de código. Muito útil em documentação de migração ou changelog.

### Sintaxe

````markdown
```diff
- linha removida (aparece em vermelho)
+ linha adicionada (aparece em verde)
  linha sem alteração (sem cor)
```
````

### Exemplo: Migração de Código Python

````markdown
```diff
- import requests
+ import httpx

  async def buscar_dados(url: str):
-     response = requests.get(url)
-     return response.json()
+     async with httpx.AsyncClient() as client:
+         response = await client.get(url)
+         return response.json()
```
````

### Exemplo: Atualização de Dependências

````markdown
```diff
  {
    "dependencias": {
-     "express": "^4.17.0",
-     "lodash": "^4.17.21"
+     "express": "^4.18.0",
+     "lodash": "^4.17.21",
+     "helmet": "^7.0.0"
    }
  }
```
````

### Exemplo: Alteração em Arquivo de Configuração

````markdown
```diff
  # nginx.conf
  server {
      listen 80;
-     server_name localhost;
+     server_name meu-dominio.com;
+     return 301 https://$server_name$request_uri;
  }
+
+ server {
+     listen 443 ssl;
+     server_name meu-dominio.com;
+     ssl_certificate /path/to/cert.pem;
+ }
```
````

---

## Números de Linha e Destaque de Linhas

Funcionalidades extras suportadas por certas plataformas (MkDocs, Docusaurus) mas não pelo CommonMark padrão.

### MkDocs com Extensão `pymdownx.highlight`

````markdown
<!-- Números de linha -->
```python linenums="1"
def soma(a, b):
    return a + b

resultado = soma(3, 4)
```

<!-- Destaque de linhas específicas -->
```python linenums="1" hl_lines="2 4"
def soma(a, b):
    return a + b          # esta linha é destacada

resultado = soma(3, 4)   # esta também
```
````

### Docusaurus

````markdown
<!-- Destaque de linhas com comentários especiais -->
```python
def soma(a, b):
    # highlight-next-line
    return a + b

# highlight-start
resultado = soma(3, 4)
print(resultado)
# highlight-end
```
````

**Nota:** Estas funcionalidades não funcionam no GitHub ou GitLab — verifique a compatibilidade antes de usar.

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Sempre especifique a linguagem -->
```python
print("sempre com linguagem")
```

<!-- Código inline para referências curtas -->
Use `await` para chamadas assíncronas.

<!-- Diff para mostrar alterações -->
```diff
- código antigo
+ código novo
```
```

### Evitar

```markdown
<!-- Sem linguagem especificada (quando possível evitar) -->
```
sem realce
```

<!-- Código indentado (estilo antigo) -->
    sem linguagem e sem realce

<!-- Blocos muito longos sem divisão -->
<!-- Se um bloco tem mais de 50 linhas, considere dividir ou referenciar um arquivo -->
```

---

## Referências

- [CommonMark Spec — Code Spans](https://spec.commonmark.org/0.31.2/#code-spans) — Código inline
- [CommonMark Spec — Fenced Code Blocks](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) — Blocos cercados
- [GitHub Docs — Code Blocks](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks) — Realce de sintaxe no GitHub
- [MkDocs — Highlight Extension](https://facelessuser.github.io/pymdown-extensions/extensions/highlight/) — Números de linha e destaque
