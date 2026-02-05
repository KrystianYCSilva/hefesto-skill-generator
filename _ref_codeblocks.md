# Blocos de Código em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Código Inline, Blocos Cercados, Realce de Sintaxe, Código Indentado, Código em Listas, Blocos Diff

---

## Overview

Blocos de código são um dos elementos mais utilizados em documentação técnica. O Markdown oferece duas formas principales: código inline (para trechos curtos dentro de um parágrafo) e blocos cercados (para trechos maiores com realce de sintaxe). Dominar ambas as formas garante documentação clara e renderizada corretamente.

---

## Código Inline

Usado para referências a código dentro de texto corrido. Delimitado por um par de backticks.

### Sintaxe

```markdown
Use o comando `git clone` para clonar o repositório.
```

**Renderiza:** Use o comando `git clone` para clonar o repositório.

### Exemplos Práticos

```markdown
<!-- Comandos -->
Execute `npm install` antes de iniciar o projeto.

<!-- Nomes de variáveis e funções -->
A função `calcularTotal()` retorna o valor em `float`.

<!-- Nomes de arquivos -->
Configure as variáveis no arquivo `.env`.

<!-- Valores e strings -->
O padrão padrão é `localhost:3000`.

<!-- Caminho de arquivo -->
Edite o arquivo em `src/config/database.ts`.
```

### Código Inline com Backtick Dentro

Se o seu código contém um backtick, use dois backticks como delimitador:

```markdown
<!-- Código contendo backtick -->
`` const template = `Hello ${name}` ``

<!-- Ou adicione espaço após/antes dos delimitadores -->
`` ` `` é usado para template literals no JavaScript.
```

---

## Blocos de Código Cercados (Fenced Code Blocks)

O método padrão para blocos de código maiores. Delimitado por três backticks na linha de abertura e três na linha de fechamento.

### Sintaxe Básica

````markdown
```
código sem realce de sintaxe
```
````

### Com Especificação de Linguagem (Realce de Sintaxe)

````markdown
```javascript
const saudacao = (nome) => `Olá, ${nome}!`;
console.log(saudacao("mundo"));
```
````

### Linguagens Comuns e Seus Identificadores

```markdown
<!-- Identificadores aceitos pela maioria dos renderizadores -->

