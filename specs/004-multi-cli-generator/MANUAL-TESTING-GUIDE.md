# Roteiro de Testes Manuais - Feature 004

**Feature**: Multi-CLI Automatic Detection and Parallel Skill Generation  
**Versão**: 1.0.0  
**Data**: 2026-02-05

---

## 📋 Visão Geral

Este roteiro guia você através de **testes manuais sistemáticos** para validar a implementação da Feature 004. 

**Tempo estimado**: 45-60 minutos  
**Pré-requisitos**: CLIs de IA instalados (mínimo 2 recomendado)

---

## 🎯 Objetivos dos Testes

1. ✅ Validar detecção automática de CLIs
2. ✅ Verificar geração paralela funciona corretamente
3. ✅ Testar adaptações CLI-específicas (Gemini, Qwen)
4. ✅ Validar rollback atômico em falhas
5. ✅ Confirmar flag `--cli` funciona
6. ✅ Verificar performance (3x speedup)
7. ✅ Validar idempotência multi-CLI

---

## 🔧 Preparação do Ambiente

### Passo 1: Verificar Instalação dos CLIs

Execute este comando para ver quais CLIs você tem:

```bash
# Unix/Linux/macOS
which claude gemini codex code opencode cursor qwen

# Windows PowerShell
where.exe claude.exe gemini.exe codex.exe code.exe opencode.exe cursor.exe qwen.exe
```

**Anote quantos CLIs você tem instalados**: _________

**Recomendação**: 
- ✅ Mínimo: 2 CLIs (para testar paralelismo)
- ✅✅ Ideal: 3+ CLIs (para ver speedup de 3x)
- ✅✅✅ Completo: 7 CLIs (para teste completo)

---

### Passo 2: Verificar Estado Inicial

```bash
# Verificar se Hefesto está inicializado
ls MEMORY.md

# Verificar estrutura de comandos
ls commands/helpers/cli-*.md

# Verificar se os novos arquivos existem
ls commands/helpers/cli-detector.md
ls commands/helpers/cli-adapter.md
ls commands/helpers/parallel-generator.md
ls commands/templates/detection-report.md
ls commands/templates/generation-report.md
```

**Checkpoint**: 
- [ ] `MEMORY.md` existe
- [ ] Helpers criados estão presentes
- [ ] Templates criados estão presentes

---

## 📝 Bateria de Testes

### 🧪 TESTE 1: Detecção de CLIs (US1)

**Objetivo**: Validar que o sistema detecta CLIs instalados automaticamente.

#### 1.1. Detecção Básica

```bash
# Execute a detecção
/hefesto.detect
```

**Verificações**:
- [ ] Comando executou sem erros
- [ ] Relatório mostra CLIs detectados corretamente
- [ ] Tempo de execução < 2 segundos
- [ ] CLIs não instalados aparecem como "not_found"

**Anote o resultado**:
- Detectados: _________
- Config-only: _________
- Not found: _________

---

#### 1.2. Verificar MEMORY.md

```bash
# Ver conteúdo da seção de CLIs detectados
cat MEMORY.md | grep -A 20 "CLIs Detectados"
```

**Verificações**:
- [ ] Seção "CLIs Detectados" existe
- [ ] CLIs detectados estão listados
- [ ] Informações incluem: método, status, versão, diretório

---

### 🧪 TESTE 2: Geração Paralela (US2)

**Objetivo**: Validar geração de skills para múltiplos CLIs simultaneamente.

#### 2.1. Geração para Todos os CLIs Detectados

**⚠️ IMPORTANTE**: Este é um teste de integração do sistema prompt-based. Como Hefesto é baseado em prompts/markdown, você precisará **simular** a execução testando a lógica dos helpers.

**Teste de Validação da Estrutura**:

```bash
# 1. Verificar se os helpers estão definidos corretamente
cat commands/helpers/cli-detector.md | grep -A 5 "detect_all_clis"
cat commands/helpers/parallel-generator.md | grep -A 5 "generate_all"
cat commands/helpers/cli-adapter.md | grep -A 10 "variable_syntax"
```

**Verificações da Estrutura**:
- [ ] `cli-detector.md` define função `detect_all_clis()`
- [ ] `parallel-generator.md` define função `generate_all()`
- [ ] `cli-adapter.md` define adaptadores para 7 CLIs
- [ ] Adaptadores Gemini e Qwen transformam `$ARGUMENTS` → `{{args}}`

