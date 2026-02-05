# Estrutura de Skills - Best Practices

## Fonte
Extraído de: `docs/pesquisa/skill-generator-automatizado.md` (seções 55-100)  
Agent Skills Spec: https://agentskills.io  
Exemplos reais: `.opencode/skills/` (6 skills)  
Acessado: 2026-02-05

## Resumo
Estrutura modular recomendada para skills de agentes, incluindo organização de diretórios, arquivos de manifesto, separação de conteúdo e implementação de carregamento JIT (Just-in-Time). Baseado no princípio de "Organização Modular e Implementação de Carregamento Sob-Demanda".

## Princípios Arquiteturais

### 1. Modularidade (T0-HEFESTO-01)
Uma skill DEVE ser uma unidade funcional autocontida:
- **Núcleo leve**: Metadados + lógica mínima
- **Conteúdo complementar**: Exemplos, referências, tutoriais (JIT)
- **Separação de concerns**: Descrição ≠ Implementação ≠ Documentação

**Fonte**: Agent Skills Standard, linha 20 do research paper

### 2. Reificação da Intenção
Estrutura DEVE materializar a intenção da skill:
- Metadados descrevem **o quê** e **para quem**
- Lógica implementa **como**
- Conteúdo complementar explica **por quê**

**Fonte**: AI-Instruments [ACM DL], linha 9 do research paper

### 3. Escalabilidade
Estrutura DEVE suportar crescimento sem refatoração:
- Adicionar exemplos não altera manifesto
- Novos CLIs não requerem reescrita completa
- Versionamento independente de componentes

## Estrutura de Diretórios Recomendada

### Estrutura Básica
```
skills/
└── skill-name/
    ├── SKILL.md              # Manifesto principal (T0-HEFESTO-03: < 500 linhas)
    ├── metadata.yaml         # Metadados estruturados
    ├── main.py               # Lógica de execução (ou main.js, main.sh)
    └── content/              # Conteúdo JIT
        ├── examples/
        ├── references/
        └── benchmarks/
```

### Estrutura Completa (Multi-CLI)
```
skills/
└── generate-complex-sql/
    ├── SKILL.md                      # Manifesto abstrato (CLI-agnostic)
    ├── metadata.yaml                 # 9 campos obrigatórios
    ├── main.py                       # Lógica principal
    ├── cli-adapters/                 # Adaptações por CLI
    │   ├── claude-code/
    │   │   ├── manifest.json         # Claude Code manifest
    │   │   └── hook.py               # Hook Python
    │   ├── gemini-cli/
    │   │   └── config.yaml           # Gemini CLI config
    │   ├── copilot/
    │   │   └── mcp-server.js         # MCP Server
    │   └── qwen-code/
    │       └── module.py             # Qwen module
    ├── content/                      # Recursos JIT
    │   ├── examples/
    │   │   ├── basic-query.sql
    │   │   ├── joins-example.sql
    │   │   └── window-functions.sql
    │   ├── references/
    │   │   ├── postgres-docs.md
    │   │   └── sqlglot-api.md
    │   ├── benchmarks/
    │   │   ├── tpch-queries.yaml
    │   │   └── performance-tests.py
    │   └── tutorials/
    │       └── step-by-step.md
    ├── tests/                        # Casos de teste
    │   ├── test_basic.py
    │   └── test_edge_cases.py
    └── README.md                     # Documentação para desenvolvedores
```

## Arquivo SKILL.md (Manifesto Principal)

### Template Mínimo (Agent Skills Spec)
```markdown
# Skill Name

## Metadata
```yaml
name: generate-complex-sql
description: |
  Generates complex SQL queries from natural language descriptions,
  including joins, aggregations, and subqueries.
author: João Silva <joao@example.com>
version: 1.0.0
license: MIT
category: database
subcategory: query-generation
platforms:
  - claude-code
  - gemini-cli
  - github-copilot
dependencies:
  - python>=3.8
  - sqlglot>=18.0.0
```

## Instructions
[Instruções para o agente executar a skill]

## Examples
```sql
-- Example 1: Complex join
-- Input: "List customers with orders in 2024"
-- Output:
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE YEAR(o.created_at) = 2024
GROUP BY c.id, c.name;
```

## References
- PostgreSQL Documentation: https://postgresql.org/docs/
- SQLGlot API: https://github.com/tobymao/sqlglot

## Related Skills
- [optimize-query-performance](../optimize-query-performance/SKILL.md)
- [validate-sql-syntax](../validate-sql-syntax/SKILL.md)
```

