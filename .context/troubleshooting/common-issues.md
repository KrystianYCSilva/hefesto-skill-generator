# Troubleshooting - Common Issues

> **Tier:** T2 - Informativo
> **Proposito:** Resolver problemas comuns do Hefesto Skill Generator
> **Versao:** 2.2.0
---

## 1. Erros de Validacao

### 1.1. INVALID_NAME

**Erro:**
```
INVALID_NAME: "Code-Review" contem caracteres invalidos
```

**Causa:** Campo `name` contem uppercase, espacos, ou caracteres especiais.

**Solucao:**
```yaml
# INCORRETO
name: Code-Review
name: code review
name: code_review

# CORRETO
name: code-review
```

**Regras do `name`:**
- Apenas lowercase (a-z), numeros (0-9), hyphens (-)
- Nao comecar/terminar com hyphen
- Sem hyphens consecutivos
- Max 64 caracteres
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

---

### 1.2. EMPTY_DESCRIPTION

**Erro:**
```
EMPTY_DESCRIPTION: Campo description esta vazio
```

**Solucao:**
```yaml
# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas.
  Use when: revisar PRs, avaliar codigo.
```

---

### 1.3. DESCRIPTION_TOO_LONG

**Erro:**
```
DESCRIPTION_TOO_LONG: Description excede 1024 caracteres
```

**Solucao:**
- Resumir descricao para < 1024 chars
- Mover detalhes para corpo do SKILL.md

---

### 1.4. FILE_TOO_LARGE

**Erro:**
```
FILE_TOO_LARGE: SKILL.md excede 500 linhas
```

**Solucao:**
1. Mover documentacao detalhada para `references/`
2. Mover scripts longos para `scripts/`
3. Manter apenas core em SKILL.md

---

### 1.5. INVALID_YAML

**Erro:**
```
INVALID_YAML: Erro de parse no frontmatter
```

**Erros comuns de YAML:**
- Aspas nao escapadas
- Indentacao inconsistente
- Dois pontos sem espaco depois

---

### 1.6. FORBIDDEN_FIELDS

**Erro:**
```
FORBIDDEN_FIELDS: Frontmatter contem campos alem de name/description
```

**Causa:** Frontmatter com license, metadata, version, tags, compatibility.

**Solucao:** Remover TODOS os campos exceto `name` e `description`.

```yaml
# PROIBIDO (v2.0.0)
---
name: code-review
description: "..."
license: MIT               # REMOVER
metadata:
  version: "1.0.0"        # REMOVER
  tags: [code-review]     # REMOVER
---

# CORRETO
---
name: code-review
description: |
  Descricao. Use when: trigger.
---
```

---

## 2. Problemas de CLI

### 2.1. Nenhum CLI Detectado

**Causa:** Nenhum CLI instalado ou nao esta no PATH.

**Solucao:**
1. Verificar se CLI esta instalado: `claude --version`, `gemini --version`
2. Adicionar ao PATH se necessario
3. Ou rodar `/hefesto.init` que tenta detectar por diretorios tambem

---

### 2.2. Diretorio de Skills Nao Existe

**Causa:** Diretorio de skills ainda nao foi criado.

**Solucao:** Rodar o installer (`install.sh` ou `install.ps1`) ou `/hefesto.init`.

---

### 2.3. Skill Ja Existe

**Solucao:**
- Escolher outro nome
- Usar `/hefesto.validate skill-name` para validar e corrigir
- Selecionar [overwrite] no Human Gate se quiser substituir

---

## 3. Problemas de Instalacao

### 3.1. Installer Nao Encontra CLIs

**Causa:** CLIs nao estao no PATH.

**Solucao:** O installer tambem detecta por diretorios existentes (`.claude/`, `.gemini/`, etc.). Se nenhum for encontrado, cria `.claude/` como default.

### 3.2. Permissao Negada

**Causa:** Sem permissao para criar diretorios.

**Solucao:**
```bash
# Unix/macOS
chmod +w .

# Windows PowerShell
# Executar como administrador se necessario
```

### 3.3. Ja Instalado

**Comportamento esperado:** O installer e idempotente.
- Arquivos identicos: `[skip]`
- Arquivos diferentes: `[update]` (com aviso)
- `.hefesto/version` atualizado

---

## 4. Problemas de Human Gate

### 4.1. Opcao Invalida

**Opcoes validas:** `[approve]` `[edit]` `[reject]`

Para `/hefesto.validate`: tambem `[fix-auto]` `[fix-manual]` `[skip]`

---

## 5. Problemas de Extracao

### 5.1. Arquivo Nao Encontrado

**Solucao:** Verificar caminho do arquivo. Usar caminho relativo ao diretorio atual.

### 5.2. Nenhum Padrao Detectado

**Solucao:**
- Arquivo pode nao ter padroes claros para extrair
- Usar `/hefesto.create` ao inves de `/hefesto.extract`

---

## 6. Perguntas Frequentes

### Como resetar uma skill?

Deletar o diretorio da skill manualmente:
```bash
rm -rf .claude/skills/skill-name/
# Repetir para outros CLIs
```

### Como atualizar Hefesto?

Rodar o installer novamente no projeto:
```bash
bash hefesto-skill-generator/installer/install.sh
```

### Comandos disponiveis?

| Comando | Descricao |
|---------|-----------|
| `/hefesto.create` | Criar skill de descricao |
| `/hefesto.validate` | Validar + corrigir skill |
| `/hefesto.extract` | Extrair skill de codigo |
| `/hefesto.init` | Verificar instalacao |
| `/hefesto.list` | Listar skills |

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)



