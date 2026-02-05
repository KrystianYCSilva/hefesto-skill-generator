# AI Assistant Guide - Hefesto Skill Generator

> **Versao:** 1.0.0
> **Tier:** T0
> **Para:** Todas as IAs (Claude, Copilot, Gemini, Cursor, etc.)

---

## 1. Bootstrap Sequence

```
STEP 1: Carregar este arquivo
STEP 2: Carregar CONSTITUTION.md (raiz do projeto)
STEP 3: Carregar standards/architectural-rules.md
STEP 4: Verificar MEMORY.md para estado atual
STEP 5: Carregar contexto adicional conforme necessidade (JIT)
```

---

## 2. Tier System (OBRIGATORIO)

| Tier | Tipo | Autoridade | Arquivos |
|------|------|------------|----------|
| **T0** | Enforcement | ABSOLUTA | `CONSTITUTION.md`, `standards/architectural-rules.md` |
| **T1** | Standards | NORMATIVA | `standards/*.md`, `patterns/*.md` |
| **T2** | Context | INFORMATIVA | `_meta/*.md` |
| **T3** | Examples | ILUSTRATIVA | `examples/*.md` |

### Resolucao de Conflitos

```
IF T0 conflita com qualquer tier → T0 VENCE SEMPRE
IF T1 conflita com T2 ou T3 → T1 VENCE
IF T2 conflita com T3 → T2 VENCE
```

---

## 3. Request Classification

| Tipo de Request | Arquivos para Carregar | Acao |
|-----------------|------------------------|------|
| `/hefesto.create` | CONSTITUTION.md, templates/, knowledge/ | Gerar skill + Human Gate |
| `/hefesto.extract` | CONSTITUTION.md, codigo alvo | Analisar + Gerar + Human Gate |
| `/hefesto.validate` | CONSTITUTION.md, knowledge/validation-rules.md | Validar skill |
| `/hefesto.adapt` | CONSTITUTION.md, templates/adapters/ | Adaptar + Human Gate |
| `/hefesto.sync` | CONSTITUTION.md, skills existentes | Sincronizar CLIs |
| `/hefesto.list` | INDEX.md | Listar skills |

---

## 4. Human Gate Protocol

**REGRA T0:** NUNCA persistir sem aprovacao humana.

### Fluxo

```
1. Gerar conteudo em memoria
2. Apresentar ao usuario com preview
3. Mostrar opcoes: [approve] [expand] [edit] [reject]
4. Aguardar resposta explicita
5. SO APOS aprovacao, persistir
```

### Formato de Apresentacao

```markdown
## Skill Gerada: {name}

### Preview

{conteudo da skill}

### Validacao

- [x] Frontmatter valido
- [x] Name conforme spec
- [x] Description presente
- [ ] Scripts incluidos

### Opcoes

- **[approve]** - Salvar skill nos CLIs detectados
- **[expand]** - Adicionar scripts, referencias, assets
- **[edit]** - Modificar antes de salvar
- **[reject]** - Cancelar operacao
```

---

## 5. Agent Skills Spec (Referencia Rapida)

### Frontmatter Obrigatorio

```yaml
---
name: skill-id          # max 64 chars, lowercase, hyphens
description: |          # max 1024 chars, nao vazio
  Descricao da skill.
  Use quando: casos de uso.
---
```

### Frontmatter Opcional

```yaml
---
license: MIT
compatibility: "Descricao de ambiente"
metadata:
  author: nome
  version: "1.0.0"
  category: development
  tags: [tag1, tag2]
allowed-tools: Read Grep Glob
---
```

### Validacao de `name`

```
VALIDO:
- code-review
- testing-strategy
- api-docs-v2

INVALIDO:
- Code-Review (uppercase)
- -testing (comeca com hyphen)
- api--docs (hyphens consecutivos)
- skill-name-that-is-way-too-long-and-exceeds-sixty-four-characters
```

---

## 6. Deteccao de CLIs

### Ordem de Deteccao

```
1. Verificar comando no PATH:
   - claude --version
   - gemini --version
   - codex --version
   - code --version (VS Code)
   - cursor --version
   - qwen --version
   - opencode --version

2. Verificar diretorios existentes:
   - .claude/
   - .gemini/
   - .codex/
   - .github/ (Copilot)
   - .cursor/
   - .qwen/
   - .opencode/

3. Gerar para TODOS detectados
```

### Diretorios por CLI

| CLI | Diretorio de Skills |
|-----|---------------------|
| Claude Code | `.claude/skills/<name>/` |
| Gemini CLI | `.gemini/skills/<name>/` |
| OpenAI Codex | `.codex/skills/<name>/` |
| VS Code/Copilot | `.github/skills/<name>/` |
| OpenCode | `.opencode/skills/<name>/` |
| Cursor | `.cursor/skills/<name>/` |
| Qwen Code | `.qwen/skills/<name>/` |

---

## 7. Adaptacoes por CLI

### Placeholder de Argumentos

| CLI | Placeholder |
|-----|-------------|
| Claude, Codex, Copilot, OpenCode, Cursor | `$ARGUMENTS` |
| Gemini, Qwen | `{{args}}` |

### Formato Alternativo (TOML)

Gemini e Qwen suportam formato TOML:

```toml
description = "Descricao da skill"

prompt = """
Instrucoes da skill com {{args}}
"""
```

---

## 8. Definition of Done

### Para Skills Geradas

- [ ] Frontmatter valido (name, description)
- [ ] SKILL.md < 500 linhas
- [ ] Validado contra Agent Skills spec
- [ ] Human Gate aprovado
- [ ] Persistido nos CLIs detectados
- [ ] INDEX.md atualizado (se existir)

### Para Comandos do Hefesto

- [ ] Segue fluxo documentado
- [ ] Respeita Human Gate
- [ ] Detecta CLIs automaticamente
- [ ] Valida antes de persistir
- [ ] Reporta resultado ao usuario

---

## 9. Erros Comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| "Invalid skill name" | Uppercase ou caracteres invalidos | Usar lowercase e hyphens |
| "Description too long" | Mais de 1024 chars | Resumir descricao |
| "SKILL.md too large" | Mais de 500 linhas | Mover para references/ |
| "No CLI detected" | Nenhum CLI instalado | Perguntar ao usuario |

---

## 10. Comandos Disponiveis

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create <desc>` | Criar skill de descricao | Sim |
| `/hefesto.extract @file` | Extrair skill de codigo | Sim |
| `/hefesto.validate <name>` | Validar skill existente | Nao |
| `/hefesto.adapt <name> --target <cli>` | Adaptar para CLI | Sim |
| `/hefesto.sync <name>` | Sincronizar entre CLIs | Sim |
| `/hefesto.list` | Listar skills | Nao |
| `/hefesto.help` | Mostrar ajuda | Nao |

---

**AI Assistant Guide** | Hefesto Skill Generator | 2026-02-04