### Regra T0-HEFESTO-03
**SKILL.md DEVE ter < 500 linhas**

Se conteúdo exceder 500 linhas:
1. Mover exemplos para `content/examples/`
2. Mover referências para `content/references/`
3. Mover tutoriais para `content/tutorials/`
4. Usar JIT Protocol para carregar sob demanda

## Arquivo metadata.yaml (9 Campos Obrigatórios)

```yaml
# Campo 1: Identificador único
name: generate-complex-sql

# Campo 2: Descrição detalhada
description: |
  Esta skill gera declarações SQL complexas a partir de descrição natural,
  incluindo junções, agregações e subconsultas. Suporta PostgreSQL, MySQL e SQLite.

# Campo 3: Autor e contato
author: João Silva <joao.silva@email.com>

# Campo 4: Versão SemVer
version: 1.0.0

# Campo 5: Licença
license: MIT

# Campo 6: Categoria principal
category: database

# Campo 7: Subcategoria
subcategory: query-generation

# Campo 8: Dependências
dependencies:
  - python>=3.8
  - sqlglot>=18.0.0
  - pydantic>=2.0.0

# Campo 9: Plataformas suportadas
platforms:
  - claude-code
  - gemini-cli
  - github-copilot
  - opencode
  - cursor
  - qwen-code

# Campos opcionais (mas recomendados)
example_prompt: |
  Gerar SQL para listar os 10 clientes com mais pedidos no último ano.

test_cases:
  - input: "List customers with orders in 2024"
    expected_output: "SELECT c.name, COUNT(o.id) ..."
  - input: "Calculate average order value by region"
    expected_output: "SELECT r.name, AVG(o.total) ..."

jit_manifest:
  examples_url: https://gist.github.com/user/sql-examples-abc123
  tutorial_url: https://docs.company.com/skills/generate-sql/tutorial
  references_urls:
    - https://www.postgresql.org/docs/
    - https://sqlite.org/lang.html
  benchmarks_url: https://github.com/user/sql-skill-benchmarks
```

## Arquivo main.py (Lógica de Execução)

### Template Básico
```python
#!/usr/bin/env python3
"""
Skill: generate-complex-sql
Author: João Silva
Version: 1.0.0
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any

# Importar bibliotecas necessárias
import sqlglot
from pydantic import BaseModel

class SkillInput(BaseModel):
    """Input schema para a skill"""
    description: str
    database: str = "postgresql"
    include_comments: bool = True

class SkillOutput(BaseModel):
    """Output schema para a skill"""
    sql: str
    confidence: float
    warnings: list[str] = []

def load_metadata() -> Dict[str, Any]:
    """Carregar metadados da skill"""
    metadata_path = Path(__file__).parent / "metadata.yaml"
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_jit_examples(examples_url: str) -> list[Dict[str, str]]:
    """Carregar exemplos via JIT Protocol"""
    # Implementação de carregamento sob demanda
    # Pode ser HTTP GET, GitHub API, etc.
    pass

def execute_skill(input_data: SkillInput) -> SkillOutput:
    """Lógica principal da skill"""
    # Processar descrição natural
    # Gerar SQL usando sqlglot
    # Validar sintaxe
    # Retornar resultado
    pass

def main():
    """Entry point da skill"""
    metadata = load_metadata()
    print(f"Executing skill: {metadata['name']} v{metadata['version']}")
    
    # Ler input do stdin ou args
    input_str = sys.stdin.read() if not sys.stdin.isatty() else sys.argv[1]
    input_data = SkillInput.model_validate_json(input_str)
    
    # Executar skill
    result = execute_skill(input_data)
    
    # Escrever output no stdout
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
```

## CLI Adapters (Multi-CLI)

### Claude Code (manifest.json + hook.py)
**Arquivo**: `cli-adapters/claude-code/manifest.json`
```json
{
  "name": "generate-complex-sql",
  "version": "1.0.0",
  "domains": ["database", "sql"],
  "keywords": ["generate", "sql", "query", "database"],
  "hook": "hook.py"
}
```

**Arquivo**: `cli-adapters/claude-code/hook.py`
```python
def on_request(request_text: str, context: dict) -> dict:
    """Hook executado em cada request ao agente"""
    keywords = ["sql", "query", "database", "generate"]
    if any(kw in request_text.lower() for kw in keywords):
        return {
            "load_skill": "generate-complex-sql",
            "inject_context": context.get("examples", [])
        }
    return {}
```

