# Troubleshooting - Common Issues

> **Tier:** T2 - Informativo
> **Proposito:** Resolver problemas comuns do Hefesto Skill Generator

---

## 1. Erros de Validacao

### 1.1. INVALID_NAME

**Erro:**
```
❌ INVALID_NAME: "Code-Review" contem caracteres invalidos
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
- Apenas lowercase (a-z)
- Apenas numeros (0-9)
- Apenas hyphens (-)
- Nao comecar/terminar com hyphen
- Sem hyphens consecutivos
- Max 64 caracteres

---

### 1.2. EMPTY_DESCRIPTION

**Erro:**
```
❌ EMPTY_DESCRIPTION: Campo description esta vazio
```

**Causa:** Campo `description` vazio ou ausente.

**Solucao:**
```yaml
# INCORRETO
description: ""
description:

# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas.
  Use quando: revisar PRs, avaliar codigo.
```

---

### 1.3. DESCRIPTION_TOO_LONG

**Erro:**
```
❌ DESCRIPTION_TOO_LONG: Description excede 1024 caracteres (atual: 1156)
```

**Causa:** Description muito longa.

**Solucao:**
- Resumir descricao para < 1024 chars
- Mover detalhes para corpo do SKILL.md
- Usar references/ para documentacao extensa

---

### 1.4. FILE_TOO_LARGE

**Erro:**
```
❌ FILE_TOO_LARGE: SKILL.md excede 500 linhas (atual: 623)
```

**Causa:** SKILL.md muito extenso.

**Solucao:**
1. Mover documentacao detalhada para `references/REFERENCE.md`
2. Mover exemplos extensos para `references/EXAMPLES.md`
3. Mover scripts longos para `scripts/`
4. Manter apenas core em SKILL.md

---

### 1.5. INVALID_YAML

**Erro:**
```
❌ INVALID_YAML: Erro de parse no frontmatter linha 5
```

**Causa:** YAML malformado no frontmatter.

**Solucao:**
```yaml
# INCORRETO (aspas nao escapadas)
description: Skill para "code review"

# CORRETO
description: Skill para "code review"
# ou
description: |
  Skill para "code review"
```

**Erros comuns de YAML:**
- Aspas nao escapadas
- Indentacao inconsistente
- Dois pontos sem espaco depois
- Listas mal formatadas

---

## 2. Problemas de CLI

### 2.1. Nenhum CLI Detectado

**Erro:**
```
⚠️ Nenhum CLI de IA detectado no sistema
```

**Causa:** Nenhum CLI instalado ou nao esta no PATH.

**Solucao:**
1. Verificar se CLI esta instalado:
   ```bash
   claude --version
   gemini --version
   codex --version
   ```
2. Adicionar ao PATH se necessario
3. Usar flag para especificar CLI manualmente:
   ```
   /hefesto.create --cli claude "descricao"
   ```

---

### 2.2. Diretorio de Skills Nao Existe

**Erro:**
```
⚠️ Diretorio .claude/skills/ nao existe
```

**Causa:** Diretorio de skills ainda nao foi criado.

**Solucao:** Hefesto cria automaticamente. Se erro persistir:
```bash
mkdir -p .claude/skills
mkdir -p .gemini/skills
```

---

### 2.3. Skill Ja Existe

**Erro:**
```
⚠️ Skill "code-review" ja existe em .claude/skills/
```

**Causa:** Tentando criar skill com nome ja existente.

**Solucao:**
- Escolher outro nome
- Usar `/hefesto.validate code-review` para validar e corrigir
- Selecionar [overwrite] no Human Gate se quiser substituir

---

## 3. Problemas de Sincronizacao

### 3.1. Versoes Diferentes Entre CLIs

**Aviso:**
```
⚠️ Versoes diferentes detectadas:
   - Claude: v1.0.0
   - Gemini: v0.9.0
```

**Causa:** Skills desatualizadas em alguns CLIs.

**Solucao:**
Re-criar a skill com `/hefesto.create` ou `/hefesto.validate` com fix-auto para atualizar em todos os CLIs.

---

### 3.2. Adaptacao Falhou

**Erro:**
```
❌ Adaptacao falhou: Placeholder $CUSTOM_VAR nao suportado por Gemini
```

**Causa:** Skill usa features nao suportadas pelo CLI alvo.

**Solucao:**
1. Verificar features suportadas pelo CLI
2. Remover/substituir features incompativeis
3. Criar versao separada para CLI especifico

---

## 4. Problemas de Human Gate

### 4.1. Timeout no Human Gate

**Aviso:**
```
⚠️ Human Gate expirou apos 5 minutos de inatividade
```

**Causa:** Usuario nao respondeu a tempo.

**Solucao:**
- Executar comando novamente
- Skill gerada pode estar em cache, verificar com `/hefesto.list --pending`

---

### 4.2. Opcao Invalida

**Erro:**
```
❌ Opcao invalida: "ok"
Opcoes validas: [approve] [expand] [edit] [reject]
```

**Causa:** Resposta nao reconhecida no Human Gate.

**Solucao:** Usar uma das opcoes validas:
- `approve` ou `a` - Aprovar e salvar
- `expand` ou `e` - Expandir com wizard
- `edit` ou `ed` - Editar antes de salvar
- `reject` ou `r` - Cancelar

---

## 5. Problemas de Extracao

### 5.1. Arquivo Nao Encontrado

**Erro:**
```
❌ Arquivo nao encontrado: @src/utils/validation.ts
```

**Causa:** Caminho incorreto ou arquivo nao existe.

**Solucao:**
1. Verificar caminho do arquivo
2. Usar caminho relativo a partir do diretorio atual
3. Usar tab-completion se disponivel

---

### 5.2. Arquivo Muito Grande

**Aviso:**
```
⚠️ Arquivo muito grande (5000+ linhas). Analise pode demorar.
```

**Causa:** Arquivo fonte muito extenso.

**Solucao:**
- Especificar partes especificas do arquivo
- Usar `--lines 1-500` para limitar analise
- Extrair de multiplos arquivos menores

---

### 5.3. Nenhum Padrao Detectado

**Aviso:**
```
⚠️ Poucos padroes detectados no arquivo
```

**Causa:** Arquivo nao tem padroes claros para extrair.

**Solucao:**
- Verificar se arquivo e adequado para extracao
- Usar `/hefesto.create` ao inves de `/hefesto.extract`
- Combinar multiplos arquivos para mais contexto

---

## 6. Perguntas Frequentes

### Como resetar uma skill?

```
# Deletar manualmente
rm -rf .claude/skills/code-review/

# Ou usar Hefesto
/hefesto.delete code-review
```

### Como ver o que foi gerado?

```
# Listar skills
/hefesto.list

# Ver detalhes de uma skill
/hefesto.show code-review
```

### Como atualizar Hefesto?

Skills sao arquivos Markdown, nao ha "instalacao" do Hefesto. Para atualizar templates:
1. Baixar novos templates
2. Substituir em `templates/`

### Como reportar bug?

1. Usar `/hefesto.bug` para gerar relatorio
2. Ou criar issue em github.com/hefesto/issues

---

## 7. Contato e Suporte

- Documentacao: README.md
- Issues: docs/cards/ (criar CARD)
- Exemplos: .context/examples/

---

**Ultima Atualizacao:** 2026-02-04
