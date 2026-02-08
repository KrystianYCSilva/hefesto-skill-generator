# Troubleshooting - Foundation Issues

> **Tier:** T2 - Informativo
> **Proposito:** Resolver problemas de infraestrutura do Hefesto
> **Versao:** 2.0.0

---

## Quick Diagnostics

```bash
# 1. Verificar instalacao
/hefesto.init

# 2. Listar skills
/hefesto.list

# 3. Verificar versao
cat .hefesto/version
```

---

## Common Issues

### Issue 1: "Hefesto not installed"

**Sintomas:**
- Nao existe `.hefesto/` no projeto
- Comandos `/hefesto.*` nao disponiveis

**Causa:** Hefesto nao foi instalado no projeto.

**Solucao:**
```bash
# Unix/macOS
bash /caminho/para/hefesto-skill-generator/installer/install.sh

# Windows PowerShell
& /caminho/para/hefesto-skill-generator/installer/install.ps1
```

---

### Issue 2: "No CLIs detected"

**Sintomas:**
- `/hefesto.init` reporta 0 CLIs encontrados
- Nenhum diretorio CLI criado

**Causa:** Nenhum AI CLI instalado ou no PATH.

**Solucao:**
```bash
# Verificar CLIs (Unix/macOS)
which claude gemini codex opencode qwen

# Windows
where.exe claude
```

Se nenhum CLI encontrado, o installer cria `.claude/` como default.

---

### Issue 3: Permission Denied

**Sintomas:**
- Erro ao criar diretorios
- Installer falha parcialmente

**Solucao:**
```bash
# Verificar permissoes
ls -la .

# Corrigir (Unix/macOS)
chmod +w .
```

---

### Issue 4: Templates Desatualizados

**Sintomas:**
- `.hefesto/version` mostra versao antiga
- Skills geradas com formato antigo

**Solucao:**
```bash
# Re-rodar installer (idempotente)
bash /caminho/para/installer/install.sh

# Templates serao atualizados em .hefesto/templates/
```

---

### Issue 5: Comandos Faltando em Algum CLI

**Sintomas:**
- CLI detectado mas sem comandos `hefesto.*`
- `/hefesto.list` funciona em um CLI mas nao em outro

**Causa:** Installer pode nao ter detectado o CLI na primeira execucao.

**Solucao:**
```bash
# Re-rodar installer (detecta CLIs novos)
bash /caminho/para/installer/install.sh
```

---

### Issue 6: Skills Dessincronizadas Entre CLIs

**Sintomas:**
- Skill existe em `.claude/skills/` mas nao em `.gemini/skills/`
- Versoes diferentes entre CLIs

**Causa:** Skill criada/modificada manualmente em apenas um CLI.

**Solucao:**
```bash
# Re-criar skill (gera para todos CLIs)
/hefesto.create "descricao da skill"

# Ou validar (fix-auto sincroniza)
/hefesto.validate skill-name
```

---

## Platform-Specific Issues

### Windows

**Issue:** PowerShell execution policy

```powershell
# Verificar
Get-ExecutionPolicy

# Corrigir (sessao atual)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Ou para usuario
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### macOS

**Issue:** CLI instalado via Homebrew nao detectado

```bash
# Verificar Homebrew path
echo $PATH | grep homebrew

# Adicionar se necessario
export PATH="/opt/homebrew/bin:$PATH"  # Apple Silicon
```

---

## Prevention Best Practices

1. **Sempre usar installer:** `install.sh` ou `install.ps1` ao inves de criar diretorios manualmente
2. **Usar comandos Hefesto:** Nao editar skills manualmente, usar `/hefesto.create` e `/hefesto.validate`
3. **Verificar instalacao:** Rodar `/hefesto.init` periodicamente
4. **Manter CLIs no PATH:** Garante deteccao automatica
5. **Nao editar `.hefesto/`:** Diretorio gerenciado pelo installer

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)
