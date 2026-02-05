---
name: kotlin-fundamentals
description: |
  Auxilia no desenvolvimento de código Kotlin seguindo boas práticas de tipos seguros,
  programação funcional e recursos idiomáticos da linguagem (Kotlin 1.x a 2.x).
  Use quando: criar classes Kotlin, trabalhar com tipos nulos, usar coroutines básicas,
  aplicar funções de extensão, usar collections, data classes, sealed classes ou interfaces.
license: MIT
metadata: ./metadata.yaml
---

# Kotlin Fundamentals

Skill para desenvolvimento em Kotlin seguindo fundamentos sólidos do sistema de tipos, programação funcional e recursos idiomáticos da linguagem. Abrange Kotlin 1.x a 2.x de forma genérica, sem dependência de framework específico.

---

## When to Use

Use esta skill quando precisar:

- **Criar classes e estruturas Kotlin** com tipos seguros (data classes, sealed classes, value classes)
- **Trabalhar com tipos nulos** (nullable types, smart casts, operadores `?.` e `!!`)
- **Escrever funções idiomáticas** (lambdas, funções de extensão, higher-order functions, inline)
- **Usar collections** (List, Set, Map, sequences, operações funcionais)
- **Implementar coroutines básicas** (suspend functions, scopes, dispatchers)
- **Aplicar herança e interfaces** com delegação por propriedade
- **Tratar erros** de forma robusta (Result, try/catch, exceções customizadas)
- **Refatorar código existente** para idiomatic Kotlin
- **Escrever código compatível** entre diferentes versões do Kotlin (1.x a 2.x)

**Não use para:** Frameworks específicos (Android/Jetpack Compose, Ktor, Spring Boot), build tools, deployment, multiplatform avançado.

---

## Instructions

### Step 1: Analisar Contexto

Antes de gerar código, identifique:

1. **Versão do Kotlin alvo**
   - Verifique `kotlin -version` ou arquivos de build (`build.gradle.kts`, `pom.xml`)
   - Se versão não especificada: assumir Kotlin 1.9 (estável e amplo suporte)

2. **Padrões de código existentes**
   - Convenções de nomenclatura (camelCase para funções/variáveis, PascalCase para classes)
   - Uso de `val` vs `var` no projeto
   - Estilo de indentação (padrão: 4 espaços)

3. **Recursos disponíveis por versão**
   - Kotlin 1.0-1.2: Basics, nullable types, data classes, companion objects
   - Kotlin 1.3+: Coroutines estáveis, sealed classes, inline classes
   - Kotlin 1.5+: Sealed interfaces, value classes, SAM conversions
   - Kotlin 1.7+: Builder inference, definitely non-volatile
   - Kotlin 1.9+: K2 compiler improvements
   - Kotlin 2.0+: K2 compiler padrão, script improvements

### Step 2: Aplicar Princípios Core do Kotlin

**Imutabilidade por padrão:**
```kotlin
// CORRETO: val para valores que não mudam
val nome = "Alice"
val lista = listOf(1, 2, 3)       // lista imutável

// var apenas quando necessário
var contador = 0
contador++
```

**Tipos seguros e nullable:**
```kotlin
// Tipo não-nulo por padrão
val nome: String = "Alice"         // nunca null

// Tipo nulo explícito
val apelido: String? = null        // pode ser null

// Safe call e elvis operator
val tamanho = apelido?.length ?: 0

// Smart cast automático
fun saudar(nome: String?) {
    if (nome != null) {
        println(nome.uppercase())  // smart cast: String? -> String
    }
}
```

**Data classes para DTOs:**
```kotlin
// Gera equals, hashCode, toString, copy e component functions
data class Produto(
    val id: String,
    val nome: String,
    val preco: Double
) {
    // Validação no init block
    init {
        require(preco >= 0) { "Preço não pode ser negativo" }
    }
}

val p1 = Produto("1", "Notebook", 4999.0)
val p2 = p1.copy(preco = 4599.0)   // cópia com campo alterado
```

### Step 3: Usar Recursos Modernos

**Sealed classes e interfaces para hierarquias controladas:**
```kotlin
sealed interface Forma {
    data class Circulo(val raio: Double) : Forma
    data class Retangulo(val largura: Double, val altura: Double) : Forma
    data class Triangulo(val base: Double, val altura: Double) : Forma
}

// when é exhaustivo com sealed types (sem necessidade de else)
fun area(forma: Forma): Double = when (forma) {
    is Forma.Circulo    -> Math.PI * forma.raio * forma.raio
    is Forma.Retangulo  -> forma.largura * forma.altura
    is Forma.Triangulo  -> 0.5 * forma.base * forma.altura
}
```

**Funções de extensão:**
```kotlin
// Adiciona funcionalidade sem herança
fun String.capitalizar(): String =
    replaceFirstChar { it.uppercase() }

fun List<Int>.media(): Double =
    if (isEmpty()) 0.0 else sum().toDouble() / size

// Uso
val texto = "hello".capitalizar()       // "Hello"
val avg = listOf(10, 20, 30).media()    // 20.0
```