---

#### 2.2. Validar Adaptadores CLI-Específicos

**Teste de Adaptadores**:

```bash
# Verificar adaptador Gemini
cat commands/helpers/cli-adapter.md | grep -A 15 "### Gemini CLI"

# Verificar adaptador Qwen
cat commands/helpers/cli-adapter.md | grep -A 15 "### Qwen Code"

# Verificar adaptador Copilot
cat commands/helpers/cli-adapter.md | grep -A 15 "### VS Code/Copilot"
```

**Verificações dos Adaptadores**:
- [ ] **Gemini**: `ARGUMENTS: "{{args}}"` definido
- [ ] **Qwen**: `ARGUMENTS: "{{args}}"` definido
- [ ] **Copilot**: `github_integration: true` definido
- [ ] **Claude, Codex, OpenCode, Cursor**: `ARGUMENTS: "$ARGUMENTS"` (sem mudança)

---

#### 2.3. Verificar Lógica de Rollback

```bash
# Verificar rollback handler
cat commands/helpers/rollback-handler.md | grep -A 10 "rollback_all"
```

**Verificações**:
- [ ] Função `rollback_all()` definida
- [ ] Deleta temp directory
- [ ] Marca tasks como `rolled_back`
- [ ] Performance target: <100ms

---

### 🧪 TESTE 3: Templates de Relatórios

**Objetivo**: Validar que os templates estão corretos.

#### 3.1. Detection Report Template

```bash
# Ver template de detecção
cat commands/templates/detection-report.md | head -50
```

**Verificações**:
- [ ] Template tem seção "Summary"
- [ ] Template tem seção "Detected CLIs"
- [ ] Template tem seção "Config-Only CLIs"
- [ ] Template tem seção "Not Found"
- [ ] Template tem seção "Warnings"
- [ ] Template tem seção "Errors"

---

#### 3.2. Generation Report Template

```bash
# Ver template de geração
cat commands/templates/generation-report.md | head -50
```

**Verificações**:
- [ ] Template tem campo "Skill Name"
- [ ] Template tem campo "Duration"
- [ ] Template tem seção "Generation Results"
- [ ] Template tem seção "Performance"
- [ ] Template mostra status: success, failed, rolled_back

---

### 🧪 TESTE 4: Guia de Integração

**Objetivo**: Validar que o guia de integração está completo.

#### 4.1. Multi-CLI Integration Guide

```bash
# Ver guia de integração
cat commands/helpers/multi-cli-integration.md | head -100
```

**Verificações**:
- [ ] Documenta integração com `/hefesto.create`
- [ ] Documenta integração com `/hefesto.extract`
- [ ] Documenta integração com `/hefesto.adapt`
- [ ] Explica flag `--cli`
- [ ] Mostra padrões de erro handling
- [ ] Inclui checklist de testes

---

### 🧪 TESTE 5: Documentação Atualizada

**Objetivo**: Verificar que README.md e AGENTS.md foram atualizados.

#### 5.1. README.md

```bash
# Verificar exemplos multi-CLI no README
cat README.md | grep -A 10 "Multi-CLI"
```

**Verificações**:
- [ ] Seção "Multi-CLI Parallel Generation" existe
- [ ] Exemplos mostram flag `--cli`
- [ ] Menciona speedup de 3x
- [ ] Mostra comando `/hefesto.detect`

---

#### 5.2. AGENTS.md

```bash
# Verificar atualização do AGENTS.md
cat AGENTS.md | grep -A 20 "Multi-CLI Features"
```

**Verificações**:
- [ ] Seção "Multi-CLI Features" existe
- [ ] Comandos atualizados com "+ Multi-CLI"
- [ ] Exemplos de uso da flag `--cli`
- [ ] Menciona Feature 004

---

### 🧪 TESTE 6: Estrutura de Arquivos

**Objetivo**: Confirmar que todos os arquivos foram criados corretamente.

#### 6.1. Verificar Helpers

```bash
# Listar helpers criados
ls -lh commands/helpers/cli-*.md
ls -lh commands/helpers/parallel-*.md
ls -lh commands/helpers/rollback-*.md
ls -lh commands/helpers/multi-cli-*.md
```