javascript / js
typescript / ts
python / py
java
kotlin / kts
bash / sh / shell
sql
html
css / scss / sass
json
yaml / yml
xml
markdown / md
dockerfile
makefile
ruby / rb
go / golang
rust / rs
c / cpp / c++
csharp / cs
php
swift
dart
r
matlab
lua
```

### Exemplos por Linguagem

````markdown
```python
def fibonacci(n: int) -> list[int]:
    """Gera a sequência de Fibonacci até n termos."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    sequencia = [0, 1]
    for _ in range(2, n):
        sequencia.append(sequencia[-1] + sequencia[-2])
    return sequencia
```
````

````markdown
```bash
# Instalar dependências e iniciar servidor
npm install
npm run build
npm start
```
````

````markdown
```sql
-- Buscar usuários ativos com seus pedidos recentes
SELECT u.nome, u.email, COUNT(p.id) AS total_pedidos
FROM usuarios u
LEFT JOIN pedidos p ON p.usuario_id = u.id
WHERE u.ativo = true
  AND p.criado_em >= NOW() - INTERVAL '30 days'
GROUP BY u.id, u.nome, u.email
ORDER BY total_pedidos DESC;
```
````

````markdown
```json
{
  "nome": "meu-projeto",
  "versao": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "test": "jest --coverage"
  },
  "dependencias": {
    "express": "^4.18.2"
  }
}
```
````

---

## Código Indentado (Método Alternativo)

No CommonMark, linhas indentadas com 4 espaços ou 1 tab são tratadas como bloco de código. **Não suporta realce de sintaxe.**

```markdown
    const x = 42;
    console.log(x);
    // Saída: 42
```

**Quando usar:** Raramente. Prefira sempre blocos cercados com especificação de linguagem.

**Limitações:**
- Sem realce de sintaxe
- Pode confundir com listas indentadas
- Não funciona dentro de listas sem indentação adicional

---

## Blocos Cercados com Quatro Backticks

Quando seu bloco de código contém três backticks dentro (por exemplo, para mostrar sintaxe Markdown), use quatro backticks como delimitador externo.

`````markdown
````markdown
Isto é um bloco de código cercado:

```python
print("Olá!")
```
````
`````

---

## Código em Listas

Incluir blocos de código dentro de itens de lista requer indentação adequada.

### Em Lista Não Ordenada

````markdown
- **Passo 1:** Instale o Node.js

  ```bash
  sudo apt install nodejs
  ```

- **Passo 2:** Instale as dependências

  ```bash
  npm install
  ```

- **Passo 3:** Inicie o servidor

  ```bash
  npm start
  ```
````

**Regra:** O bloco de código dentro de um item de lista deve estar indentado com 2 ou 4 espaços (alinhado com o conteúdo do item).

### Em Lista Ordenada

````markdown
1. Clone o repositório:

   ```bash
   git clone https://github.com/usuario/projeto.git
   cd projeto
   ```

2. Crie o arquivo de configuração:

   ```bash
   cp .env.example .env
   ```

3. Execute as migrations:

   ```bash
   npm run migrate
   ```
````

### Em Blockquote com Código

````markdown
> **Nota importante:** Use sempre a versão LTS do Node.js.
>
> ```bash
> node --version
> # Saída esperada: v20.x.x (LTS)
> ```
````

---

## Blocos Diff (Comparação de Código)

A linguagem `diff` permite mostrar mudanças com linhas adicionadas (verde) e removidas (vermelho).

### Sintaxe

````markdown
```diff
- linha removida
+ linha adicionada
  linha sem alteração
```
````

### Exemplos Práticos

````markdown
```diff
- const nome = "mundo";
+ const nome = "Markdown";
  console.log(`Olá, ${nome}!`);
```
````

````markdown
```diff
  function calcular(a, b) {
-   return a + b;
+   if (typeof a !== 'number' || typeof b !== 'number') {
+     throw new Error('Argumentos devem ser números');
+   }
+   return a + b;
  }
```
````

````markdown
```diff
  # requirements.txt
  flask==2.3.3
- requests==2.28.0
+ requests==2.31.0
+ python-dotenv==1.0.0
```
````

---

## Blocos de Código com Números de Linha

A maioria dos renderizadores padrão (GitHub, GitLab) **não suporta** números de linha nativamente em Markdown. Porém, sites de documentação como MkDocs com pymdownx.superfences suportam via extensões:

```markdown
<!-- MkDocs com pymdownx.superfences + pymdownx.highlight -->
```python linenums="1"
def main():
    print("Olá!")

if __name__ == "__main__":
    main()
```
```

---

## Destacando Linhas Específicas

Alguns renderizadores (MkDocs, Docusaurus) permitem destacar linhas dentro de blocos de código:

```markdown
<!-- Sintaxe MkDocs/Docusaurus para destacar linhas 2-3 -->
```python hl_lines="2 3"
def conectar(host, porta):
    conexao = criar_conexao(host, porta)  # linha destacada
    conexao.autenticar()                  # linha destacada
    return conexao
```
```

**Compatibilidade:** Esta syntaxe é específica de extensões e não funciona no GitHub ou GitLab padrão.

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Sempre especificar a linguagem -->
```python
print("Olá!")
```

<!-- Código inline para referências curtas no texto -->
Use o método `render()` para gerar a saída.

<!-- Blocos cercados (não indentados) como padrão -->
<!-- Diff para mostrar alterações entre versões -->
<!-- Indentação adequada quando código está dentro de listas -->
```

### Evitar

```markdown
<!-- Código sem linguagem especificada -->
```
algum código aqui
```

<!-- Código inline para trechos longos (mais que ~40 caracteres) -->
Use `const resultado = calcularSomaDosTotalsDosItensDoCarrinho(itens)` para obter o valor.

<!-- Código indentado quando cercado está disponível -->
    print("Olá!")     <!-- sem realce de sintaxe -->
```

---

## Referências

- [CommonMark Spec — Fenced Code Blocks](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) — Especificação oficial
- [GitHub Docs — Code Blocks](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks) — Suporte de realce de sintaxe no GitHub
- [GitLab Docs — Code Blocks](https://docs.gitlab.com/ee/user/markdown.html#code-spans-and-blocks) — Blocos de código no GitLab
- [Highlight.js — Linguagens Suportadas](https://highlightjs.org/static/demo/) — Lista de linguagens com realce
