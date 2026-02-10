---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

## Java Example

`java
Service svc = Service.create(wsdlUrl, qname); MyPort port = svc.getPort(MyPort.class);
`

## Kotlin Example

`kotlin
val port: MyPort = Service.create(wsdlUrl, qname).getPort(MyPort::class.java)
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- JAX-WS
- SOAP 1.2
- WSDL evolution
- fault contracts
- certificate management

