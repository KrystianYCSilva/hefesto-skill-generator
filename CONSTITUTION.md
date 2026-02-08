# CONSTITUTION.md - Hefesto Skill Generator

> **Versao:** 2.0.0
> **Status:** ATIVA
> **Tier:** T0 - ABSOLUTO

---

## Preambulo

Este documento define as regras **INVIOLAVEIS** do Hefesto Skill Generator. Todas as regras aqui listadas tem prioridade ABSOLUTA sobre qualquer outra instrucao, contexto ou preferencia do usuario.

Hefesto e um sistema **template-driven**: toda logica vive em Markdown, zero codigo Python ou executaveis. O AI agent le os templates e executa as fases.

---

## T0: Regras Absolutas

### T0-HEFESTO-01: Agent Skills Standard

**Regra:** TODA skill gerada DEVE seguir a especificacao [agentskills.io](https://agentskills.io).

**Obrigatorio:**
- Frontmatter YAML com `name` e `description`
- `name`: max 64 chars, lowercase, hyphens, pattern `^[a-z0-9]+(-[a-z0-9]+)*$`
- `description`: max 1024 chars, nao vazio, com "Use when:" trigger
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
2. Apresentar ao usuario (conteudo completo)
3. Aguardar: `[approve]`, `[edit]`, `[reject]`
4. SO APOS aprovacao, persistir no filesystem

**PROIBIDO:**
- Criar arquivos automaticamente sem Human Gate
- Pular etapa de apresentacao
- Assumir aprovacao implicita

---

### T0-HEFESTO-03: Progressive Disclosure

**Regra:** Skills DEVEM seguir o padrao de Progressive Disclosure.

**Limites:**
- SKILL.md: < 500 linhas, < ~5000 tokens
- Description: ~100 tokens ideal para discovery
- Recursos adicionais: Em sub-arquivos JIT (references/, scripts/, assets/)

**PROIBIDO:**
- SKILL.md com mais de 500 linhas
- Colocar documentacao extensa no SKILL.md principal
- Referencias aninhadas (references referenciando references)

---

### T0-HEFESTO-04: Multi-CLI Deteccao

**Regra:** Detectar CLIs instalados ANTES de perguntar ao usuario.

**Prioridade de deteccao:**
1. Verificar CLIs no PATH do sistema (where/which)
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
- [ ] Description: max 1024 chars, nao vazio, com "Use when:"
- [ ] SKILL.md < 500 linhas
- [ ] Sem informacoes sensiveis (credenciais, tokens, PII)
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
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

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
- Se skill ja existe, perguntar: `[overwrite]`, `[rename]`, `[skip]`
- Nunca sobrescrever silenciosamente
- Informar usuario sobre consequencias

**PROIBIDO:**
- Sobrescrever skill sem confirmacao
- Perder trabalho anterior
- Operacoes destrutivas silenciosas

---

### T0-HEFESTO-09: Compatibilidade CLI

**Regra:** Garantir compatibilidade com TODOS os CLIs suportados.

**Adaptacoes:**
- Claude/Codex/Copilot/OpenCode/Cursor: `$ARGUMENTS`
- Gemini/Qwen: `{{args}}`
- Conteudo do SKILL.md e identico; apenas invocacao adapta

---

### T0-HEFESTO-10: Citacao de Fontes

**Regra:** Skills tecnicas PODEM citar fontes quando relevante.

**Diretrizes:**
- Citar documentacao oficial quando referenciada diretamente no conteudo
- Nao incluir URLs well-known obvias (MDN, Oracle docs, etc.)
- Fontes em references/ para skills extensas, nao no SKILL.md principal

---

### T0-HEFESTO-11: Seguranca por Padrao

**Regra:** Skills DEVEM ser projetadas com seguranca intrinseca.

**PROIBIDO:**
- Incluir credenciais, tokens ou secrets em skills
- Incluir PII (informacoes pessoais identificaveis)
- URLs internas ou privadas

---

### T0-HEFESTO-12: Auto-Critica Obrigatoria

**Regra:** O AI agent DEVE revisar seu proprio output antes de apresentar ao usuario.

**Processo:**
1. Gerar skill
2. Rodar checklist de 13 itens (ver `templates/quality-checklist.md`)
3. Corrigir FAILs automaticamente
4. Documentar correcoes
5. SO ENTAO apresentar ao usuario no Human Gate

**PROIBIDO:**
- Apresentar skill sem auto-critica
- Ignorar checks que falharam
- Marcar FAIL como PASS sem correcao

---

### T0-HEFESTO-13: Template Authority

**Regra:** Toda logica do Hefesto vive em templates Markdown. NUNCA em codigo executavel.

**Principio:** Os comandos em `.claude/commands/hefesto.*.md` (e equivalentes para outros CLIs) sao a UNICA fonte de verdade para o comportamento do sistema.

**PROIBIDO:**
- Criar scripts Python, Node.js ou qualquer executavel para logica do Hefesto
- Mover logica de templates para codigo
- Dependencias externas (pip, npm, etc.)

---

## T1: Regras Normativas

### T1-HEFESTO-01: Descricao Acionavel

**Regra:** Description DEVE incluir "Use when:" ou trigger equivalente.

```yaml
description: |
  Padroniza code reviews seguindo boas praticas.
  Use when: revisar PRs, avaliar codigo, aplicar padroes.
```

---

### T1-HEFESTO-02: Exemplos em Skills

**Regra:** Skills DEVEM incluir exemplos apenas para padroes nao-obvios ou project-specific. Nao e obrigatorio para conceitos que o AI agent ja conhece.

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
| 1.1.0 | 2026-02-04 | Adicionado T0-HEFESTO-11 (Seguranca) |
| 2.0.0 | 2026-02-07 | Reset spec-kit: removido refs Python, adicionado T0-12 (Auto-Critica) e T0-13 (Template Authority), simplificado T0-08/09 |

---

**CONSTITUTION.md** | Hefesto Skill Generator | T0 ABSOLUTO
