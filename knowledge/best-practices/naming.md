# Nomenclatura de Skills - Best Practices

## Fonte
Extraído de: `docs/pesquisa/skill-generator-automatizado.md`  
Agent Skills Spec: https://agentskills.io  
Acessado: 2026-02-05

## Resumo
Convenções de nomenclatura para skills de agentes, incluindo estrutura de identificadores, categorias semânticas e padrões de nomeação que facilitam descoberta, reutilização e manutenção. Baseado em análise de 87 papers acadêmicos e documentação oficial de CLIs.

## Princípios Fundamentais

### 1. Identificadores Únicos e Descritivos
Uma skill DEVE ter um identificador (`name`) que seja:
- **Único** no ecossistema do CLI-alvo
- **Descritivo** da funcionalidade principal
- **Legível** por humanos e máquinas
- **Sem espaços** (usar kebab-case ou snake_case)

**Fonte**: Princípio de "Reificação da Intenção" [AI-Instruments, ACM DL]

### 2. Hierarquia Semântica
Skills DEVEM ser organizadas em hierarquia de 2-3 níveis:
```
category/subcategory/skill-name
```

**Exemplo**:
```
database/query-generation/generate-complex-sql
testing/unit-tests/jest-test-generator
security/code-analysis/detect-injection-vulnerabilities
```

### 3. Verbos de Ação
Nomes de skills DEVEM iniciar com verbo que descreve ação:
- `generate-*` (gerar código, documentação)
- `analyze-*` (análise de código, dados)
- `refactor-*` (refatoração)
- `validate-*` (validação)
- `optimize-*` (otimização)
- `detect-*` (detecção de padrões, bugs)

## Convenções por Domínio

### Database Skills
| Padrão | Exemplo | Categoria |
|--------|---------|-----------|
| `generate-{query-type}` | `generate-complex-sql` | `database/query-generation` |
| `optimize-{aspect}` | `optimize-query-performance` | `database/optimization` |
| `migrate-{source}-to-{target}` | `migrate-mysql-to-postgres` | `database/migration` |

### Code Quality Skills
| Padrão | Exemplo | Categoria |
|--------|---------|-----------|
| `analyze-{aspect}` | `analyze-code-complexity` | `code-quality/analysis` |
| `detect-{issue-type}` | `detect-security-vulnerabilities` | `code-quality/security` |
| `format-{language}` | `format-python-pep8` | `code-quality/formatting` |

### Testing Skills
| Padrão | Exemplo | Categoria |
|--------|---------|-----------|
| `generate-{test-type}` | `generate-unit-tests` | `testing/generation` |
| `run-{framework}` | `run-jest-coverage` | `testing/execution` |
| `mock-{dependency}` | `mock-api-responses` | `testing/mocking` |

### Documentation Skills
| Padrão | Exemplo | Categoria |
|--------|---------|-----------|
| `generate-{doc-type}` | `generate-api-docs` | `documentation/generation` |
| `validate-{format}` | `validate-markdown-links` | `documentation/validation` |
| `extract-{content}` | `extract-code-comments` | `documentation/extraction` |

## Regras de Formatação

### Kebab-Case (Recomendado)
```yaml
name: generate-complex-sql
category: database
subcategory: query-generation
```

**Vantagens**:
- Compatível com URLs
- Legível em paths de arquivo
- Adotado por Claude Code, Gemini CLI

### Snake_Case (Alternativa)
```yaml
name: generate_complex_sql
category: database
subcategory: query_generation
```

**Vantagens**:
- Compatível com Python/Ruby
- Usado em alguns CLIs legados

### CamelCase (Evitar)
```yaml
# ❌ NÃO RECOMENDADO
name: GenerateComplexSql
```

**Desvantagens**:
- Menos legível em contextos CLI
- Conflitos com case-sensitive filesystems

## Nomes de Categorias Padronizadas

