# Contributing to Hefesto Skill Generator

> **Obrigado por considerar contribuir com o Hefesto!** Este documento define as diretrizes para contribuição.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Governance Model](#governance-model)

---

## Code of Conduct

Este projeto adere ao [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). Ao participar, espera-se que você siga este código. Por favor, reporte comportamentos inaceitáveis para os mantenedores do projeto.

---

## How Can I Contribute?

### 1. Reportar Bugs

Antes de criar um bug report:
- **Verifique** se o bug já foi reportado nas [Issues](../../issues)
- **Verifique** a documentação em `docs/` e `.context/`
- **Use** o template de issue apropriado

Inclua no report:
- **Versão do Hefesto** (`MEMORY.md` linha 4)
- **CLIs instalados** (output de `/hefesto.detect`)
- **Sistema operacional** e versão
- **Passos para reproduzir** o problema
- **Comportamento esperado** vs **comportamento atual**
- **Logs/screenshots** se aplicável

### 2. Sugerir Features

Antes de propor uma feature:
- **Verifique** se já existe em [CARDs](docs/cards/) ou [Issues](../../issues)
- **Leia** o [CONSTITUTION.md](./CONSTITUTION.md) (regras T0)
- **Revise** a [arquitetura](docs/ARCHITECTURE.md)

Inclua na proposta:
- **Problema** que a feature resolve
- **Solução proposta** (descritiva)
- **Alternativas consideradas**
- **Impacto** em T0 rules e compatibilidade CLI

### 3. Contribuir com Código

- **Fork** o repositório
- **Crie** um branch para sua feature (`git checkout -b feature/nome-descritivo`)
- **Siga** os padrões de código (veja abaixo)
- **Escreva** testes para sua mudança
- **Rode** todos os testes antes de commitar
- **Commit** com mensagens convencionais (veja abaixo)
- **Envie** um Pull Request

### 4. Melhorar Documentação

Documentação é crucial! Contribuições para:
- Correção de typos e clareza em `README.md`, `docs/`, `.context/`
- Exemplos de uso em `.context/examples/`
- Troubleshooting em `.context/troubleshooting/`

---

## Development Setup

### Pré-requisitos

- **Python 3.9+** (para scripts de validação)
- **Node.js 18+** (se usar CLIs como Codex)
- **Git** para controle de versão
- **Pelo menos 1 CLI de IA** instalado (Claude, Gemini, OpenCode, etc.)

### Clone e Setup

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/hefesto-skill-generator.git
cd hefesto-skill-generator

# Verifique T0 rules
cat CONSTITUTION.md

# Rode detecção de CLIs
# (via seu CLI de IA preferido)
/hefesto.detect

# Valide uma skill existente para testar
/hefesto.validate java-fundamentals
```

### Estrutura do Projeto

```
hefesto-skill-generator/
├── CONSTITUTION.md           # T0 rules (NUNCA violar)
├── MEMORY.md                 # Estado atual do projeto
├── AGENTS.md                 # Bootstrap para IAs
├── .context/                 # Contexto para IAs
│   ├── standards/            # T0/T1 rules expandidas
│   ├── patterns/             # Padrões de design
│   └── examples/             # Exemplos de código
├── docs/                     # Documentação para humanos
│   ├── cards/                # CARDs de implementação
│   └── specs/                # Especificações detalhadas
├── commands/                 # Implementação de comandos /hefesto.*
├── templates/                # Templates de skills
└── .opencode/skills/         # Skills de demonstração
```

---

## Coding Standards

### Conventional Commits

Use mensagens de commit seguindo [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona comando /hefesto.extend para skills existentes
fix: corrige validação de frontmatter em skills com metadata JIT
docs: atualiza README com feature Multi-CLI Parallel Generation
test: adiciona testes para rollback atomico em multi-cli
refactor: extrai logica de deteccao CLI para modulo separado
chore: atualiza dependencias de validacao Agent Skills spec
```

**Formato:**
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação apenas
- `test`: Adicionar/modificar testes
- `refactor`: Refatoração sem mudar comportamento
- `chore`: Manutenção (deps, config, etc.)
- `perf`: Melhoria de performance

### Python Code Style

```python
# CORRETO - PEP 8, type hints, docstrings
def validate_skill_frontmatter(skill_path: str) -> bool:
    """
    Valida frontmatter YAML contra Agent Skills spec.
    
    Args:
        skill_path: Caminho absoluto para SKILL.md
        
    Returns:
        True se frontmatter válido, False caso contrário
        
    Raises:
        FileNotFoundError: Se skill_path não existe
    """
    # Implementation...
    pass

# PROIBIDO - sem types, sem docstring
def validate(path):
    # Implementation...
    pass
```

**Regras:**
- **PEP 8** compliance (use `black` formatter)
- **Type hints** obrigatórios
- **Docstrings** para funções públicas (Google style)
- **Max line length**: 100 chars
- **Imports**: grouped (stdlib, 3rd-party, local)

### Markdown Documentation

```markdown
# CORRETO - Headers hierárquicos, código fenced

## Seção Principal

Texto descritivo claro.

### Subseção

```bash
# Exemplo de comando
/hefesto.create "skill description"
```

# PROIBIDO - Headers sem hierarquia, código sem syntax highlight

### Titulo (sem ## anterior)

Comando sem fence:
/hefesto.create "skill"
```

**Regras:**
- **CommonMark** compliant (veja `.opencode/skills/markdown-fundamentals/`)
- **Títulos**: hierarquia correta (H1 → H2 → H3)
- **Código**: sempre usar fenced blocks com syntax highlight
- **Links**: relativos para arquivos locais, absolutos para externos
- **Tabelas**: usar para dados estruturados (GFM style)

### T0 Rules Compliance

**CRÍTICO:** Toda contribuição DEVE seguir [CONSTITUTION.md](./CONSTITUTION.md) T0 rules:

| T0 Rule | Checklist |
|---------|-----------|
| T0-HEFESTO-01 | ✅ Skill segue [agentskills.io](https://agentskills.io) |
| T0-HEFESTO-02 | ✅ Human Gate antes de persistir |
| T0-HEFESTO-03 | ✅ SKILL.md < 500 linhas |
| T0-HEFESTO-04 | ✅ Detecta CLIs antes de perguntar |
| T0-HEFESTO-05 | ✅ Armazena em projeto local |
| T0-HEFESTO-06 | ✅ Valida contra spec antes de persistir |
| T0-HEFESTO-07 | ✅ Nome lowercase, hyphens, max 64 chars |
| T0-HEFESTO-08 | ✅ Operações idempotentes |
| T0-HEFESTO-09 | ✅ Compatível com 7 CLIs |
| T0-HEFESTO-10 | ✅ Cita ≥2 fontes (skills técnicas) |
| T0-HEFESTO-11 | ✅ Segurança por padrão (sanitização) |

**Violação de T0 rule = PR rejeitado automaticamente.**

---

## Testing Guidelines

### Tipos de Testes

1. **Unit Tests** (Python)
   ```bash
   # Rodar testes unitários (quando disponíveis)
   pytest tests/unit/
   ```

2. **Integration Tests** (CLIs)
   ```bash
   # Testar comandos manualmente via CLI de IA
   /hefesto.create "test skill"
   /hefesto.validate test-skill
   ```

3. **Validation Tests** (Specs)
   ```bash
   # Validar contra Agent Skills spec
   /hefesto.validate <skill-name>
   ```

### Test Coverage

- **Novas features**: Devem incluir testes (mínimo 80% coverage)
- **Bug fixes**: Devem incluir teste de regressão
- **Documentação**: Exemplos devem ser testáveis

### Manual Testing Checklist

Antes de submeter PR, teste manualmente:

```markdown
- [ ] `/hefesto.detect` - Detecta CLIs corretamente
- [ ] `/hefesto.create` - Cria skill válida
- [ ] `/hefesto.validate` - Valida contra T0 rules
- [ ] Human Gate - Apresenta preview antes de persistir
- [ ] Multi-CLI - Gera para todos CLIs detectados
- [ ] Rollback - Reverte em caso de erro parcial
- [ ] Skill gerada é carregável pelo CLI de IA
```

---

## Pull Request Process

### 1. Antes de Abrir o PR

- [ ] **Branch atualizado** com `main`
- [ ] **Testes passando** (unit + integration)
- [ ] **Conventional commits** aplicados
- [ ] **Documentação atualizada** (se aplicável)
- [ ] **T0 rules validadas** (todas 11)
- [ ] **Self-review** feito (leia seu próprio diff)

### 2. Template de PR

Use o template `.github/pull_request_template.md` (será criado). Inclua:

```markdown
## Descrição

[Descrição clara da mudança]

## Tipo de Mudança

- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix ou feature que quebra compatibilidade)
- [ ] Documentação

## Checklist T0

- [ ] T0-HEFESTO-01: Agent Skills Standard
- [ ] T0-HEFESTO-02: Human Gate
- [ ] T0-HEFESTO-03: Progressive Disclosure (<500 linhas)
- [ ] ... (todas as 11 regras)

## Testes

- [ ] Unit tests adicionados/atualizados
- [ ] Testes manuais via `/hefesto.*` commands
- [ ] Validação contra Agent Skills spec

## Screenshots/Logs

[Se aplicável]
```

### 3. Review Process

1. **CI passa** (quando configurado)
2. **Pelo menos 1 aprovação** de mantenedor
3. **Conflitos resolvidos** com `main`
4. **Discussão de feedback** (se houver)
5. **Merge** via squash ou rebase (decidido por mantenedor)

### 4. Após Merge

- Branch será deletado automaticamente
- Se feature for grande, adicionada ao `MEMORY.md` session log
- Se quebra compatibilidade, adicionada ao `RELEASE-NOTES.md`

---

## Issue Guidelines

### Templates Disponíveis

Use os templates em `.github/ISSUE_TEMPLATE/`:

1. **bug_report.md** - Para reportar bugs
2. **feature_request.md** - Para sugerir features
3. **question.md** - Para dúvidas gerais

### Labels

| Label | Uso |
|-------|-----|
| `bug` | Algo não funciona conforme esperado |
| `feature` | Nova funcionalidade proposta |
| `documentation` | Melhorias na documentação |
| `good first issue` | Bom para iniciantes |
| `help wanted` | Mantenedores precisam de ajuda |
| `T0-violation` | Viola regra T0 (crítico) |
| `CLI-specific` | Relacionado a CLI específico (claude, gemini, etc.) |

### Priorização

- **P0 (Crítico)**: Violação T0, bloqueador de releases
- **P1 (Alta)**: Bugs graves, features core faltando
- **P2 (Média)**: Melhorias, bugs não-críticos
- **P3 (Baixa)**: Nice-to-have, otimizações

---

## Governance Model

### Modelo: Ditador Benevolente (Fase Inicial)

Dado que o projeto está em **LTS v1.0.0** (inicial), adotamos o modelo **Ditador Benevolente**:

- **Decisões finais**: Tomadas pelo criador/mantenedor principal
- **Contribuições**: Bem-vindas via PR com review obrigatório
- **Roadmap**: Definido via CARDs em `docs/cards/`

### Futuro: Meritocracia (v2.0.0+)

Quando a comunidade crescer:
- **Contribuidores frequentes** ganham commit access
- **Decisões técnicas** via consenso ou voto (3+ contribuidores ativos)
- **Roadmap** co-criado via discussões públicas

### Comunicação

- **Issues**: Bugs, features, perguntas
- **Discussions** (futuro): Ideias, RFC, help
- **Email**: Para questões privadas (Code of Conduct violations)

---

## Recursos Adicionais

| Recurso | Link |
|---------|------|
| **Agent Skills Spec** | https://agentskills.io |
| **Conventional Commits** | https://www.conventionalcommits.org/ |
| **PEP 8** | https://peps.python.org/pep-0008/ |
| **CommonMark** | https://commonmark.org/ |
| **Contributor Covenant** | https://www.contributor-covenant.org/ |
| **Architecture** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **T0 Rules** | [CONSTITUTION.md](./CONSTITUTION.md) |
| **Current State** | [MEMORY.md](./MEMORY.md) |

---

## Contato

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions) *(futuro)*
- **Email**: *(adicionar se aplicável)*

---

**Obrigado por contribuir com Hefesto!** 🔥

Juntos, estamos forjando ferramentas que empoderam agentes de IA.

---

**CONTRIBUTING.md** | Hefesto Skill Generator | v1.0.0-LTS | 2026-02-05
