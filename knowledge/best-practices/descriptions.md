# Descrições Eficazes - Best Practices

## Fonte
Extraído de: `docs/pesquisa/skill-generator-automatizado.md` (linhas 17-25)  
Agent Skills Spec: https://agentskills.io  
Learn Prompting: https://learnprompting.org/  
Acessado: 2026-02-05

## Resumo
Técnicas para escrever descrições de skills que sejam claras, acionáveis e eficazes tanto para agentes de IA quanto para desenvolvedores humanos. Baseado em princípios de "Descritividade e Auto-documentação" e análise de 87 papers acadêmicos.

## Princípios Fundamentais

### 1. Descrição = Contrato
A descrição da skill é um contrato formal que:
- Define **o quê** a skill faz
- Especifica **quando** usar a skill
- Declara **limitações** conhecidas
- Documenta **dependências** externas

**Fonte**: AI-Instruments [ACM DL] - Auto-documentação

### 2. Clareza > Brevidade
Prefira descrição completa e clara a descrição curta e ambígua:
```yaml
# ❌ Ruim (ambíguo)
description: Generates SQL

# ✅ Bom (claro)
description: |
  Generates complex SQL queries from natural language descriptions,
  supporting PostgreSQL, MySQL and SQLite. Handles joins, aggregations,
  window functions and CTEs.
```

### 3. Ação-Resultado-Contexto
Estrutura recomendada:
```
[AÇÃO] → [RESULTADO] → [CONTEXTO]
```

**Exemplo**:
```yaml
description: |
  [AÇÃO] Analyzes Python code for security vulnerabilities
  [RESULTADO] Returns list of issues with severity levels and fix suggestions
  [CONTEXTO] Supports CWE-22, CWE-78, CWE-89, CWE-79 and CWE-798
```

## Anatomia de uma Boa Descrição

### Campo `description` (Obrigatório)
```yaml
description: |
  [1-2 linhas] Resumo executivo do que a skill faz
  
  [3-5 linhas] Detalhes sobre funcionalidades principais:
  - Funcionalidade 1
  - Funcionalidade 2
  - Funcionalidade 3
  
  [1-2 linhas] Limitações conhecidas ou pré-requisitos
```

### Exemplo Real (java-fundamentals)
```yaml
description: |
  Auxilia no desenvolvimento de código Java seguindo boas práticas de POO,
  padrões de código limpo e recursos modernos da linguagem (Java 6-25).
  
  Use quando: criar classes Java, refatorar código, aplicar design patterns,
  trabalhar com collections, streams, exceções ou recursos da JVM.
  
  Requer: JDK 8+ instalado, conhecimento básico de programação.
```

## Componentes de Descrição

### 1. Resumo Executivo (Linha 1)
**O quê**: Declaração direta da funcionalidade principal

```yaml
# Template
description: |
  [Verbo de ação] [objeto] [propósito/benefício]

# Exemplos
description: |
  Generates unit tests for JavaScript/TypeScript functions using Jest framework
  
  Analyzes database schema and suggests normalization improvements
  
  Refactors Python code to follow PEP 8 style guide
```

### 2. Funcionalidades Detalhadas (Linhas 3-7)
**Como**: Lista de capacidades específicas

```yaml
description: |
  Generates complex SQL queries from natural language descriptions.
  
  Capabilities:
  - Multi-table joins (INNER, LEFT, RIGHT, FULL)
  - Aggregations (GROUP BY, HAVING)
  - Window functions (ROW_NUMBER, RANK, LAG, LEAD)
  - Common Table Expressions (CTEs)
  - Subqueries and derived tables
```

### 3. Casos de Uso (Linhas 8-10)
**Quando**: Contextos onde skill é útil

```yaml
description: |
  ...
  
  Use when:
  - Converting business requirements to SQL
  - Optimizing existing queries
  - Learning SQL best practices
  - Documenting database access patterns
```

### 4. Limitações (Linhas 11-13)
**O que NÃO faz**: Restrições e avisos