**Coroutines básicas:**
```kotlin
import kotlinx.coroutines.*

suspend fun buscarDados(id: Int): String {
    delay(1000)  // simula chamada assíncrona
    return "Dado #$id"
}

fun main() = runBlocking {
    // Execução sequencial
    val dado1 = buscarDados(1)
    val dado2 = buscarDados(2)

    // Execução paralela com launch
    launch { println(buscarDados(3)) }
    launch { println(buscarDados(4)) }
}
```

### Step 4: Validar e Revisar

**Checklist Final:**
- [ ] Código compila sem warnings (`kotlinc` ou build tool)
- [ ] `val` usado onde possível; `var` apenas quando necessário
- [ ] Tipos nulos tratados com `?.`, `?:` ou smart cast
- [ ] Data classes usadas para objetos de dados
- [ ] Sealed types usados para hierarquias fechadas
- [ ] Funções pequenas e focadas (< 20 linhas)
- [ ] Nomes descritivos (classes, funções, variáveis)
- [ ] Sem código duplicado (considere funções de extensão)
- [ ] Erros tratados com Result ou exceções adequadas
- [ ] Compatível com versão Kotlin alvo do projeto

---

## Referências JIT

Para tópicos avançados, consulte as referências detalhadas:

| Tópico | Arquivo | Conteúdo |
|--------|---------|----------|
| Sistema de Tipos | [types.md](./references/types.md) | Nullable types, smart casts, generics, type aliases, value classes |
| OOP em Kotlin | [oop.md](./references/oop.md) | Classes, data classes, sealed classes, interfaces, delegação |
| Funções | [functions.md](./references/functions.md) | Lambdas, higher-order functions, extensões, inline |
| Collections | [collections.md](./references/collections.md) | List, Set, Map, sequences, operações funcionais |
| Coroutines | [coroutines.md](./references/coroutines.md) | Suspend functions, scopes, dispatchers, channels |
| Tratamento de Erros | [error-handling.md](./references/error-handling.md) | Try/catch, Result, exceções customizadas |

Estas referências são carregadas just-in-time quando necessário.

---

## Quick Examples

### Data Class com Validação
```kotlin
data class Cliente(
    val nome: String,
    val email: String,
    val idade: Int
) {
    init {
        require(nome.isNotBlank()) { "Nome não pode estar vazio" }
        require(email.contains("@")) { "Email inválido" }
        require(idade in 0..150) { "Idade inválida" }
    }
}
```

### Sealed Interface + when Exhaustivo
```kotlin
sealed interface Resultado<out T> {
    data class Sucesso<T>(val valor: T) : Resultado<T>
    data class Falha(val erro: String) : Resultado<Nothing>
}

fun processar(resultado: Resultado<String>) {
    when (resultado) {
        is Resultado.Sucesso -> println("OK: ${resultado.valor}")
        is Resultado.Falha   -> println("Erro: ${resultado.erro}")
    }
}
```

### Collections Funcionais
```kotlin
val produtos = listOf(
    Produto("1", "Notebook", 4999.0),
    Produto("2", "Mouse", 49.0),
    Produto("3", "Teclado", 129.0)
)

// Filtrar, transformar e ordenar
val caros = produtos
    .filter { it.preco > 100.0 }
    .sortedByDescending { it.preco }
    .map { it.nome }
// ["Notebook", "Teclado"]
```

Para exemplos detalhados, consulte as **[referências JIT](#referências-jit)**.

---

## Compatibility

| CLI | Status | Notes |
|-----|--------|-------|
| Claude Code | Supported | Fully supported |
| Gemini CLI | Supported | Fully supported |
| OpenAI Codex | Supported | Fully supported |
| GitHub Copilot | Supported | Fully supported |
| OpenCode | Supported | Fully supported |
| Cursor | Supported | Fully supported |
| Qwen Code | Supported | Fully supported |

**Requires:**
- Acesso ao filesystem para ler código existente
- Capacidade de executar `kotlin -version` (detecção de versão)

---

## Segurança

- Não executa código automaticamente
- Não acessa rede ou recursos externos
- Apenas leitura e análise de código Kotlin
- Sugestões seguem princípios de segurança: validação de entrada (`require`, `check`), uso de `val` para imutabilidade, tipos seguros para evitar NPE em runtime
- Dados sensíveis não devem ser hardcoded; use variáveis de ambiente ou arquivos de configuração

---

## Fontes

| Fonte | Tipo | URL |
|-------|------|-----|
| Kotlin Language Documentation | Oficial | [kotlinlang.org](https://kotlinlang.org/docs/) |
| Kotlin Coroutines Documentation | Oficial | [kotlinlang.org/docs/coroutines](https://kotlinlang.org/docs/coroutines-guide.html) |
| Kotlin in Action (Irina Galstyan & Dmitry Jemerov) | Livro | [Manning](https://www.manning.com/books/kotlin-in-action-second-edition) |
| Effective Kotlin (Marcin Mostyn) | Livro | [effectivekotlin.com](https://effectivekotlin.com/) |
| JetBrains Kotlin Coding Conventions | Oficial | [kotlinlang.org/docs/coding-conventions](https://kotlinlang.org/docs/coding-conventions.html) |

---

**Version**: 1.0.0
**Created**: 2026-02-04
**License**: MIT
