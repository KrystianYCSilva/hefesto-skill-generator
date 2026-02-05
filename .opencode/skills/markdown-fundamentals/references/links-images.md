# Links e Imagens em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Links Inline, Relativos, Estilo Referência, Imagens, Badges

---

## Overview

Links e imagens são elementos centrais da documentação Markdown. Dominar os diferentes estilos de link (inline, referência, relativos) e técnicas de imagem (badges, redimensionamento, imagens clicáveis) permite criar documentação profissional e navegável.

---

## Links Inline

A sintaxe básica e mais comum para links.

```markdown
<!-- Link básico -->
[texto visível](https://exemplo.com)

<!-- Link com título (tooltip ao hover) -->
[documentação oficial](https://docs.exemplo.com "Guia completo")

<!-- Link com âncore interno à página -->
[ver instalação](#instalação)

<!-- Link que abre em nova aba (HTML necessário) -->
<a href="https://exemplo.com" target="_blank" rel="noopener">abrir em nova aba</a>
```

### Links com Caracteres Especiais

```markdown
<!-- Parênteses na URL: escapar com %28 e %29 -->
[página Wikipedia](https://en.wikipedia.org/wiki/Kotlin_(programming_language))

<!-- URL com espaços: usar %20 ou encode completo -->
[arquivo com espaço](https://exemplo.com/meu%20arquivo.pdf)

<!-- Caracteres especiais no texto: usar backslash -->
[texto com \[colchetes\]](https://exemplo.com)
```

---

## Links Relativos

Links relativos são essenciais para navegação dentro de repositórios e documentação multi-arquivo.

### Estrutura de Diretórios

```
projeto/
├── README.md
├── docs/
│   ├── instalação.md
│   ├── uso.md
│   └── avançado/
│       └── configuração.md
├── src/
│   └── main.py
└── CHANGELOG.md
```

### Exemplos de Caminhos Relativos

```markdown
<!-- De README.md para docs/instalação.md -->
[Como instalar](docs/instalação.md)

<!-- De docs/uso.md para docs/instalação.md (mesmo nível) -->
[voltar à instalação](instalação.md)

<!-- De docs/avançado/configuração.md para docs/uso.md (um nível acima) -->
[uso básico](../uso.md)

<!-- De docs/uso.md para README.md (diretório raiz) -->
[README principal](../README.md)

<!-- Link para arquivo de código fonte -->
[ver código fonte](../src/main.py)

<!-- Link para linha específica de um arquivo -->
[ver função principal](../src/main.py#L42)

<!-- Link para range de linhas (GitHub) -->
[ver classe Config](../src/config.py#L10-L35)
```

### Boas Práticas com Links Relativos

```markdown
<!-- CORRETO: caminho relativo limpo -->
[instalação](docs/instalação.md)

<!-- EVITAR: caminho absoluto desnecessário -->
[instalação](/projeto/docs/instalação.md)

<!-- EVITAR: caminho com ../ excessivo — considere reorganizar -->
[referência](../../../docs/ref/api.md)
```

---

## Links de Estilo Referência

Estilo referência mantém o texto mais limpo quando há muitos links, especialmente em textos densos.

```markdown
<!-- No corpo do texto: usar a referência -->
Para mais informações, consulte a [documentação oficial][docs]
e o [guia de instalação][install].

<!-- No final do documento (ou na seção relevante): definir as referências -->
[docs]: https://docs.exemplo.com
[install]: https://docs.exemplo.com/install "Guia de Instalação"
```

### Referência Implícita

```markdown
<!-- Quando o texto do link é igual ao ID da referência -->
Visite o [GitHub] para ver o código fonte.

[GitHub]: https://github.com
```

### Quando Usar Estilo Referência

```markdown
<!-- USAR estilo referência quando: -->
<!-- 1. Mesmo link aparece múltiplas vezes -->
Consulte a [documentação][docs] na seção de instalação.
Para configuração avançada, veja também a [documentação][docs].

[docs]: https://docs.exemplo.com

<!-- 2. Texto é denso e links prejudicam leitura -->
O protocolo [OAuth 2.0][oauth] utiliza [tokens de acesso][tokens]
que são renovados periodicamente via [refresh tokens][refresh].

[oauth]: https://tools.ietf.org/html/rfc6749
[tokens]: https://tools.ietf.org/html/rfc6750
[refresh]: https://tools.ietf.org/html/rfc6749#section-6
```

---

## Autolinks

Autolinks reconhecem URLs automaticamente em certas plataformas.

```markdown
<!-- Sintaxe explícita com angle brackets (CommonMark) -->
<https://exemplo.com>
<mailto:contato@exemplo.com>

<!-- GFM: URLs são linkadas automaticamente sem angle brackets -->
Visite https://exemplo.com para mais informações.
<!-- Renderiza como link clicável no GitHub -->

<!-- Menções e referências automáticas (GitHub) -->
Corrigido pelo @usuario em #42
```

---

## Imagens

### Sintaxe Básica

```markdown
<!-- Imagem básica -->
![texto alternativo](caminho/para/imagem.png)

<!-- Imagem com título -->
![logo do projeto](assets/logo.png "Logo oficial")

<!-- Imagem remota -->
![screenshot](https://cdn.exemplo.com/screenshot.png)
```

### Alt Text — Acessibilidade

O texto alternativo é crítico para acessibilidade. Descreva o que a imagem mostra.

```markdown
<!-- CORRETO: Alt text descritivo -->
![Diagrama mostrando o fluxo de autenticação entre cliente e servidor](diagrams/auth-flow.png)

<!-- EVITAR: Alt text vazio ou genérico -->
![imagem](screenshot.png)
![](logo.png)
```

