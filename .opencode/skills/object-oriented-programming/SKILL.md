---
name: object-oriented-programming
description: |
  Orienta design e implementacao OOP com foco em modelagem, extensibilidade e manutencao.
  Use when: o usuario precisa modelar dominios orientados a objetos, escolher entre composicao e heranca, desenhar interfaces ou evitar armadilhas de OOP.
---

# Object-Oriented Programming

Fornece orientacao objetiva para modelar dominios com classes, interfaces e relacionamentos. Foca em escolhas de design que impactam manutencao e evolucao do sistema.

## How to model domain objects
- Mapear entidades, responsabilidades e limites de agregados.
- Definir invariantes do dominio e manter em um unico lugar.
- Usar nomes e metodos que expressem comportamento, nao apenas dados.

## How to choose composition vs inheritance
- Preferir composicao quando o reuso for funcional, nao hierarquico.
- Usar heranca apenas quando houver substituicao valida (LSP).
- Evitar hierarquias profundas e fragis.

## How to design interfaces and abstractions
- Introduzir interfaces onde houver variacao real de implementacao.
- Manter contratos pequenos e coesos.
- Evitar classes "god object" que concentram tudo.

## How to apply encapsulation and immutability
- Expor o minimo necessario do estado interno.
- Preferir objetos imutaveis em fluxos concorrentes.
- Validar invariantes no construtor ou factory.

## How to manage polymorphism safely
- Usar polimorfismo para eliminar condicionais repetitivas.
- Centralizar decisoes de tipo em um ponto (factory/registry).
- Evitar casts e verificacoes de tipo espalhadas.

## How to avoid common OOP pitfalls
- Evitar "anemic models" com apenas getters/setters.
- Nao misturar logica de dominio com detalhes de persistencia.
- Evitar acoplamento entre camadas por dependencia direta.

## Examples

### Example 1: Composicao vs heranca

**Input:**  
"Tenho RelatorioFinanceiro e RelatorioOperacional com logica comum de exportacao."

**Output:**  
"Use composicao: extraia um componente Exportador e injete nas classes de relatorio, evitando uma hierarquia fragil."
