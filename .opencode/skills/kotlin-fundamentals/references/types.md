# Sistema de Tipos em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Nullable Types, Smart Casts, Generics, Type Aliases, Value Classes

---

## Overview

O sistema de tipos do Kotlin é null-safe por design: tipos não-nulos são o padrão, e o compilador aplica verificações estáticas para evitar NullPointerException em runtime. Generics, type aliases e value classes completam o sistema com expressividade e type safety.

---

## Tipos Básicos

### Primitivos e Wrappers

Kotlin não distingue entre primitivos e wrappers na superfície — o compilador otimiza automaticamente.

```kotlin
val inteiro: Int = 42
val ponto: Double = 3.14
val booleano: Boolean = true
val caractere: Char = 'A'
val texto: String = "Olá"
val longo: Long = 1234567890L
val curto: Short = 100
val byte: Byte = 127
val flutuante: Float = 2.5f
```

### Conversões de Tipo

```kotlin
val inteiro: Int = 42
val double: Double = inteiro.toDouble()     // 42.0
val string: String = inteiro.toString()     // "42"
val fromString: Int = "123".toInt()         // 123
val fromStringSafe: Int? = "abc".toIntOrNull()  // null (sem exceção)

// Conversões explícitas sempre necessárias
val a: Int = 10
val b: Long = a.toLong()      // explícito obrigatório
// val c: Long = a           // ERRO: tipo incompatível
```

---

## Nullable Types

### Declaração

```kotlin
val nome: String = "Alice"      // nunca null
val apelido: String? = null     // pode ser null
val idade: Int? = null          // pode ser null
```

### Safe Call Operator (?.)

Retorna null se o objeto for null, sem lançar exceção.

```kotlin
val apelido: String? = null
val tamanho: Int? = apelido?.length    // null (não lança NPE)

// Encadeamento
data class Endereco(val cidade: String?)
data class Usuario(val endereco: Endereco?)

val usuario: Usuario? = null
val cidade = usuario?.endereco?.cidade  // null — sem NPE
```

### Elvis Operator (?:)

Fornece valor padrão quando o lado esquerdo é null.

```kotlin
val apelido: String? = null
val nome = apelido ?: "Desconhecido"   // "Desconhecido"

// Encadeamento com elvis
val valor = configurar()?.obter() ?: valores.padrao() ?: "fallback"

// Elvis com throw
val nome2 = apelido ?: throw IllegalStateException("Nome não pode ser null")
```

### Non-null Assertion (!!)

Força conversão para tipo não-nulo. Lança NPE se for null. **Usar com cautela.**

```kotlin
val apelido: String? = "Bob"
val nome: String = apelido!!  // "Bob" — seguro aqui

// PERIGOSO:
val nulo: String? = null
val crash: String = nulo!!    // lança NullPointerException!
```

---

## Smart Casts

O compilador rastreia verificações de tipo e aplica casts automaticamente.

### if como Smart Cast

```kotlin
fun processar(valor: Any) {
    if (valor is String) {
        // Smart cast: valor é String aqui
        println(valor.uppercase())  // sem cast manual
        println(valor.length)
    } else if (valor is Int) {
        // Smart cast: valor é Int aqui
        println(valor * 2)
    }
}
```

### when como Smart Cast

```kotlin
fun descrever(valor: Any): String = when (valor) {
    is String  -> "String de tamanho ${valor.length}"    // smart cast
    is Int     -> "Inteiro: ${valor * 2}"                // smart cast
    is Boolean -> "Booleano: $valor"                     // smart cast
    is List<*> -> "Lista com ${valor.size} elementos"   // smart cast
    else       -> "Tipo desconhecido"
}
```

### Smart Cast com Variáveis

```kotlin
val valor: String? = obterValor()

// NÃO funciona: valor é var ou pode mudar entre verificação e uso
// if (valor != null) { valor.length }  // erro se valor fosse var

// FUNCIONA: val local garante imutabilidade
val valorLocal = valor
if (valorLocal != null) {
    println(valorLocal.length)  // smart cast funciona
}

// Ou usar let
valor?.let { v ->
    println(v.length)  // v é String (não nullable)
}
```

### is com negação

```kotlin
val valor: Any = obterValor()

if (valor !is String) {
    return  // retorna cedo
}
// Aqui, valor é smart cast para String
println(valor.uppercase())
```

---

## Generics

### Classes Genéricas

```kotlin
// Container genérico
class Caixa<T>(private var conteudo: T) {
    fun obter(): T = conteudo
    fun definir(valor: T) { conteudo = valor }
}

val caixaString = Caixa("Olá")
val caixaInt = Caixa(42)

println(caixaString.obter())  // "Olá"
println(caixaInt.obter())     // 42
```

### Funções Genéricas

```kotlin
fun <T> primeiro(lista: List<T>): T? =
    lista.firstOrNull()

fun <T : Comparable<T>> maior(a: T, b: T): T =
    if (a > b) a else b

println(primeiro(listOf("A", "B", "C")))  // "A"
println(maior(10, 20))                    // 20
println(maior("banana", "maçã"))          // "maçã"
```

### Bounded Type Parameters

```kotlin
// T deve ser Comparable
fun <T : Comparable<T>> ordenar(lista: List<T>): List<T> =
    lista.sorted()

// Múltiplos bounds com where
fun <T> processar(valor: T): String
    where T : Comparable<T>, T : java.io.Serializable
{
    return valor.toString()
}
```

