# Links e Imagens em Markdown

> **Referência avançada de**: markdown-fundamentals
> **Tópico**: Links Relativos, Links Externos, Imagens, Badges, Estilo Referência, Prevenção de Links Quebrados

---

## Overview

Links e imagens são elementos fundamentais de navegação e comunicação visual em documentos Markdown. Dominar os diferentes estilos de link (inline, referência, automático) e compreender caminhos relativos são habilidades essenciais para documentação de qualidade.

---

## Links Inline

O estilo mais comum de link em Markdown.

### Sintaxe Básica

```markdown
[texto visível](URL)
```

### Exemplos

```markdown
<!-- Link externo simples -->
[Visitar o site](https://www.exemplo.com)

<!-- Link com título (tooltip ao hover) -->
[Documentação oficial](https://docs.exemplo.com "Guia completo da API")

<!-- Link para seção no mesmo documento (âncora) -->
[Ver instalação](#instalação)

<!-- Link para outro arquivo no repositório (caminho relativo) -->
[Leia as contribuições](./CONTRIBUTING.md)

<!-- Link para pasta específica -->
[Exemplos de código](./examples/)
```

---

## Links Relativos

Links relativos são essenciais para navegação dentro de repositórios e sites de documentação.

### Estrutura de Caminhos

```
projeto/
├── README.md
├── docs/
│   ├── instalacao.md
│   ├── uso.md
│   └── api/
│       └── referencia.md
├── CONTRIBUTING.md
└── LICENSE
```

### Exemplos de Caminhos Relativos

```markdown
<!-- De README.md para docs/instalacao.md -->
[Como instalar](./docs/instalacao.md)

<!-- De docs/uso.md para docs/api/referencia.md (mesmo nível pai) -->
[Referência da API](./api/referencia.md)

<!-- De docs/api/referencia.md para README.md (subir dois níveis) -->
[Voltar ao início](../../README.md)

<!-- De docs/uso.md para CONTRIBUTING.md (subir um nível) -->
[Contribuir](../CONTRIBUTING.md)

<!-- Link para seção específica em outro arquivo -->
[Seção de instalação via npm](./instalacao.md#via-npm)
```

### Caminhos Relativos vs Absolutos

```markdown
<!-- PREFERIR: Caminho relativo (funciona em forks e mirrors) -->
[Licença](./LICENSE)

<!-- EVITAR: URL absoluta do repositório (quebra em forks) -->
[Licença](https://github.com/usuario/projeto/blob/main/LICENSE)
```

---

## Links de Estilo Referência

Útil quando um mesmo link é usado em múltiplos lugares ou quando você quer manter a legibilidade do texto limpa.

### Sintaxe

```markdown
[texto visível][id-da-referência]

<!-- Definição da referência (geralmente no final do documento) -->
[id-da-referência]: URL "Título opcional"
```

### Exemplos

```markdown
Consulte a [documentação oficial][docs] e também o [guia de início rápido][quickstart]
para começar rapidamente.

Para mais detalhes, veja o [repositório no GitHub][repo].

---

[docs]: https://docs.exemplo.com/
[quickstart]: https://docs.exemplo.com/quickstart "Guia de 5 minutos"
[repo]: https://github.com/usuario/projeto
```

### Link de Referência Implícito

Quando o texto e a referência são iguais:

```markdown
Visite o [GitHub][] para mais informações.

[GitHub]: https://github.com
```

---

## Links Automáticos (Autolinks)

Em GFM, URLs e emails são automaticamente convertidos em links.

```markdown
<!-- GFM: Automático -->
Acesse https://www.exemplo.com diretamente.

<!-- CommonMark: Requer angle brackets -->
Acesse <https://www.exemplo.com> diretamente.

<!-- Email autolink -->
Contato: <contato@exemplo.com>
```

---

## Imagens

### Sintaxe Básica

```markdown
![texto alternativo](caminho-da-imagem)
```

O texto alternativo (alt text) é crucial para acessibilidade — é lido por leitores de tela.

### Exemplos

```markdown
<!-- Imagem local no repositório -->
![Diagrama da arquitetura](./docs/images/arquitetura.png)

<!-- Imagem externa -->
![Logo do projeto](https://cdn.exemplo.com/logo.png)

<!-- Imagem com título -->
![Exemplo de uso](./screenshots/exemplo.png "Tela principal do aplicativo")

<!-- Imagem com redimensionamento (GitHub/GitLab) -->
![Diagrama](./images/diagrama.png =600x)
<!-- Apenas largura: =600x -->
<!-- Apenas altura: =x400 -->
<!-- Ambos: =600x400 -->
```

### Imagem Clicável (Link com Imagem)

```markdown
<!-- Imagem que funciona como link -->
[![Badge do projeto](https://img.shields.io/badge/status-ativo-verde)](https://github.com/usuario/projeto)

<!-- Screenshot clicável que abre imagem maior -->
[![Miniatura](./screenshots/thumb.png)](./screenshots/full.png)
```