```yaml
description: |
  ...
  
  Limitations:
  - Does not execute queries (only generates)
  - Requires schema context for complex joins
  - Limited support for vendor-specific extensions
```

### 5. Pré-requisitos (Linhas 14-15)
**Dependências**: O que é necessário

```yaml
description: |
  ...
  
  Requires: Python 3.8+, SQLGlot library, database schema file
```

## Descrições por Tipo de Skill

### Code Generation Skills
```yaml
description: |
  [Gera/Cria] [tipo de código] [linguagem/framework] [padrão/estilo]
  
  Features:
  - [Lista de padrões suportados]
  - [Configurações disponíveis]
  
  Output: [Formato do resultado]
```

**Exemplo**:
```yaml
description: |
  Generates React component boilerplate following Airbnb style guide.
  
  Features:
  - Functional components with hooks
  - PropTypes validation
  - JSDoc documentation
  - Jest test template
  
  Output: .jsx file + .test.jsx file
```

### Analysis Skills
```yaml
description: |
  [Analisa] [objeto] [critério/métrica] [ação subsequente]
  
  Checks:
  - [Aspecto 1]
  - [Aspecto 2]
  
  Reports: [Formato do relatório]
```

**Exemplo**:
```yaml
description: |
  Analyzes Python code complexity using cyclomatic complexity metrics.
  
  Checks:
  - Function complexity (McCabe score)
  - Nested loops and conditionals
  - Code duplication (DRY violations)
  
  Reports: JSON with scores, hotspots and refactoring suggestions
```

### Refactoring Skills
```yaml
description: |
  [Refatora] [padrão original] [padrão-alvo] [benefício]
  
  Transformations:
  - [Transformação 1]
  - [Transformação 2]
  
  Preserves: [O que não muda]
```

**Exemplo**:
```yaml
description: |
  Refactors callback-based async code to async/await syntax for better readability.
  
  Transformations:
  - .then() chains → async/await
  - Nested callbacks → sequential await
  - Error handling → try/catch blocks
  
  Preserves: Functionality, variable names, comments
```

### Testing Skills
```yaml
description: |
  [Gera/Executa] [tipo de teste] [framework] [cobertura]
  
  Test types:
  - [Tipo 1]
  - [Tipo 2]
  
  Assertions: [Biblioteca de assertions]
```

**Exemplo**:
```yaml
description: |
  Generates comprehensive unit tests for Python functions using pytest.
  
  Test types:
  - Happy path (expected inputs)
  - Edge cases (boundary conditions)
  - Error cases (invalid inputs)
  
  Assertions: pytest built-in + hypothesis for property-based testing
```

## Descrição vs. Instructions

### Campo `description`
- **Público**: Agente + Humano
- **Quando**: Durante seleção de skill
- **Conteúdo**: O quê, quando, limitações

### Campo `instructions` (SKILL.md)
- **Público**: Agente executando skill
- **Quando**: Durante execução
- **Conteúdo**: Como executar, passo-a-passo

**Exemplo**:
```yaml
# metadata.yaml
description: |
  Generates complex SQL queries from natural language descriptions.
  Supports PostgreSQL, MySQL and SQLite dialects.
```

```markdown
# SKILL.md
## Instructions
When user provides natural language query description:
1. Parse description to identify tables, columns, conditions
2. Determine join types needed (INNER, LEFT, etc.)
3. Generate SQL using SQLGlot for target dialect
4. Add comments explaining complex parts
5. Validate syntax before returning
```

## Verbos de Ação Recomendados

### Geração/Criação
- `Generates` - Criar novo conteúdo
- `Creates` - Instanciar estrutura
- `Builds` - Construir artefato complexo
- `Scaffolds` - Criar estrutura base

### Análise/Inspeção
- `Analyzes` - Examinar em detalhe
- `Inspects` - Verificar aspectos específicos
- `Detects` - Identificar padrões/problemas
- `Audits` - Revisão sistemática

### Transformação
- `Refactors` - Reestruturar código
- `Converts` - Mudar formato
- `Migrates` - Mover entre sistemas
- `Optimizes` - Melhorar performance