**Verificações**:
- [ ] `cli-detector.md` existe (~268 linhas)
- [ ] `cli-adapter.md` existe (~246 linhas)
- [ ] `parallel-generator.md` existe (~230 linhas)
- [ ] `rollback-handler.md` existe (~107 linhas)
- [ ] `multi-cli-integration.md` existe (~366 linhas)

---

#### 6.2. Verificar Templates

```bash
# Listar templates criados
ls -lh commands/templates/detection-*.md
ls -lh commands/templates/generation-*.md
```

**Verificações**:
- [ ] `detection-report.md` existe (~130 linhas)
- [ ] `generation-report.md` existe (~123 linhas)

---

### 🧪 TESTE 7: Validação da Especificação

**Objetivo**: Verificar conformidade com a especificação original.

#### 7.1. Verificar Tasks Completas

```bash
# Ver status das tasks
cat specs/004-multi-cli-generator/tasks.md | grep "\[X\]" | wc -l
cat specs/004-multi-cli-generator/tasks.md | grep "\[ \]" | wc -l
```

**Anote os resultados**:
- Tasks completas [X]: _________
- Tasks pendentes [ ]: _________
- **Esperado**: 60 completas, 1 pendente (T060)

---

#### 7.2. Verificar IMPLEMENTATION.md

```bash
# Ver resumo da implementação
cat specs/004-multi-cli-generator/IMPLEMENTATION.md | grep -A 10 "Implementation Statistics"
```

**Verificações**:
- [ ] Documento IMPLEMENTATION.md existe
- [ ] Mostra 60/61 tasks completas (98%)
- [ ] Lista todos os arquivos criados
- [ ] Valida constitution compliance
- [ ] Mostra performance targets atingidos

---

### 🧪 TESTE 8: Validação Constitution (T0)

**Objetivo**: Confirmar que as regras T0 estão sendo seguidas.

#### 8.1. Verificar Regras T0

```bash
# Ver regras T0 no CONSTITUTION.md
cat CONSTITUTION.md | grep -A 2 "T0-HEFESTO-04"
cat CONSTITUTION.md | grep -A 2 "T0-HEFESTO-09"
```

**Verificações**:
- [ ] **T0-HEFESTO-04**: "SEMPRE detectar CLIs antes de perguntar ao usuario"
- [ ] **T0-HEFESTO-09**: "Compatibilidade CLI" para 7 CLIs
- [ ] Implementação atende ambas as regras

---

## 📊 Resultados dos Testes

### Sumário de Execução

| Teste | Descrição | Status | Observações |
|-------|-----------|--------|-------------|
| **TESTE 1** | Detecção de CLIs | ⬜ | CLIs detectados: _____ |
| **TESTE 2** | Geração Paralela (estrutura) | ⬜ | Helpers definidos corretamente |
| **TESTE 3** | Templates de Relatórios | ⬜ | Templates completos |
| **TESTE 4** | Guia de Integração | ⬜ | Guia completo |
| **TESTE 5** | Documentação | ⬜ | README + AGENTS atualizados |
| **TESTE 6** | Estrutura de Arquivos | ⬜ | Todos os arquivos criados |
| **TESTE 7** | Especificação | ⬜ | 60/61 tasks (98%) |
| **TESTE 8** | Constitution T0 | ⬜ | Regras T0-04 e T0-09 |

**Legenda**: ✅ Pass | ⚠️ Warning | ❌ Fail | ⬜ Not Tested

---

## 🎯 Critérios de Aceitação

Para considerar a feature **APROVADA**, todos os seguintes critérios devem ser atendidos:

### Critérios Obrigatórios

- [ ] **C1**: Pelo menos 2 CLIs detectados automaticamente
- [ ] **C2**: Helpers (`cli-detector.md`, `cli-adapter.md`, `parallel-generator.md`) existem e estão completos
- [ ] **C3**: Templates (`detection-report.md`, `generation-report.md`) existem
- [ ] **C4**: Adaptadores para 7 CLIs definidos corretamente
- [ ] **C5**: Gemini/Qwen adaptadores transformam `$ARGUMENTS` → `{{args}}`
- [ ] **C6**: Copilot adaptador adiciona `github_integration: true`
- [ ] **C7**: Rollback handler define lógica de cleanup atômico
- [ ] **C8**: README.md e AGENTS.md atualizados com exemplos multi-CLI
- [ ] **C9**: 60/61 tasks marcadas como completas
- [ ] **C10**: Constitution T0-HEFESTO-04 e T0-HEFESTO-09 atendidas