### Redimensionamento de Imagens

CommonMark não suporta redimensionamento nativo. Soluções por plataforma:

```markdown
<!-- GitHub: usar HTML img tag -->
<img src="logo.png" alt="Logo" width="200">
<img src="logo.png" alt="Logo" width="100" height="100">

<!-- MkDocs com extensão attr_list -->
![Logo](logo.png){ width="200" }

<!-- Jekyll/Kramdown -->
![Logo](logo.png){: width="200px" }
```

### Imagens Clicáveis

```markdown
<!-- Imagem que funciona como link -->
[![Alt text](imagem.png)](https://destino.com)

<!-- Exemplo prático: badge clicável -->
[![CI Status](https://img.shields.io/github/actions/workflow/status/usuario/repo/ci.yml)](https://github.com/usuario/repo/actions)
```

---

## Badges

Badges são pequenas imagens geradas dinamicamente, muito comuns em READMEs.

### Shields.io — Badges Populares

```markdown
<!-- Licença -->
[![Licença](https://img.shields.io/badge/licença-MIT-brightgreen)](LICENSE)

<!-- Versão do projeto -->
[![Versão](https://img.shields.io/badge/versão-1.2.0-blue)](CHANGELOG.md)

<!-- CI/CD Status (GitHub Actions) -->
[![CI](https://img.shields.io/github/actions/workflow/status/usuario/repo/ci.yml?label=CI)](https://github.com/usuario/repo/actions)

<!-- Cobertura de testes -->
[![Cobertura](https://img.shields.io/codecov/c/github/usuario/repo?label=cobertura)](https://codecov.io/gh/usuario/repo)

<!-- Stars do repositório -->
[![Stars](https://img.shields.io/github/stars/usuario/repo?style=social)](https://github.com/usuario/repo)

<!-- Downloads por mês (npm) -->
[![Downloads](https://img.shields.io/npm/dm/pacote-nome)](https://www.npmjs.com/package/pacote-nome)
```

### Badges Estáticos Customizados

```markdown
<!-- Badge estático com cor customizada -->
<!-- Sintaxe: https://img.shields.io/badge/LABEL-MESSAGE-COLOR -->
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)](.)
[![Plataforma](https://img.shields.io/badge/plataforma-linux%20|%20mac%20|%20windows-lightgrey)](.)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green)](.)
```

### Organização de Badges

```markdown
# Meu Projeto

<!-- Grupo 1: Status do projeto -->
[![CI](https://img.shields.io/github/actions/workflow/status/usuario/repo/ci.yml)](https://github.com/usuario/repo/actions)
[![Cobertura](https://img.shields.io/codecov/c/github/usuario/repo)](https://codecov.io/gh/usuario/repo)

<!-- Grupo 2: Metadados -->
[![Versão](https://img.shields.io/npm/v/pacote)](https://www.npmjs.com/package/pacote)
[![Licença](https://img.shields.io/badge/licença-MIT-brightgreen)](LICENSE)

<!-- Grupo 3: Social -->
[![Stars](https://img.shields.io/github/stars/usuario/repo?style=social)](https://github.com/usuario/repo)
```

---

## Prevenção de Links Quebrados

Links quebrados prejudicam a usabilidade e a credibilidade da documentação.

### Checklist de Verificação

- [ ] Todos os links relativos apontam para arquivos que existem
- [ ] Âncore internos (`#seção`) correspondem aos headings existentes
- [ ] Links externos foram testados recentemente
- [ ] Imagens referenciadas existem no caminho especificado
- [ ] Links para linhas específicas de código não são muito frágeis (mudanças de código quebram)

### Ferramentas de Verificação

```markdown
<!-- Verificar links relativos no repositório -->
<!-- GitHub: use bots como linkcheck ou markdown-link-check -->
<!-- MkDocs: npm install -g markdown-link-check -->
<!-- Ex: markdown-link-check README.md -->

<!-- Para CI/CD, use GitHub Actions: -->
<!-- - uses: gaucel/linkcheck@main -->
```

### Estratégia para Links Estáveis

```markdown
<!-- PREFIRA: links para tags/releases ao invés de branches -->
<!-- EVITAR -->
[código fonte](https://github.com/usuario/repo/blob/main/src/main.py)

<!-- PREFERIR: permalink com commit hash ou tag -->
[código fonte](https://github.com/usuario/repo/blob/v1.2.0/src/main.py)
```

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Links relativos para navegação interna -->
[próxima seção](./uso.md)

<!-- Alt text descritivo em imagens -->
![Fluxo de autenticação OAuth 2.0](diagrams/oauth-flow.png)

<!-- Estilo referência para links repetidos -->
Consulte a [documentação][docs] e os [exemplos][exemplos].
[docs]: https://docs.exemplo.com
[exemplos]: https://docs.exemplo.com/exemplos
```

### Evitar

```markdown
<!-- Links com texto genérico "aqui" -->
Para mais informações, clique aqui.  <!-- onde está "aqui"? -->

<!-- Alt text vazio -->
![](imagem.png)

<!-- URLs cruas no meio do texto (sem link formatado) -->
Acesse https://docs.exemplo.com/very/long/path/to/resource para ver.
```

---

## Referências

- [CommonMark Spec — Links](https://spec.commonmark.org/0.31.2/#links) — Especificação de links inline e referência
- [CommonMark Spec — Images](https://spec.commonmark.org/0.31.2/#images) — Especificação de imagens
- [Shields.io](https://shields.io/) — Gerador de badges
- [GitHub Docs — Links](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links) — Links no GitHub Markdown