### Variância: out e in

```kotlin
// out (Covariance): produz T, não consome
// Producer Extends
class Produtor<out T>(private val valor: T) {
    fun obter(): T = valor
    // fun definir(v: T) {} — NÃO permitido com out
}

// in (Contravariance): consome T, não produz
// Consumer Super
class Consumidor<in T> {
    fun processar(valor: T) { println(valor) }
    // fun obter(): T {} — NÃO permitido com in
}

// Exemplo prático
val produtorString: Produtor<String> = Produtor("Hello")
val produtorAny: Produtor<Any> = produtorString  // OK: String é subtipo de Any
```

### Star Projection (*)

```kotlin
// Quando não importa o tipo genérico
fun imprimirTudo(lista: List<*>) {
    lista.forEach { println(it) }
}

imprimirTudo(listOf(1, 2, 3))
imprimirTudo(listOf("A", "B"))
```

---

## Type Aliases

Criam nomes alternativos para tipos complexos.

```kotlin
// Sem alias: difícil de ler
fun processar(callback: (Map<String, List<Int>>, String) -> Boolean) { }

// Com alias: muito mais legível
typealias FiltroMapear = (Map<String, List<Int>>, String) -> Boolean

fun processar(callback: FiltroMapear) { }

// Outros exemplos
typealias Identificador = String
typealias PontoPar = Pair<Double, Double>
typealias ResultadoAsincrono<T> = java.util.concurrent.Future<T>

val id: Identificador = "USR-001"
val ponto: PontoPar = Pair(1.0, 2.0)
```

---

## Value Classes (Inline Classes)

Value classes criam tipos wrapper que são eliminados em compile-time, sem overhead de runtime.

```kotlin
// Sem value class: pode passar qualquer String onde email é esperado
fun enviar(email: String) { /* ... */ }
enviar("isso não é um email")  // sem erro

// Com value class: type safety em compile-time
@JvmInline
value class Email(val endereco: String) {
    init {
        require(endereco.contains("@")) { "Email inválido" }
    }
}

fun enviar(email: Email) { /* ... */ }
enviar(Email("alice@gmail.com"))  // OK
// enviar("string")               // ERRO de compilação

// Em runtime, Email é apenas um String — sem overhead de objeto
```

### Outros Exemplos de Value Class

```kotlin
@JvmInline
value class Celsius(val valor: Double)

@JvmInline
value class Fahrenheit(val valor: Double)

fun Celsius.toFahrenheit(): Fahrenheit =
    Fahrenheit(valor * 9.0 / 5.0 + 32.0)

val temperatura = Celsius(100.0)
val convertido = temperatura.toFahrenheit()
println(convertido.valor)  // 212.0

// Sem value class, é possível misturar Celsius e Fahrenheit:
// val errado: Fahrenheit = Celsius(100.0)  — com value class, ERRO
```

---

## Enums

```kotlin
enum class Direcao {
    NORTE, SUL, LESTE, OESTE
}

// Enum com propriedades e funções
enum class Planeta(val massa: Double, val raio: Double) {
    TERRA(5.976e24, 6.37814e6),
    MARTE(6.421e23, 3.3972e6);

    val gravidade: Double
        get() = 6.67300E-11 * massa / (raio * raio)
}

val dir = Direcao.NORTE
println(dir.name)     // "NORTE"
println(dir.ordinal)  // 0

// when com enum
fun descrever(dir: Direcao): String = when (dir) {
    Direcao.NORTE -> "Para cima"
    Direcao.SUL   -> "Para baixo"
    Direcao.LESTE -> "Para a direita"
    Direcao.OESTE -> "Para a esquerda"
}
```

---

## Best Practices

### Usar

```kotlin
// Usar tipos não-nulos por padrão
val nome: String = "Alice"  // nunca null

// Usar safe call + elvis para null safety
val resultado = valor?.processar() ?: valorPadrao

// Usar smart cast ao invés de cast manual
if (valor is String) println(valor.length)  // sem (valor as String)

// Usar value classes para semântica de tipo sem overhead
@JvmInline value class UserId(val valor: Long)

// Usar type aliases para tipos complexos
typealias Handler = (Request) -> Response
```

### Evitar

```kotlin
// NÃO usar !! sem necessidade real
val nome: String = valor!!  // perigoso

// NÃO ignorar nullable types com casts inseguros
val nome = valor as String  // lança ClassCastException se null

// NÃO usar Any quando tipo específico é possível
fun processar(valor: Any) { }  // preferir tipo concreto ou genérico

// NÃO usar raw types (Java interop)
val lista: List<*> = java.util.ArrayList()  // perder type safety
```

---

## Referências

- [Kotlin Basic Types](https://kotlinlang.org/docs/basic-types.html) — Documentação oficial
- [Kotlin Null Safety](https://kotlinlang.org/docs/null-safety.html) — Guia completo
- [Kotlin Generics](https://kotlinlang.org/docs/generics.html) — Variância e projections
- [Kotlin Value Classes](https://kotlinlang.org/docs/value-classes.html) — Inline classes
- [Effective Kotlin — Types](https://effectivekotlin.com/) — Boas práticas