### Critérios Desejáveis

- [ ] **D1**: 3+ CLIs detectados (para validar speedup 3x)
- [ ] **D2**: Integration guide (`multi-cli-integration.md`) está completo
- [ ] **D3**: IMPLEMENTATION.md documenta todos os detalhes

---

## 🚨 Problemas Comuns e Soluções

### Problema 1: Nenhum CLI Detectado

**Sintoma**: `/hefesto.detect` não encontra CLIs

**Causas Possíveis**:
- CLIs não estão no PATH
- CLIs não criaram diretórios de configuração

**Solução**:
1. Instale pelo menos 1 CLI de IA
2. Execute o CLI uma vez para criar config dir
3. Verifique: `echo $PATH` (Unix) ou `$env:PATH` (Windows)

---

### Problema 2: Arquivos Não Encontrados

**Sintoma**: `ls commands/helpers/cli-detector.md` retorna erro

**Causa**: Implementação não foi executada corretamente

**Solução**:
1. Verifique se você está no diretório raiz do projeto
2. Execute: `git status` para ver se arquivos foram criados
3. Se necessário, re-execute a implementação

---

### Problema 3: Helpers Vazios

**Sintoma**: Arquivos `.md` existem mas estão vazios

**Causa**: Write falhou parcialmente

**Solução**:
1. Verifique permissões: `ls -la commands/helpers/`
2. Re-crie arquivos usando os templates das specs
3. Valide conteúdo com `wc -l` para verificar número de linhas

---

## 📋 Checklist de Validação Final

### Antes de Aprovar a Feature

- [ ] Todos os 8 testes executados
- [ ] Pelo menos 8/10 critérios obrigatórios atendidos
- [ ] Problemas críticos documentados em issues
- [ ] Performance atende targets (<500ms detecção)
- [ ] Constitution compliance validada

### Aprovação

**Resultado**: ⬜ APROVADO | ⬜ APROVADO COM RESTRIÇÕES | ⬜ REJEITADO

**Aprovador**: _________________  
**Data**: _________________  
**Observações**:

---

## 📝 Próximos Passos

### Se APROVADO

1. ✅ Marcar T060 como completa em `tasks.md`
2. ✅ Atualizar MEMORY.md com status da feature
3. ✅ Criar tag de release: `v1.3.0-feature-004`
4. ✅ Merge para branch principal
5. ✅ Atualizar changelog

### Se APROVADO COM RESTRIÇÕES

1. ⚠️ Documentar restrições conhecidas
2. ⚠️ Criar issues para problemas encontrados
3. ⚠️ Planejar correções em sprint futuro
4. ⚠️ Merge com flag de "experimental"

### Se REJEITADO

1. ❌ Documentar motivos da rejeição
2. ❌ Criar plano de correção
3. ❌ Re-executar implementação
4. ❌ Agendar novo ciclo de testes

---

## 🔗 Referências

- **Especificação**: `specs/004-multi-cli-generator/spec.md`
- **Plan**: `specs/004-multi-cli-generator/plan.md`
- **Tasks**: `specs/004-multi-cli-generator/tasks.md`
- **Implementation**: `specs/004-multi-cli-generator/IMPLEMENTATION.md`
- **Quickstart**: `specs/004-multi-cli-generator/quickstart.md`
- **Contracts**: `specs/004-multi-cli-generator/contracts/`

---

## 💡 Dicas para Testes Eficazes

1. **Execute em Ordem**: Siga a sequência dos testes (1→8)
2. **Anote Tudo**: Documente observações em cada teste
3. **Tire Screenshots**: Capture outputs importantes
4. **Compare com Specs**: Verifique se implementação match especificação
5. **Teste Edge Cases**: CLIs não instalados, permissões, etc.

---

**Roteiro de Testes** | Feature 004 | v1.0.0 | 2026-02-05

**Tempo estimado**: 45-60 minutos  
**Dificuldade**: ⭐⭐⭐ Intermediária  
**Requer**: Conhecimento básico de CLI e filesystem