### Validação
- `Validates` - Verificar conformidade
- `Verifies` - Confirmar correção
- `Checks` - Inspecionar requisitos
- `Tests` - Executar testes

## Checklist de Qualidade

### Obrigatório
- [ ] Primeira linha é resumo executivo claro
- [ ] Usa verbos de ação no presente
- [ ] Lista funcionalidades principais
- [ ] Declara limitações conhecidas
- [ ] Especifica pré-requisitos técnicos

### Recomendado
- [ ] Seção "Use when" com casos de uso
- [ ] Seção "Output" com formato esperado
- [ ] Exemplos concretos inline
- [ ] Comparação com alternativas (quando relevante)
- [ ] Links para documentação externa

### Evitar
- [ ] Jargão não explicado
- [ ] Promessas vagas ("melhor", "mais rápido")
- [ ] Descrição só com keywords
- [ ] Foco excessivo em implementação interna
- [ ] Texto promocional/marketing

## Exemplo Comparativo

### ❌ Descrição Ruim
```yaml
description: SQL generator using AI
```

**Problemas**:
- Genérica demais
- Não especifica capacidades
- Sem contexto de uso
- Sem limitações

### ✅ Descrição Boa
```yaml
description: |
  Generates complex SQL queries (SELECT statements) from natural language
  descriptions using SQLGlot parser and template matching.
  
  Capabilities:
  - Multi-table joins with automatic FK detection
  - Aggregations with GROUP BY and HAVING clauses
  - Window functions (PostgreSQL 9.6+)
  - Common Table Expressions (CTEs)
  
  Use when:
  - Converting business requirements to queries
  - Learning SQL syntax for specific use cases
  - Prototyping data access layers
  
  Limitations:
  - SELECT only (no INSERT/UPDATE/DELETE)
  - Requires schema context file (YAML or JSON)
  - Limited support for MySQL-specific syntax
  
  Requires: Python 3.8+, SQLGlot 18.0+, schema file
```

**Por quê é boa**:
- Específica e detalhada
- Lista capacidades concretas
- Define casos de uso
- Declara limitações claramente
- Especifica dependências

## Internacionalização

### Idioma Primário: Inglês
```yaml
name: generate-complex-sql
description: |
  Generates complex SQL queries from natural language...
```

### Tradução (Opcional)
```yaml
name: generate-complex-sql
description: |
  Generates complex SQL queries from natural language...
description_pt: |
  Gera consultas SQL complexas a partir de descrições em linguagem natural...
description_es: |
  Genera consultas SQL complejas a partir de descripciones en lenguaje natural...
```

## Validação Automatizada

### Regex Checks
```python
# Verificar que primeira linha não termina com ponto
assert not description.split('\n')[0].endswith('.')

# Verificar que começa com verbo de ação
action_verbs = ['generates', 'analyzes', 'refactors', 'validates', ...]
assert description.split()[0].lower() in action_verbs

# Verificar comprimento mínimo
assert len(description.split()) >= 20  # Mínimo 20 palavras
```

### Quality Score
```python
def score_description(desc: str) -> float:
    score = 0.0
    if has_action_verb(desc): score += 0.2
    if has_capabilities_list(desc): score += 0.2
    if has_use_cases(desc): score += 0.2
    if has_limitations(desc): score += 0.2
    if has_requirements(desc): score += 0.2
    return score
```

## Relacionados
- [naming.md](naming.md) - Nomenclatura de skills
- [structure.md](structure.md) - Estrutura de skills
- [jit-resources.md](jit-resources.md) - Recursos complementares
- [../agent-skills-spec.md](../agent-skills-spec.md) - Spec completa

## Referências
1. AI-Instruments [ACM DL] - Auto-documentação
2. Learn Prompting - Prompt engineering guide
3. Agent Skills Spec (https://agentskills.io)
4. skill-generator-automatizado.md (linhas 17-25)
5. Existing skills in `.opencode/skills/`

---

**Best Practice** | Hefesto Knowledge Base | v1.0.0
