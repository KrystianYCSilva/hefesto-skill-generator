---
name: nosql-specialist
description: |
  Ensina e orienta NoSQL do basico ao avancado para modelar, criar e operar bancos nao-relacionais com seguranca e desempenho.
  Use when: o usuario precisa criar bancos NoSQL, escrever scripts, modelar solucoes, escolher modelos (documento, chave-valor, colunar, grafo) ou evitar erros comuns.
---

# NoSQL Specialist

Fornece orientacao pratica para escolher o modelo NoSQL adequado, modelar dados por padroes de acesso e operar com consistencia e performance.

## How to choose the NoSQL model
- Documento: dados semi-estruturados, leitura agregada por entidade.
- Chave-valor: cache, sessao, lookup rapido.
- Colunar: grandes volumes e queries analiticas em colunas.
- Grafo: relacionamentos complexos e caminhos.

## How to model NoSQL data by access patterns
- Partir das consultas mais criticas.
- Denormalizar de forma intencional e documentada.
- Evitar joins e garantir agregacao no mesmo documento quando possivel.

## How to design keys and partitioning
- Escolher chaves com alta cardinalidade.
- Evitar hotspots com distribuicao uniforme.
- Considerar range vs hash para padroes de leitura.

## How to handle consistency and durability
- Definir nivel de consistencia por operacao quando suportado.
- Usar idempotencia em escrita distribuida.
- Ajustar replicacao conforme RPO/RTO.

## How to design indexes in NoSQL
- Criar indices somente para queries confirmadas.
- Validar impacto em escrita e armazenamento.
- Evitar indices que nao refletem uso real.

## How to write efficient NoSQL queries
- Ler apenas campos necessarios.
- Evitar scans completos em colecoes grandes.
- Usar paginacao segura (por cursor) quando suportado.

## How to scale and operate NoSQL safely
- Dimensionar para crescimento horizontal.
- Monitorar latencia, throughput e tamanho de particoes.
- Definir politicas de TTL quando aplicavel.

## How to avoid common NoSQL mistakes
- Tratar NoSQL como relacional e forcar joins.
- Documentos com crescimento ilimitado.
- Chaves de particao com baixa cardinalidade.
- Ignorar consistencia requerida pelo negocio.
- Modelos que nao seguem os padroes de acesso reais.

## Examples

### Example 1: Escolha de modelo NoSQL

**Input:**  
"Preciso armazenar perfis de usuario com campos variaveis e ler o perfil completo com frequencia."

**Output:**  
"Modelo documento e o mais adequado. Projete o documento para retornar o perfil completo em uma leitura."

## References

- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [Redis Documentation](https://redis.io/docs/)
