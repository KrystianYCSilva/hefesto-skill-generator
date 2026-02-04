# Project Overview - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 1.0.0

---

## 1. Visao Geral

**Hefesto Skill Generator** e um sistema de geracao de Agent Skills padronizadas para multiplos CLIs de IA.

### Missao

Simplificar a criacao de skills reutilizaveis que funcionam em qualquer CLI de IA compativel com o padrao [agentskills.io](https://agentskills.io).

### Problema que Resolve

- Desenvolvedores precisam criar skills manualmente para cada CLI
- Nao ha padronizacao entre diferentes ferramentas de IA
- Dificuldade em manter skills sincronizadas entre CLIs
- Falta de validacao automatica contra especificacoes

### Solucao

Sistema que:
1. Gera skills a partir de descricao natural ou codigo existente
2. Valida automaticamente contra Agent Skills spec
3. Detecta CLIs instalados e gera para todos
4. Aplica Human Gate para controle de qualidade
5. Mantem skills sincronizadas entre CLIs

---

## 2. Escopo

### Dentro do Escopo

- Geracao de skills seguindo Agent Skills spec
- Suporte a multiplos CLIs (Claude, Gemini, Codex, Copilot, etc.)
- Validacao contra especificacao
- Deteccao automatica de CLIs
- Human Gate para aprovacao
- Wizard interativo para expansao
- Extracao de skills de codigo existente

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
| Time de Desenvolvimento | Padronizar skills do time | `/hefesto.create`, `/hefesto.sync` |
| Arquiteto de Software | Definir padroes de skills | `/hefesto.extract`, `/hefesto.validate` |
| DevOps | Automatizar workflows | `/hefesto.extract` |

---

## 4. Principios de Design

### 4.1. Agent Skills Standard First

Toda skill gerada segue a especificacao [agentskills.io](https://agentskills.io) como formato primario.

### 4.2. Human-in-the-Loop

Nenhuma operacao de escrita ocorre sem aprovacao humana explicita (Human Gate).

### 4.3. Multi-CLI por Padrao

Detectar e gerar para todos os CLIs instalados, nao apenas um.

### 4.4. Template-First, Expand on Demand

Comecar com template basico, expandir via wizard quando necessario.

### 4.5. Progressive Disclosure

Skills principais < 500 linhas, recursos adicionais em sub-arquivos JIT.

---

## 5. Metricas de Sucesso

| Metrica | Alvo |
|---------|------|
| Skills validas geradas | 100% passam validacao |
| CLIs suportados | >= 7 |
| Tempo de geracao | < 30 segundos |
| Taxa de aprovacao Human Gate | >= 80% na primeira tentativa |

---

## 6. Riscos e Mitigacoes

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Spec Agent Skills muda | Media | Alto | Abstrair spec em knowledge/ |
| CLI nao detectado | Baixa | Medio | Perguntar ao usuario |
| Skill muito complexa | Media | Medio | Wizard para expansao |
| Conflito entre CLIs | Baixa | Alto | Adapters especificos |

---

## 7. Timeline de Implementacao

| Fase | Descricao | Duracao |
|------|-----------|---------|
| 1 | Foundation (estrutura, templates) | 1-2 dias |
| 2 | Multi-CLI (adapters, deteccao) | 2-3 dias |
| 3 | Human Gate + Wizard | 1-2 dias |
| 4 | Comandos Auxiliares | 1 dia |
| 5 | Knowledge Base + Docs | 1-2 dias |

**Total Estimado:** 6-10 dias

---

**Ultima Atualizacao:** 2026-02-04