---

## Badges

Badges são pequenas imagens SVG usadas para mostrar status, versão, licença e outras informações no topo de READMEs.

### Badges Comuns com Shields.io

```markdown
<!-- Licença -->
[![Licença](https://img.shields.io/badge/licença-MIT-brightgreen.svg)](LICENSE)

<!-- Versão do pacote -->
[![Versão](https://img.shields.io/npm/v/nome-do-pacote.svg)](https://www.npmjs.com/package/nome-do-pacote)

<!-- Status do CI/CD -->
[![CI](https://github.com/usuario/projeto/actions/workflows/ci.yml/badge.svg)](https://github.com/usuario/projeto/actions/workflows/ci.yml)

<!-- Cobertura de testes -->
[![Cobertura](https://img.shields.io/codecov/c/github/usuario/projeto.svg)](https://codecov.io/gh/usuario/projeto)

<!-- Stars do repositório -->
[![Stars](https://img.shields.io/github/stars/usuario/projeto.svg?style=social)](https://github.com/usuario/projeto/stargazers)

<!-- Downloads -->
[![Downloads](https://img.shields.io/npm/dt/nome-do-pacote.svg)](https://www.npmjs.com/package/nome-do-pacote)
```

### Badge Customizada Estática

```markdown
<!-- Badge estática com cores personalizadas -->
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange.svg)](https://github.com/usuario/projeto)

<!-- Cores disponíveis: brightgreen, green, yellowgreen, yellow, orange, red, blue, purple, blueviolet, grey, lightgrey -->
```

### Organizando Badges no README

```markdown
# Nome do Projeto

[![Licença](https://img.shields.io/badge/licença-MIT-brightgreen.svg)](LICENSE)
[![Versão](https://img.shields.io/badge/versão-2.1.0-blue.svg)](CHANGELOG.md)
[![CI](https://github.com/usuario/projeto/actions/workflows/ci.yml/badge.svg)](https://github.com/usuario/projeto/actions/workflows/ci.yml)
[![Cobertura](https://img.shields.io/badge/cobertura-94%25-green.svg)](https://codecov.io/gh/usuario/projeto)

Descrição breve do projeto.
```

---

## Prevenção de Links Quebrados

Links quebrados degradam a experiência do usuário e indicam manutenção descuidada.

### Checklist de Prevenção

```markdown
<!-- 1. SEMPRE usar caminhos relativos para arquivos internos -->
[Guia](./docs/guia.md)                <!-- OK -->
<!-- [Guia](https://github.com/user/repo/blob/main/docs/guia.md) -->  <!-- EVITAR -->

<!-- 2. Verificar case-sensitivity: Linux é case-sensitive, Windows não -->
[Imagem](./Images/Foto.png)           <!-- pode falhar no Linux se o arquivo for images/foto.png -->

<!-- 3. Usar extensão de arquivo correta -->
[Documento](./docs/readme)            <!-- FALTA .md -->
[Documento](./docs/readme.md)         <!-- OK -->

<!-- 4. Para links externos, usar referência estilo referência para manutenção fácil -->
Veja a [documentação][docs] e o [changelog][cl].

[docs]: https://docs.exemplo.com/
[cl]: https://github.com/usuario/projeto/blob/main/CHANGELOG.md
```

### Ferramentas para Verificação

- **GitHub:** Links relativos são validados automaticamente na renderização
- **linkcheck (Sphinx):** Para sites de documentação gerados com Sphinx
- **markdown-link-check:** Ferramenta CLI para validar links em arquivos .md
- **GitHub Actions:** Automatizar verificação de links em CI/CD

---

## Best Practices — Resumo

### Usar

```markdown
<!-- Caminhos relativos para navegação interna -->
[Próximo passo](./proximo-passo.md)

<!-- Alt text descritivo em imagens -->
![Diagrama do fluxo de autenticação OAuth](./diagrams/auth-flow.png)

<!-- Estilo referência quando um link aparece muitas vezes -->
Consulte [aqui][docs] e [ali][docs] para mais detalhes.
[docs]: https://docs.exemplo.com/
```

### Evitar

```markdown
<!-- Links absolutos para arquivos do próprio repositório -->
[Arquivo](https://github.com/user/repo/blob/main/arquivo.md)

<!-- Alt text vazio ou genérico -->
![](./imagem.png)
!["clique aqui"](./imagem.png)

<!-- URLs sem protocolo (pode não funcionar em todos os renderizadores) -->
[Site](www.exemplo.com)              <!-- FALTA https:// -->
```

---

## Referências

- [CommonMark Spec — Links](https://spec.commonmark.org/0.31.2/#links) — Especificação oficial de links e imagens
- [GitHub Docs — Links Relativos](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links) — Como GitHub processa links relativos
- [Shields.io](https://shields.io/) — Gerador de badges customizáveis
- [WCAG 2.1 — Alt Text](https://www.w3.org/WAI/WCAG21/Techniques/html/H37.html) — Boas práticas de texto alternativo
