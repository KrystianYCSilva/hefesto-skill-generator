# Hierarquia de Headings em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Estrutura de Headings H1–H6, Outline do Documento, Acessibilidade, SEO

---

## Overview

Os headings são o elemento mais importante para estrutura e navegação em documentos Markdown. Seguir uma hierarquia consistente é fundamental para acessibilidade (leitores de tela), SEO (otimização para motores de busca) e usabilidade geral do documento.

**Princípio central:** Um documento deve ter exatamente um H1, e a hierarquia deve ser sequencial — nunca saltar níveis (H1 → H3 sem H2 intermediário).

---

## Níveis de Heading

### H1 — Título do Documento

O H1 é o título principal. Deve haver apenas **um** por documento.

```markdown
# Título do Documento
```

**Quando usar:**
- Como primeira linha de conteúdo (após front matter, se houver)
- Para identificar o tema central do documento

**Evitar:**
- Usar mais de um H1 no mesmo arquivo
- Usar H1 apenas por estética (negrito grande)

### H2 — Seções Principais

H2 divide o documento em seções de primeiro nível. São os equivalentes aos capítulos.

```markdown
## Instalação

## Uso

## Configuração

## Troubleshooting
```

**Boas práticas:**
- Manter entre 3 e 8 seções H2 por documento
- Usar nomes descritivos e acionáveis
- Cada H2 deve ser suficiente para entender o conteúdo sem contexto externo

### H3 — Subseções

H3 detalha uma seção H2. Sempre deve estar sob um H2.

```markdown
## Instalação

### Pré-requisitos

### Via npm

### Via Homebrew
```

### H4 — Detalhes

H4 é usado para detalhamento adicional dentro de uma subseção H3. Usar com moderação.

```markdown
### Via npm

#### Instalação global

#### Instalação local no projeto
```

### H5 e H6 — Níveis Profundos

H5 e H6 são raramente necessários. Se você precisar de mais de 4 níveis de hierarquia, considere dividir o documento em múltiplos arquivos.

```markdown
#### Configuração avançada

##### Opções de timeout

###### Valores padrão por ambiente
```

**Regra geral:** Se você está usando H5 ou H6, provavelmente o documento precisa ser dividido.

---

## Outline do Documento

O outline é a estrutura de navegação gerada pelos headings. Muitos renderizadores (GitHub, GitLab, docs sites) geram uma tabela de conteúdo automática a partir dos headings.

### Exemplo de Outline Bem Estruturado

```markdown
# Guia de API REST

## Autenticação
### Token Bearer
### OAuth 2.0

## Endpoints
### Usuários
#### Listar usuários
#### Criar usuário
### Produtos
#### Listar produtos
#### Criar produto

## Tratamento de Erros
### Códigos HTTP
### Formato da Resposta de Erro

## Exemplos
```

Este outline gera uma navegação clara e lógica. Cada nível adiciona detalhe sem repetição.

### Exemplo de Outline Incorreto

```markdown
# Guia de API REST

### Autenticação          <!-- ERRO: H3 sem H2 pai -->
## Token Bearer           <!-- ERRO: H2 como filho de H3 -->
#### Scopes               <!-- ERRO: H4 sem H3 pai -->
```

---

## Acessibilidade

Os headings são críticos para acessibilidade, especialmente para usuários que dependem de leitores de tela.

### Regras de Acessibilidade (WCAG 2.1)

- **Estrutura lógica:** Headings devem refletir a estrutura real do conteúdo, não ser usados apenas para formatação visual
- **Sem saltos de nível:** A sequência deve ser H1 → H2 → H3, nunca H1 → H3
- **Headings descritivos:** Cada heading deve ser compreensível fora do contexto da página
- **Não usar headings vazios:** `##` sem texto é inválido

### Exemplos de Compliance

```markdown
<!-- CORRETO: Heading descritivo e sequencial -->
## Como Instalar o Pacote

<!-- EVITAR: Vago e não descritivo -->
## Mais Informações

<!-- EVITAR: Heading usado apenas como formatação -->
## ────────────────────
```

### Leitores de Tela e Navegação

Leitores de tela permitem aos usuários navegar diretamente entre headings. Um outline bem estruturado transforma o documento em um mapa navegável.

```markdown
<!-- Usuário leitor de tela ouve: -->
<!-- "Nível 1: Documentação do Projeto" -->
<!-- "Nível 2: Instalação" -->
<!-- "Nível 3: Requisitos do Sistema" -->
<!-- "Nível 2: Uso Básico" -->
```

---

## SEO (Otimização para Motores de Busca)

Embora Markdown em repositórios não seja diretamente indexado como sites, documentações geradas (MkDocs, Docusaurus, Jekyll) são indexadas pelos motores de busca.

### Práticas de SEO para Headings

1. **H1 deve conter a palavra-chave principal** do documento
2. **H2 e H3 devem usar variações** da palavra-chave
3. **Sem keyword stuffing:** Não repita palavras-chave artificialmente
4. **Headings únicos:** Cada heading no documento deve ser diferente

```markdown
<!-- CORRETO: Keyword natural -->
# Instalação do Framework X

## Instalação via npm
## Instalação via Docker
## Configuração Inicial

<!-- EVITAR: Keyword stuffing -->
# Framework X Instalação Framework X
## Framework X npm Instalação
```

### Estrutura para Documentação Pública

Quando a documentação será indexada, estruture pensando na busca:

```markdown
# Como usar a API de Pagamentos

## Autenticação da API de Pagamentos
### Obtendo o Token de API

## Criando um Pagamento
### Parâmetros Obrigatórios
### Exemplo de Requisição

## Consultando Status do Pagamento
```

Cada H2 pode ser uma página de busca por si só.

---

## Convenções por Plataforma

### GitHub e GitLab

- Geram Table of Contents automática a partir dos headings
- Heading IDs são gerados automaticamente (lowercase, espaços → hífens)
- Caracteres especiais são removidos do ID

```markdown
## Instalação e Configuração
<!-- ID gerado: instalação-e-configuração (GitHub) -->
<!-- ID gerado: instalacao-e-configuracao (GitLab, sem acentos) -->
```

### MkDocs / Docusaurus

- Suportam yet another anchor generation
- Permitem personalização de IDs via extensões
- Geram sidebar automática a partir dos headings

```markdown
## Seção Principal {#custom-id}
<!-- ID personalizado: custom-id -->
<!-- Suportado em: MkDocs com extensão toc, Jekyll com kramdown -->
```

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Um único H1 por documento -->
# Título Único e Descritivo

<!-- Hierarquia sequencial -->
## Seção
### Subseção
#### Detalhe

<!-- Headings descritivos e acionáveis -->
## Como Configurar o Ambiente Local
### Instalando as Dependências
```

### Evitar

```markdown
<!-- Múltiplos H1 -->
# Título 1
# Título 2

<!-- Saltos de hierarquia -->
# Título
### Subseção sem H2  <!-- ERRO -->

<!-- Headings para formatação visual -->
## ─────────────
## ...

<!-- Headings vazios ou genéricos -->
##
## Detalhes
## Mais
```

---

## Referências

- [CommonMark Spec — Headings](https://spec.commonmark.org/0.31.2/#atx-headings) — Especificação oficial de headings ATX e Setext
- [WCAG 2.1 — Heading Structure](https://www.w3.org/WAI/WCAG21/Techniques/html/H42.html) — Boas práticas de acessibilidade
- [GitHub Docs — Heading Anchors](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#headings-1) — Como GitHub gera IDs de headings
