# CARD-009: /hefesto.extract - Extração de Skills de Código

## 1. Descrição & User Story

"Como um **desenvolvedor com código existente**, eu quero **extrair Agent Skills de arquivos de código** através do comando `/hefesto.extract`, para que eu possa **reutilizar scripts e ferramentas** sem reescrever tudo do zero."

---

## 2. Regras de Negócio (RN)

* [RN01] DEVE analisar arquivos de código (.py, .js, .ts, .sh, .java, .go, etc.)
* [RN02] DEVE gerar wrapper SKILL.md com metadados inferidos
* [RN03] DEVE copiar código original para scripts/ directory
* [RN04] DEVE detectar e rejeitar arquivos com secrets/credentials
* [RN05] DEVE suportar Wizard Mode quando file_path omitido

---

## 3. Regras Técnicas (RT)

### RT01: Análise de Código
- Detectar linguagem (extensão + shebang)
- Identificar framework (import statements)
- Inferir propósito (função main, comentários)
- Detectar dependencies (import/require/use)
- Validar segurança (T0-HEFESTO-11)

### RT02: Estrutura Gerada
```
.{cli}/skills/{skill-name}/
├── SKILL.md              # Wrapper com instruções
├── metadata.yaml         # Metadados JIT
└── scripts/
    └── {original-file}   # Código extraído
```

### RT03: Fluxo de Execução
1. Parse arguments (file_path, --target, --name)
2. Se file_path vazio → Wizard Mode
3. Validar arquivo existe e é legível
4. Análise de código (linguagem, framework, propósito)
5. Security scan (detectar secrets - ABORT se encontrar)
6. Gerar skill name (sanitize basename ou --name)
7. Collision detection (usar Human Gate de CARD-005)
8. Gerar SKILL.md wrapper
9. Validar contra Agent Skills spec
10. Human Gate (preview + approval)
11. Persistir atomicamente (SKILL.md + scripts/)
12. Multi-CLI parallel generation (Feature 004)

### RT04: Wizard Mode Steps
- Step 1: File path ou paste code?
- Step 2: Custom skill name? (default: sanitized filename)
- Step 3: Custom description? (default: inferido)
- Step 4: Target CLIs? (default: all detected)
- Step 5: Review + Human Gate

### RT05: Security Validation (T0-HEFESTO-11)
- Regex para API keys, tokens, passwords
- Check hardcoded credentials
- Se detectado → ABORT com sugestão de environment vars

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] Performance: < 7s (excluindo Human Gate wait)
* [RQ02] Suportar 20+ linguagens populares
* [RQ03] Security scan: 99% detecção de secrets comuns
* [RQ04] Wizard Mode: mesma UX de /hefesto.create

---

## 5. Critérios de Aceite

- [ ] Comando `/hefesto.extract <file>` funcional
- [ ] Wizard Mode ativado quando file_path omitido
- [ ] Análise de código infere linguagem/framework
- [ ] Security scan rejeita arquivos com secrets
- [ ] Skill wrapper gerado com metadados corretos
- [ ] Código original copiado para scripts/
- [ ] Human Gate integrado (CARD-005)
- [ ] Multi-CLI parallel generation (CARD-004)
- [ ] Collision detection funcional
- [ ] Atomic rollback em caso de falha

---

## 6. Tarefas (Sub-Tasks)

### Phase 1: Code Analysis Engine (8h)
- [ ] T001: Criar `commands/lib/code_analyzer.py`
- [ ] T002: Criar `commands/lib/security_scanner.py`

### Phase 2: Extract Implementation (12h)
- [ ] T003: Criar `commands/hefesto_extract_impl.py`
- [ ] T004: Integrar code_analyzer
- [ ] T005: Integrar security_scanner

### Phase 3: Skill Generation (8h)
- [ ] T006: Criar template `templates/extract/SKILL.md.template`
- [ ] T007: Implementar skill wrapper generation
- [ ] T008: Implementar sanitização de skill name

### Phase 4: Integration (6h)
- [ ] T009: Integrar Human Gate (CARD-005)
- [ ] T010: Integrar Collision Detection (CARD-005)
- [ ] T011: Integrar Multi-CLI Generation (CARD-004)
- [ ] T012: Integrar Wizard Mode (CARD-005)

### Phase 5: Testing & Documentation (6h)
- [ ] T013: Testes unitários
- [ ] T014: Testes de integração
- [ ] T015: Atualizar documentação

---

## 7. Dependências

| CARD | Descrição | Status | Necessário Para |
|------|-----------|--------|-----------------|
| CARD-001 | Foundation | ✅ Complete | CLI detection, file structure |
| CARD-002 | Templates | ✅ Complete | Template rendering |
| CARD-003 | Commands | ⚠️ Partial | Command structure (extract.md exists) |
| CARD-004 | Multi-CLI | ✅ Complete | Parallel generation |
| CARD-005 | Human Gate | ✅ Complete | Approval workflow, Wizard, Collision |

**Status**: Pode começar imediatamente - todas dependências satisfeitas.

---

## 8. Complexidade & Estimativa

| Componente | Complexidade | Tempo | Justificativa |
|------------|--------------|-------|---------------|
| Code Analyzer | **Alta** | 8h | Suportar 20+ linguagens, parsing robusto |
| Security Scanner | **Média** | 4h | Regex patterns + logging |
| Extract Implementation | **Média** | 8h | Integração com libs existentes |
| Skill Generation | **Baixa** | 4h | Template rendering simples |
| Integration | **Baixa** | 6h | Libs já existem (CARD-005, 004) |
| Testing | **Média** | 6h | Coverage de múltiplas linguagens |

**Total**: **36h** (4.5 dias - 1 sprint)

---

## 9. Riscos & Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| False positives em security scan | Média | Baixo | Whitelist de patterns seguros |
| Linguagens não suportadas | Alta | Baixo | Generic fallback (treat as script) |
| Código muito grande para scripts/ | Baixa | Médio | Validar size < 100KB, suggest splitting |
| Framework detection impreciso | Média | Baixo | Permitir override manual no Wizard |

---

## 10. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | 🔴 **NOT STARTED** |
| **Prioridade** | **P2** (após Feature 005 complete) |
| **Estimativa** | 36h (4.5 dias) |
| **Assignee** | AI Agent |
| **Dependências** | CARD-005 (✅), CARD-004 (✅) |
| **Bloqueadores** | Nenhum |
| **Sprint** | Next (após Feature 005 testes) |
| **Related Issues** | T020 (Wizard em extract - tasks.md) |

---

## 11. Definition of Done

- [ ] `hefesto_extract_impl.py` criado e funcional
- [ ] `code_analyzer.py` suporta 20+ linguagens
- [ ] `security_scanner.py` detecta 20 secret patterns
- [ ] Template `extract/SKILL.md.template` criado
- [ ] Human Gate integrado (preview + approval)
- [ ] Wizard Mode integrado (4 steps)
- [ ] Collision detection integrado
- [ ] Multi-CLI generation integrado
- [ ] 15 unit tests escritos e passando
- [ ] 5 integration tests escritos e passando
- [ ] Documentação atualizada (AGENTS.md, MEMORY.md)
- [ ] Quickstart examples criados
- [ ] Manual testing completo (10 linguagens testadas)
- [ ] CARD-009 marcado como ✅ COMPLETE

---

**Created**: 2026-02-05  
**Last Updated**: 2026-02-05  
**Version**: 1.0.0
