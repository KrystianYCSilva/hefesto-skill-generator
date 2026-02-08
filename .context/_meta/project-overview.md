# Project Overview - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 2.0.0

---

## 1. Visao Geral

**Hefesto Skill Generator** e um spec-kit template-driven que gera Agent Skills para 7 CLIs de IA. Zero Python, zero dependencias - toda logica vive em Markdown templates.

Named after the Greek god of the forge, Hefesto crafts specialized tools (skills) that empower AI agents.

### Problema que Resolve

- Desenvolvedores precisam criar skills manualmente para cada CLI
- Nao ha padronizacao entre diferentes ferramentas de IA
- Dificuldade em manter skills sincronizadas entre CLIs
- Falta de validacao automatica contra especificacoes

### Solucao

Sistema que:
1. Gera skills a partir de descricao natural ou codigo existente
2. Valida automaticamente contra Agent Skills spec (13-point checklist)
3. Detecta CLIs instalados automaticamente
4. Gera skills para todos os CLIs detectados
5. Aplica Human Gate para controle de qualidade
6. Pode corrigir problemas automaticamente (fix-auto)

---

## 2. Escopo

### Dentro do Escopo

- Geracao de skills seguindo Agent Skills spec (agentskills.io)
- Suporte a 7 CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen)
- Validacao + correcao automatica contra spec
- Deteccao automatica de CLIs
- Human Gate para aprovacao
- Extracao de skills de codigo existente
- Installer portatil (bash + PowerShell)

### Fora do Escopo

- Execucao de skills (responsabilidade dos CLIs)
- Hospedagem/distribuicao de skills
- IDE integrado
- Interface grafica (apenas CLI/chat)

---

## 3. Usuarios Alvo

| Persona | Necessidade | Uso Principal |
|---------|-------------|---------------|
| Desenvolvedor Individual | Criar skills pessoais | `/hefesto.create` |
| Time de Desenvolvimento | Padronizar skills do time | `/hefesto.create`, `/hefesto.validate` |
| Arquiteto de Software | Definir padroes de skills | `/hefesto.extract`, `/hefesto.validate` |

---

## 4. Principios de Design

### 4.1. Template-Driven (Zero Dependencies)
Toda logica em Markdown templates. Nenhuma dependencia de Python, Node.js, etc.

### 4.2. Agent Skills Standard First
Toda skill segue a especificacao agentskills.io.

### 4.3. Human-in-the-Loop
Nenhuma operacao de escrita ocorre sem aprovacao humana (Human Gate).

### 4.4. Multi-CLI por Padrao
Detectar e gerar para todos os CLIs instalados, nao apenas um.

### 4.5. Progressive Disclosure
Skills < 500 linhas, recursos adicionais em `references/`.

### 4.6. Token Economy
Frontmatter SOMENTE name + description. Body sem tutorials desnecessarios.

---

## 5. Comandos

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao natural | Sim |
| `/hefesto.validate` | Validar + corrigir skill | Sim (fix-auto) |
| `/hefesto.extract` | Extrair skill de codigo/docs | Sim |
| `/hefesto.init` | Bootstrap/verificar instalacao | Nao |
| `/hefesto.list` | Listar skills instaladas | Nao |

---

## 6. Instalacao

### Via Installer Script

```bash
# Unix/macOS
cd installer && bash install.sh

# Windows PowerShell
cd installer; .\install.ps1
```

### Via GitHub Release

```bash
curl -fsSL https://github.com/<org>/hefesto-skill-generator/releases/latest/download/hefesto-latest.tar.gz | tar xz
cd installer && bash install.sh
```

O installer:
1. Detecta CLIs instalados (PATH + diretorios)
2. Cria `.hefesto/` com templates e versao
3. Copia comandos `hefesto.*` para cada CLI
4. Cria diretorios `skills/`

---

**Ultima Atualizacao:** 2026-02-07
