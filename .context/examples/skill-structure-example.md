# Exemplo: Estrutura de Skill - Code Review

> **Tier:** T3 - Ilustrativo
> **Proposito:** Demonstrar estrutura correta de uma skill Agent Skills

---

## 1. Estrutura de Diretorios

```
code-review/
├── SKILL.md              # Core (87 linhas)
├── scripts/
│   └── analyze.py        # Script de analise
├── references/
│   ├── REFERENCE.md      # Docs detalhadas
│   └── CHECKLIST.md      # Checklist de review
└── assets/
    └── templates/
        └── review-report.md
```

---

## 2. SKILL.md (Core)

```yaml
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas SOLID e Clean Code.
  Use quando: revisar PRs, avaliar codigo de terceiros, onboarding de novos devs.
license: MIT
compatibility: Claude Code, Gemini CLI, Codex, OpenCode, Cursor, Qwen Code, VS Code/Copilot
metadata:
  author: hefesto-examples
  version: "1.0.0"
  created: 2026-02-04
  category: development
  tags: [code-review, quality, solid, clean-code, best-practices]
  validation_score: universal
---

# Code Review

> Padroniza code reviews seguindo boas praticas SOLID e Clean Code.

## When to Use

- ✅ Revisar Pull Requests antes de merge
- ✅ Avaliar codigo de terceiros (libs, integracao)
- ✅ Onboarding de novos desenvolvedores
- ✅ Auditoria de qualidade de codigo
- ✅ Preparacao para refatoracao
- ❌ Debugging de runtime (usar skill de debugging)
- ❌ Otimizacao de performance (usar skill de profiling)

## Instructions

### Step 1: Analisar Contexto

Leia o codigo alvo e identifique:
- Linguagem e framework utilizados
- Padrao arquitetural (MVC, Clean, Hexagonal, etc.)
- Presenca de testes
- Convencoes de codigo existentes

### Step 2: Aplicar Checklist SOLID

Verifique cada principio:

- **S**ingle Responsibility: Cada classe/funcao tem uma unica responsabilidade?
- **O**pen/Closed: Codigo aberto para extensao, fechado para modificacao?
- **L**iskov Substitution: Subtipos substituiveis por tipos base?
- **I**nterface Segregation: Interfaces especificas ao inves de genericas?
- **D**ependency Inversion: Depende de abstracoes, nao implementacoes?

### Step 3: Verificar Clean Code

Checklist de qualidade:
- [ ] Nomes descritivos e pronunciaveis
- [ ] Funcoes pequenas (idealmente < 20 linhas)
- [ ] Sem comentarios obvios (codigo auto-documentado)
- [ ] Sem codigo duplicado (DRY)
- [ ] Tratamento de erros adequado
- [ ] Formatacao consistente

### Step 4: Avaliar Testes

Se testes existem:
- [ ] Cobertura adequada (>= 80%)
- [ ] Testes unitarios isolados
- [ ] Nomes descritivos nos testes
- [ ] Arrange-Act-Assert pattern

Se testes NAO existem:
- Sugerir criacao de testes prioritarios
- Identificar codigo mais critico para testar

### Step 5: Gerar Relatorio

Usar template em `assets/templates/review-report.md`:

```markdown
## Code Review: [Nome do PR/Arquivo]

### Resumo
[Avaliacao geral em 2-3 linhas]

### Pontos Positivos
- [Item 1]
- [Item 2]

### Melhorias Sugeridas
| Prioridade | Item | Justificativa |
|------------|------|---------------|
| Alta | [Item] | [Por que] |
| Media | [Item] | [Por que] |

### Proximos Passos
1. [Acao 1]
2. [Acao 2]
```

## References

- [Detailed Reference](references/REFERENCE.md) - Documentacao completa dos principios
- [Checklist](references/CHECKLIST.md) - Checklist detalhado para impressao

## Scripts

- `scripts/analyze.py` - Analisa metricas basicas (complexidade, linhas, etc.)

---

**Gerado por:** Hefesto Skill Generator v1.0.0
**Ultima Atualizacao:** 2026-02-04
```

---

## 3. references/REFERENCE.md

```markdown
# Code Review - Reference Guide

## SOLID Principles (Detalhado)

### Single Responsibility Principle (SRP)

Uma classe deve ter apenas uma razao para mudar.

**Exemplo Correto:**
```java
// Responsabilidade unica: persistencia de usuario
public class UserRepository {
    public User save(User user) { ... }
    public User findById(Long id) { ... }
}

