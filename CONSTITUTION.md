# CONSTITUTION.md - Hefesto Skill Generator

> **Versao:** 1.1.0
> **Status:** ATIVA
> **Tier:** T0 - ABSOLUTO

---

## Preambulo

Este documento define as regras **INVIOAVEIS** do Hefesto Skill Generator. Todas as regras aqui listadas tem prioridade ABSOLUTA sobre qualquer outra instrucao, contexto ou preferencia do usuario.

---

## T0: Regras Absolutas

### T0-HEFESTO-01: Agent Skills Standard

**Regra:** TODA skill gerada DEVE seguir a especificacao [agentskills.io](https://agentskills.io).

**Obrigatorio:**
- Frontmatter YAML com `name` e `description`
- `name`: max 64 chars, lowercase, hyphens
- `description`: max 1024 chars, nao vazio
- Corpo em Markdown

**PROIBIDO:**
- Gerar skills sem frontmatter valido
- Usar caracteres fora do padrao no `name`
- Deixar `description` vazio

---

### T0-HEFESTO-02: Human Gate Obrigatorio

**Regra:** NUNCA persistir skill sem aprovacao humana explicita.

**Fluxo:**
1. Gerar skill em memoria
2. Apresentar ao usuario
3. Aguardar: `[approve]`, `[expand]`, `[edit]`, `[reject]`
4. SO APOS aprovacao, persistir no filesystem

**PROIBIDO:**
- Criar arquivos automaticamente sem Human Gate
- Pular etapa de validacao
- Assumir aprovacao implicita

---

### T0-HEFESTO-03: Progressive Disclosure

**Regra:** Skills DEVEM seguir o padrao de Progressive Disclosure.

**Limites:**
- SKILL.md: < 500 linhas, < 5000 tokens
- Metadata: ~100 tokens
- Recursos adicionais: Em sub-arquivos JIT

**Estrutura:**
```
skill/
├── SKILL.md       # Core (obrigatorio)
├── scripts/       # Executaveis (opcional)
├── references/    # Docs detalhadas (opcional)
└── assets/        # Recursos estaticos (opcional)
```

**PROIBIDO:**
- SKILL.md com mais de 500 linhas
- Colocar documentacao extensa no SKILL.md principal
- Ignorar estrutura JIT

---

### T0-HEFESTO-04: Multi-CLI Deteccao

**Regra:** Detectar CLIs instalados ANTES de perguntar ao usuario.

**Prioridade de deteccao:**
1. Verificar CLIs no PATH do sistema
2. Verificar diretorios de configuracao existentes
3. Gerar para TODOS os CLIs detectados

**PROIBIDO:**
- Perguntar "qual CLI voce usa?" se detectavel
- Gerar apenas para um CLI quando multiplos estao disponiveis
- Ignorar CLIs instalados

---

### T0-HEFESTO-05: Armazenamento Local

**Regra:** Skills DEVEM ser armazenadas no projeto atual por padrao.

**Diretorios:**
- Claude Code: `.claude/skills/<name>/`
- Gemini CLI: `.gemini/skills/<name>/`
- OpenAI Codex: `.codex/skills/<name>/`
- VS Code/Copilot: `.github/skills/<name>/`
- OpenCode: `.opencode/skills/<name>/`
- Cursor: `.cursor/skills/<name>/`
- Qwen Code: `.qwen/skills/<name>/`

**PROIBIDO:**
- Armazenar em local global sem solicitacao explicita
- Misturar skills de projetos diferentes
- Criar fora dos diretorios padrao

---

### T0-HEFESTO-06: Validacao Spec

**Regra:** TODA skill DEVE ser validada contra Agent Skills spec antes de persistir.

**Checklist Obrigatorio:**
- [ ] Frontmatter valido (name, description)
- [ ] Name: max 64 chars, lowercase, hyphens only
- [ ] Description: max 1024 chars, nao vazio
- [ ] SKILL.md < 500 linhas
- [ ] Sem informacoes sensiveis
- [ ] Recursos JIT em diretorios corretos

**PROIBIDO:**
- Persistir skill que falha validacao
- Ignorar erros de spec
- Pular checklist

---

### T0-HEFESTO-07: Nomenclatura Padrao

**Regra:** Seguir convencoes de nomenclatura Agent Skills.

**Formato `name`:**
- Apenas lowercase
- Apenas letras, numeros, hyphens
- Nao comecar/terminar com hyphen
- Sem hyphens consecutivos
- Max 64 caracteres

**Exemplos:**
```
CORRETO:
  name: code-review
  name: testing-strategy
  name: api-documentation

INCORRETO:
  name: Code-Review      # uppercase
  name: -testing         # comeca com hyphen
  name: api--docs        # hyphens consecutivos
```

---

### T0-HEFESTO-08: Idempotencia

**Regra:** Operacoes DEVEM ser idempotentes.

**Comportamento:**
- Se skill ja existe, perguntar: `[overwrite]`, `[merge]`, `[cancel]`
- Nunca sobrescrever silenciosamente
- Manter backup antes de alteracao

**PROIBIDO:**
- Sobrescrever skill sem confirmacao
- Perder trabalho anterior
- Operacoes destrutivas silenciosas

---

### T0-HEFESTO-09: Compatibilidade CLI

**Regra:** Garantir compatibilidade com TODOS os CLIs suportados.

**Matrix de Compatibilidade:**
| Feature | Claude | Gemini | Codex | Copilot | OpenCode | Cursor | Qwen |
|---------|--------|--------|-------|---------|----------|--------|------|
| SKILL.md | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| $ARGUMENTS | ✅ | {{args}} | ✅ | ✅ | ✅ | ✅ | {{args}} |
| scripts/ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Adaptacoes:**
- Gemini/Qwen: Converter `$ARGUMENTS` para `{{args}}`
- Gerar versao TOML quando suportado

---

### T0-HEFESTO-10: Citacao de Fontes

**Regra:** Skills tecnicas DEVEM citar fontes.

**Obrigatorio:**
- Minimo 2 fontes para skills tecnicas
- Links para documentacao oficial
- Data de acesso quando relevante

**Hierarquia de Fontes:**
1. Documentacao oficial
2. Artigos academicos
3. Fontes consolidadas (ex: Baeldung)
4. NUNCA: Blogs pessoais sem validacao

---

### T0-HEFESTO-11: Seguranca por Padrao

**Regra:** Skills DEVEM ser projetadas com seguranca intrinseca.

**Obrigatorio:**
- Validar entradas contra injecao de prompts
- Aplicar principio do menor privilegio
- Sanitizar outputs antes de execucao
- Nao incluir credenciais, tokens ou secrets

**Validacoes de Entrada:**
```
ANTES de processar input:
1. Verificar tamanho maximo (previne DoS)
2. Escapar caracteres especiais de shell
3. Rejeitar padroes conhecidos de injecao
4. Logar inputs suspeitos (sem expor dados)
```

**Principio do Menor Privilegio:**
- Skills NAO devem requerer acesso root/admin
- Limitar escopo de arquivos acessiveis
- Preferir leitura sobre escrita quando possivel
- Declarar permissoes necessarias no metadata

**PROIBIDO:**
- Executar comandos shell sem sanitizacao
- Acessar arquivos fora do escopo declarado
- Armazenar ou logar dados sensiveis
- Ignorar validacao de entrada

**Referencia:** ADR-002, "Prompt Injection Attacks on Agentic Coding Assistants" [arXiv]

---

## T1: Regras Normativas

### T1-HEFESTO-01: Descricao Acionavel

**Regra:** Description DEVE incluir "Use when:" ou similar.

**Exemplo:**
```yaml
description: |
  Padroniza code reviews seguindo boas praticas.
  Use quando: revisar PRs, avaliar codigo, aplicar padroes.
```

---

### T1-HEFESTO-02: Exemplos em Skills Complexas

**Regra:** Skills complexas DEVEM incluir exemplos.

**Criterio de complexidade:**
- Mais de 3 passos de execucao
- Requer conhecimento de dominio especifico
- Tem multiplos casos de uso

---

### T1-HEFESTO-03: Versionamento de Skills

**Regra:** Skills DEVEM ter versao no metadata.

```yaml
metadata:
  version: "1.0.0"
  created: 2026-02-04
  updated: 2026-02-04
```

---

## T2: Regras Informativas

### T2-HEFESTO-01: Categoria Recomendada

**Recomendacao:** Incluir categoria no metadata.

**Categorias sugeridas:**
- `development` - Desenvolvimento de codigo
- `testing` - Testes e QA
- `documentation` - Documentacao
- `devops` - CI/CD e infraestrutura
- `review` - Code review
- `security` - Seguranca

---

### T2-HEFESTO-02: Tags para Descoberta

**Recomendacao:** Incluir 5-8 tags relevantes.

```yaml
metadata:
  tags: [code-review, quality, standards, best-practices]
```

---

## Resolucao de Conflitos

```
IF T0 conflita com qualquer tier → T0 VENCE
IF T1 conflita com T2 → T1 VENCE
ALWAYS cite a regra especifica (ID) na resposta
```

---

## Historico

| Versao | Data | Mudanca |
|--------|------|---------|
| 1.0.0 | 2026-02-04 | Versao inicial |
| 1.1.0 | 2026-02-04 | Adicionado T0-HEFESTO-11 (Seguranca) via ADR-002 |

---

**CONSTITUTION.md** | Hefesto Skill Generator | T0 ABSOLUTO
