---
name: sql-specialist
description: |
  Ensina e orienta SQL do básico ao avançado para modelar, criar e operar bancos relacionais com segurança e desempenho.
  Use when: o usuário precisa criar bancos, escrever scripts SQL, modelar soluções relacionais, otimizar consultas ou evitar erros comuns.
---

# SQL Specialist

Fornece orientação prática para construir esquemas relacionais, escrever SQL correto e otimizar consultas. O foco é clareza, segurança e performance em ambientes reais.

## How to model relational schemas
- Definir entidades, atributos e relacionamentos antes de escrever DDL.
- Escolher chaves primárias estáveis e chaves estrangeiras consistentes.
- Normalizar até o nível necessário para evitar anomalias críticas.

## How to create tables and constraints (DDL)
- Preferir tipos de dados alinhados ao domínio (evitar “string para tudo”).
- Declarar `NOT NULL`, `UNIQUE`, `CHECK` e `FOREIGN KEY` desde o início.
- Definir índices básicos para chaves e filtros frequentes.

## How to write reliable SELECT queries
- Especificar colunas (evitar `SELECT *` em produção).
- Usar `JOIN` explícito com condições completas.
- Manter filtros e ordenação coerentes com índices.

## How to use aggregation and grouping
- Usar `GROUP BY` somente para colunas não agregadas.
- Validar cardinalidade antes de agregar para evitar duplicação.
- Preferir `HAVING` apenas para filtros pós-agregação.

## How to use subqueries, CTEs, and window functions
- Usar CTEs para legibilidade e refatoração.
- Usar `ROW_NUMBER`, `RANK`, `LAG/LEAD` para análises temporais.
- Evitar subqueries correlacionadas quando um `JOIN` resolver.

## How to manage transactions and isolation
- Agrupar operações relacionadas em transações curtas.
- Conhecer níveis de isolamento e impactos em bloqueios.
- Tratar falhas com `ROLLBACK` previsível.

## How to design indexes
- Indexar colunas usadas em `WHERE`, `JOIN`, `ORDER BY`.
- Evitar excesso de índices em tabelas de escrita intensa.
- Revisar planos com `EXPLAIN` antes de promover mudanças.

## How to optimize query performance
- Reduzir linhas cedo (filtros antes de `JOIN` quando possível).
- Inspecionar planos de execução e custos.
- Evitar funções em colunas indexadas no `WHERE`.

## How to write safe and maintainable SQL
- Usar queries parametrizadas para evitar SQL injection.
- Manter scripts idempotentes para migrações repetíveis.
- Organizar DDL/DML em ordem de dependência.

## How to avoid common SQL mistakes
- `UPDATE`/`DELETE` sem `WHERE`.
- `JOIN` com condição parcial.
- Inconsistência de tipos entre chaves.
- Índices que não refletem consultas reais.
- Misturar lógica de negócio complexa em SQL sem documentação.

## Examples

### Example 1: Window function para deduplicação

**Input:**  
“Preciso manter apenas o último registro por cliente.”

**Output:**  
“Use `ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY data DESC)` e filtre `row_number = 1`.”

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Reference Manual](https://dev.mysql.com/doc/)
- [Microsoft SQL Server Documentation](https://learn.microsoft.com/sql/)