// Responsabilidade unica: validacao de usuario
public class UserValidator {
    public ValidationResult validate(User user) { ... }
}
```

**Exemplo Incorreto:**
```java
// Multiplas responsabilidades
public class UserService {
    public User save(User user) { ... }
    public void sendEmail(User user) { ... }  // Deveria estar em EmailService
    public String generateReport(User user) { ... }  // Deveria estar em ReportService
}
```

[Continua com outros principios...]

---

## Clean Code Guidelines

### Nomes Significativos

| Ruim | Bom |
|------|-----|
| `d` | `elapsedTimeInDays` |
| `list1` | `accountList` |
| `theList` | `flaggedCells` |
| `hp` | `hypotenuse` |

[Continua...]
```

---

## 4. references/CHECKLIST.md

```markdown
# Code Review Checklist

## Pre-Review
- [ ] Entendi o proposito do codigo
- [ ] Li a descricao do PR/ticket
- [ ] Ambiente local configurado (se necessario)

## Estrutura
- [ ] Arquivos no local correto
- [ ] Nomenclatura de arquivos consistente
- [ ] Imports organizados

## Codigo
- [ ] Nomes descritivos
- [ ] Funcoes pequenas
- [ ] Sem codigo duplicado
- [ ] Tratamento de erros
- [ ] Sem magic numbers/strings

## SOLID
- [ ] Single Responsibility
- [ ] Open/Closed
- [ ] Liskov Substitution
- [ ] Interface Segregation
- [ ] Dependency Inversion

## Testes
- [ ] Testes unitarios presentes
- [ ] Cobertura adequada
- [ ] Testes isolados
- [ ] Cenarios de erro cobertos

## Seguranca
- [ ] Sem credenciais hardcoded
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention

## Performance
- [ ] Sem loops desnecessarios
- [ ] Queries otimizadas
- [ ] Caching quando apropriado
```

---

## 5. scripts/analyze.py

```python
#!/usr/bin/env python3
"""
Script de analise basica de codigo.
Calcula metricas simples para auxiliar code review.
"""

import sys
import os
from pathlib import Path

def count_lines(filepath: str) -> dict:
    """Conta linhas de codigo, comentarios e em branco."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    total = len(lines)
    blank = sum(1 for l in lines if l.strip() == '')
    # Simplificado - detecta // e #
    comments = sum(1 for l in lines if l.strip().startswith(('//','#','/*','*')))
    code = total - blank - comments
    
    return {
        'total': total,
        'code': code,
        'comments': comments,
        'blank': blank
    }

def analyze_file(filepath: str) -> None:
    """Analisa um arquivo e imprime metricas."""
    metrics = count_lines(filepath)
    
    print(f"## Analise: {filepath}")
    print(f"- Total de linhas: {metrics['total']}")
    print(f"- Linhas de codigo: {metrics['code']}")
    print(f"- Comentarios: {metrics['comments']}")
    print(f"- Linhas em branco: {metrics['blank']}")
    
    # Alertas
    if metrics['code'] > 300:
        print(f"⚠️ Arquivo grande (>{300} linhas de codigo)")
    if metrics['comments'] < metrics['code'] * 0.1:
        print(f"⚠️ Poucos comentarios (<10% do codigo)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python analyze.py <arquivo>")
        sys.exit(1)
    
    analyze_file(sys.argv[1])
```

---

## 6. assets/templates/review-report.md

```markdown
# Code Review Report

**Arquivo/PR:** [NOME]
**Reviewer:** [NOME]
**Data:** [DATA]

---

## Resumo Executivo

[Avaliacao geral em 2-3 linhas]

---

## Pontos Positivos

- [Item 1]
- [Item 2]
- [Item 3]

---

## Melhorias Sugeridas

| Prioridade | Item | Arquivo:Linha | Justificativa |
|------------|------|---------------|---------------|
| 🔴 Alta | | | |
| 🟡 Media | | | |
| 🟢 Baixa | | | |

---

## Checklist

### SOLID
- [ ] Single Responsibility
- [ ] Open/Closed
- [ ] Liskov Substitution
- [ ] Interface Segregation
- [ ] Dependency Inversion

### Qualidade
- [ ] Nomes descritivos
- [ ] Funcoes pequenas
- [ ] Sem duplicacao
- [ ] Testes presentes

---

## Proximos Passos

1. [Acao prioritaria]
2. [Acao secundaria]
3. [Acao opcional]

---

## Notas Adicionais

[Comentarios livres]
```

---

## 7. Pontos-Chave do Exemplo

| Aspecto | Implementacao |
|---------|---------------|
| Frontmatter | Completo com todos campos recomendados |
| SKILL.md | 87 linhas (< 500 limite) |
| Progressive Disclosure | Docs detalhadas em references/ |
| Scripts | Utilitario em scripts/ |
| Assets | Templates em assets/ |
| Description | Acionavel com "Use quando:" |
| Instructions | Passos claros e sequenciais |
| When to Use | Inclui quando NAO usar |

---

**Ultima Atualizacao:** 2026-02-04