### Categorias de Nível Superior
| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| `code` | Geração/análise de código | `code/generation`, `code/refactoring` |
| `database` | Operações de banco de dados | `database/query`, `database/migration` |
| `testing` | Testes e validação | `testing/unit`, `testing/integration` |
| `documentation` | Documentação | `documentation/api`, `documentation/guides` |
| `security` | Análise de segurança | `security/audit`, `security/compliance` |
| `devops` | Operações de desenvolvimento | `devops/ci-cd`, `devops/deployment` |
| `data` | Processamento de dados | `data/etl`, `data/analysis` |

### Subcategorias Comuns
| Categoria | Subcategorias |
|-----------|---------------|
| `code` | `generation`, `refactoring`, `analysis`, `formatting` |
| `database` | `query`, `schema`, `migration`, `optimization` |
| `testing` | `unit`, `integration`, `e2e`, `performance` |
| `documentation` | `api`, `guides`, `tutorials`, `changelog` |

## Anti-Patterns (Evitar)

### ❌ Nomes Genéricos Demais
```yaml
# Ruim
name: sql-generator

# Bom
name: generate-complex-sql-with-joins
```

### ❌ Nomes Específicos Demais
```yaml
# Ruim
name: generate-sql-for-postgresql-14-with-window-functions-and-ctes

# Bom
name: generate-advanced-sql
```

### ❌ Siglas Não Documentadas
```yaml
# Ruim
name: gen-sql-cte-wf

# Bom
name: generate-sql-window-functions
```

### ❌ Incluir Versão no Nome
```yaml
# Ruim
name: generate-sql-v2

# Bom
name: generate-sql
version: 2.0.0  # Usar campo version
```

## Adaptações por CLI

### Claude Code
```json
{
  "name": "generate-complex-sql",
  "domains": ["database", "sql"],
  "keywords": ["generate", "sql", "query"]
}
```

### Gemini CLI
```yaml
name: generate-complex-sql
category: database
tags:
  - sql-generation
  - database-tools
```

### GitHub Copilot
```json
{
  "skillId": "database/generate-complex-sql",
  "displayName": "Generate Complex SQL Queries"
}
```

### Qwen Code
```yaml
skill_name: generate_complex_sql
module: database.query_generation
```

## Validação de Nomes

### Checklist
- [ ] Nome segue kebab-case ou snake_case?
- [ ] Nome inicia com verbo de ação?
- [ ] Nome tem 2-5 palavras?
- [ ] Categoria está na lista padronizada?
- [ ] Nome não contém versão?
- [ ] Nome é único no ecossistema?
- [ ] Nome é descritivo sem ser prolixo?

### Regex de Validação
```regex
# Kebab-case: letras minúsculas, números, hífens
^[a-z][a-z0-9-]*[a-z0-9]$

# Snake_case: letras minúsculas, números, underscores
^[a-z][a-z0-9_]*[a-z0-9]$
```

## Exemplos Reais

### Skills Documentadas
1. **java-fundamentals** (`.opencode/skills/`)
   - Nome: `java-fundamentals`
   - Categoria: `programming-languages`
   - Descrição: Auxilia no desenvolvimento Java seguindo boas práticas

2. **kotlin-fundamentals** (`.opencode/skills/`)
   - Nome: `kotlin-fundamentals`
   - Categoria: `programming-languages`
   - Descrição: Desenvolvimento Kotlin com tipos seguros

3. **coala-framework** (`.opencode/skills/`)
   - Nome: `coala-framework`
   - Categoria: `ai-architectures`
   - Descrição: Implementação do framework CoALA

## Relacionados
- [structure.md](structure.md) - Estrutura de skills
- [descriptions.md](descriptions.md) - Descrições eficazes
- [agent-skills-spec.md](../agent-skills-spec.md) - Especificação completa

## Referências
1. AI-Instruments: Reificação da Intenção (ACM DL)
2. Agent Skills Spec (https://agentskills.io)
3. Claude Code Documentation
4. Gemini CLI Best Practices
5. GitHub Naming Conventions

---

**Best Practice** | Hefesto Knowledge Base | v1.0.0
