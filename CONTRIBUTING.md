# Contributing to Hefesto Skill Generator

> **Obrigado por considerar contribuir com o Hefesto!**

---

## Code of Conduct

Este projeto adere ao [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md).

---

## How Can I Contribute?

### 1. Reportar Bugs

- **Verifique** se o bug ja foi reportado nas [Issues](../../issues)
- **Inclua**: versao do Hefesto (`.hefesto/version`), CLIs instalados, SO, passos para reproduzir

### 2. Sugerir Features

- **Leia** o [CONSTITUTION.md](./CONSTITUTION.md) (regras T0)
- **Revise** a [arquitetura](docs/ARCHITECTURE.md)
- **Inclua**: problema, solucao proposta, impacto em T0 rules

### 3. Contribuir com Codigo

- **Fork** o repositorio
- **Crie** um branch (`git checkout -b feature/nome-descritivo`)
- **Siga** os padroes abaixo
- **Envie** um Pull Request

### 4. Melhorar Documentacao

Contribuicoes para `README.md`, `docs/`, `.context/` sao bem-vindas.

---

## Development Setup

### Pre-requisitos

- **Bash 3.2+** (Unix) ou **PowerShell 5.1+** (Windows) - para rodar o installer
- **Git** para controle de versao
- **Pelo menos 1 CLI de IA** instalado (Claude, Gemini, Codex, etc.)

### Clone e Setup

```bash
git clone https://github.com/seu-usuario/hefesto-skill-generator.git
cd hefesto-skill-generator

# Rode o init para verificar status
/hefesto.init

# Valide uma skill para testar
/hefesto.validate java-fundamentals
```

### Estrutura do Projeto

```
hefesto-skill-generator/
  CONSTITUTION.md           # T0 rules (NUNCA violar)
  AGENTS.md                 # Bootstrap para IAs
  README.md                 # Documentacao principal
  templates/                # Templates fonte (fonte de verdade)
    skill-template.md
    quality-checklist.md
    cli-compatibility.md
  installer/                # Pacote distribuivel
    install.sh / install.ps1
    payload/
  .<cli>/commands/           # 5 comandos hefesto.* por CLI
  .<cli>/skills/             # Skills de demonstracao
  .github/workflows/        # CI/CD
  docs/                     # Documentacao
  .context/                 # Contexto para IAs
```

---

## Coding Standards

### Conventional Commits

```
feat: adiciona comando /hefesto.extend
fix: corrige validacao de frontmatter
docs: atualiza README com instrucoes de instalacao
refactor: simplifica deteccao de CLI no installer
chore: sincroniza payload com comandos fonte
```

### Markdown Documentation

- **CommonMark** compliant
- **Titulos**: hierarquia correta (H1 -> H2 -> H3)
- **Codigo**: sempre usar fenced blocks com syntax highlight
- **Links**: relativos para arquivos locais

### T0 Rules Compliance

**Toda contribuicao DEVE seguir** [CONSTITUTION.md](./CONSTITUTION.md) T0 rules. Violacao = PR rejeitado.

---

## Testing

### Manual Testing Checklist

```
- [ ] /hefesto.init - Detecta CLIs corretamente
- [ ] /hefesto.create - Cria skill valida
- [ ] /hefesto.validate - Valida e oferece fix-auto
- [ ] Human Gate - Apresenta preview antes de persistir
- [ ] Multi-CLI - Gera para todos CLIs detectados
- [ ] Skill gerada e carregavel pelo CLI
```

---

## Pull Request Process

1. Branch atualizado com `main`
2. Conventional commits
3. T0 rules validadas
4. Documentacao atualizada (se aplicavel)
5. Self-review feito

---

## Governance

Modelo **Ditador Benevolente** (fase inicial):
- Decisoes finais pelo mantenedor principal
- Contribuicoes via PR com review obrigatorio

---

| Recurso | Link |
|---------|------|
| Agent Skills Spec | https://agentskills.io |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| T0 Rules | [CONSTITUTION.md](./CONSTITUTION.md) |

---

**CONTRIBUTING.md** | Hefesto Skill Generator v2.0.0
