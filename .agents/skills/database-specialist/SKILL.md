---
name: database-specialist
description: |
  Orienta fundamentos e decisões práticas sobre bancos de dados, cobrindo modelagem relacional, SQL seguro, NoSQL e critérios de escolha.
  Use when: o usuário pede explicações, comparativos, boas práticas, erros comuns ou ajuda para escolher/modelar SQL vs NoSQL.
---

# Database Specialist

Fornece orientação objetiva para explicar conceitos de bancos de dados, modelar esquemas e escolher entre SQL e NoSQL. Foca em decisões práticas, riscos comuns e boas práticas de uso.

## Instructions

### How to clarify goals and constraints
1. Identificar tipo de carga (OLTP, OLAP), padrões de acesso e volume.
2. Mapear requisitos de consistência, transações, latência e disponibilidade.
3. Considerar equipe, custos operacionais e requisitos regulatórios.

### How to explain what a database is and why it exists
- Definir como sistema para armazenar, consultar e proteger dados com integridade e desempenho.
- Explicar o trade-off entre consistência, disponibilidade, latência e custo.

### How to model relational data and DER (ERD)
1. Identificar entidades, atributos e relacionamentos.
2. Definir chaves primárias, estrangeiras e cardinalidades.
3. Normalizar até o nível necessário para evitar redundância crítica.
4. Representar tudo em um DER/ERD para comunicação e validação.

### How to build a relational database schema
1. Escolher o SGBD e padrões de nomenclatura.
2. Criar tabelas com PK, FK e constraints de domínio.
3. Projetar índices para caminhos de consulta principais.
4. Validar com dados mínimos e consultas representativas.

### How to use SQL safely and correctly
- Preferir queries parametrizadas para evitar SQL injection.
- Usar transações para operações multi-passos.
- Evitar `SELECT *` em produção.
- Usar `EXPLAIN` para validar planos de execução.
- Tratar `NULL` de forma explícita.

### How to avoid common SQL mistakes
- `UPDATE`/`DELETE` sem `WHERE`.
- `JOIN` implícito ou com condição incompleta.
- Consultas sem limite em tabelas grandes.
- Índices em excesso ou mal alinhados com consultas.
- Tipos de dados inconsistentes entre tabelas.

### How to model NoSQL data
1. Partir dos padrões de acesso e consultas críticas.
2. Denormalizar de forma intencional e documentada.
3. Escolher o modelo adequado: chave-valor, documento, colunar, grafo.
4. Definir estratégia de particionamento e cardinalidade.

### How to use NoSQL safely
- Projetar com consistência eventual quando aceitável.
- Garantir idempotência em operações distribuídas.
- Versionar esquemas e documentos.
- Monitorar hotspots e chaves “quentes”.

### How to avoid common NoSQL mistakes
- Tratar NoSQL como relacional e forçar joins.
- Documentos sem limites de crescimento.
- Chaves de partição com baixa cardinalidade.
- Ignorar SLAs de consistência do negócio.

### How to compare SQL vs NoSQL and choose
1. Usar SQL quando integridade forte, joins complexos e transações ACID são críticas.
2. Usar NoSQL quando escala horizontal, flexibilidade de esquema e baixa latência são prioritárias.
3. Validar a escolha com protótipo focado nas consultas principais.

## Key Concepts

| Concept | Notes |
| --- | --- |
| Banco de dados relacional | Modelo tabular com relações e constraints. |
| DER / ERD | Diagrama para entidades, atributos e relações. |
| ACID | Atomicidade, Consistência, Isolamento, Durabilidade. |
| Normalização | Reduz redundância e anomalias de atualização. |
| NoSQL | Família de modelos não-relacionais. |
| CAP | Trade-off entre consistência, disponibilidade e tolerância a particionamento. |
| Indexação | Estruturas para acelerar consultas em troca de custo de escrita. |

## Examples

### Example 1: Escolha entre SQL e NoSQL

**Input:**  
“Preciso de um sistema de pedidos com pagamentos, regras de integridade e relatórios financeiros. Tráfego moderado e equipe pequena.”

**Output:**  
“SQL é mais adequado: exige transações e integridade forte, com joins e relatórios consistentes. Priorize um SGBD relacional e modele entidades com DER.”

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Reference Manual](https://dev.mysql.com/doc/)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