### Gemini CLI (config.yaml)
**Arquivo**: `cli-adapters/gemini-cli/config.yaml`
```yaml
skill_id: generate-complex-sql
trigger_patterns:
  - "generate.*sql"
  - "create.*query"
  - "write.*database"
execution:
  script: ../../main.py
  timeout: 30s
```

### GitHub Copilot (MCP Server)
**Arquivo**: `cli-adapters/copilot/mcp-server.js`
```javascript
const { MCPServer } = require('@modelcontextprotocol/sdk');

const server = new MCPServer({
  name: 'generate-complex-sql',
  version: '1.0.0',
  capabilities: ['tool']
});

server.defineTool('generate_sql', {
  description: 'Generates complex SQL queries from natural language',
  parameters: {
    description: { type: 'string' },
    database: { type: 'string', enum: ['postgresql', 'mysql', 'sqlite'] }
  },
  execute: async (params) => {
    // Chamar main.py
    const { exec } = require('child_process');
    const result = await execPromise(`python ../../main.py '${JSON.stringify(params)}'`);
    return JSON.parse(result);
  }
});

server.start();
```

## Content Directory (JIT Resources)

### examples/ (Exemplos de Uso)
```
content/examples/
├── basic-query.sql
├── joins-example.sql
├── window-functions.sql
├── cte-example.sql
└── README.md
```

### references/ (Referências Externas)
```
content/references/
├── postgres-docs.md       # Links para docs oficiais
├── sqlglot-api.md        # API reference do SQLGlot
├── best-practices.md     # Melhores práticas SQL
└── README.md
```

### benchmarks/ (Casos de Teste)
```
content/benchmarks/
├── tpch-queries.yaml     # TPC-H benchmark queries
├── performance-tests.py  # Testes de performance
└── README.md
```

## Checklist de Estrutura

### Obrigatório (T0)
- [ ] SKILL.md existe e tem < 500 linhas
- [ ] metadata.yaml contém 9 campos obrigatórios
- [ ] main.py (ou main.js/main.sh) é executável
- [ ] README.md documenta instalação e uso

### Recomendado
- [ ] content/ separado para recursos JIT
- [ ] cli-adapters/ para cada CLI-alvo
- [ ] tests/ com casos de teste automatizados
- [ ] jit_manifest em metadata.yaml

### Opcional
- [ ] benchmarks/ para validação de performance
- [ ] tutorials/ para guias passo-a-passo
- [ ] LICENSE file para licença formal

## Exemplos Reais

### 1. java-fundamentals (`.opencode/skills/`)
```
.opencode/skills/java-fundamentals/
├── SKILL.md (420 linhas)
└── references/ (8 links externos)
```

### 2. kotlin-fundamentals
```
.opencode/skills/kotlin-fundamentals/
├── SKILL.md (380 linhas)
└── references/ (7 links externos)
```

### 3. coala-framework
```
.opencode/skills/coala-framework/
├── SKILL.md (450 linhas)
└── references/ (4 papers acadêmicos)
```

## Anti-Patterns (Evitar)

### ❌ SKILL.md Monolítico
```
SKILL.md (2500 linhas) ← Viola T0-HEFESTO-03
```

### ❌ Metadados Embutidos em Código
```python
# ❌ Não fazer isso
SKILL_NAME = "generate-sql"
SKILL_VERSION = "1.0.0"
```

### ❌ CLI-Specific Hardcoded
```markdown
# ❌ SKILL.md específico para Claude Code
This skill only works with Claude Code...
```

### ❌ Sem Separação de Concerns
```
skill/
├── everything.py (1500 linhas) ← Tudo junto
```

## Relacionados
- [naming.md](naming.md) - Nomenclatura de skills
- [jit-resources.md](jit-resources.md) - Recursos JIT
- [security.md](security.md) - Segurança
- [../agent-skills-spec.md](../agent-skills-spec.md) - Spec completa

## Referências
1. Agent Skills Spec (https://agentskills.io)
2. skill-generator-automatizado.md (linhas 55-100)
3. AI-Instruments [ACM DL] - Reificação da intenção
4. Claude Code Docs - Manifest structure
5. MCP Protocol - Server architecture

---

**Best Practice** | Hefesto Knowledge Base | v1.0.0
