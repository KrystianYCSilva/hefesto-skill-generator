# Funções em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Lambdas, Higher-Order Functions, Extension Functions, Inline Functions

---

## Overview

Funções são cidadãos de primeira classe em Kotlin: podem ser passadas como argumento, retornadas por outras funções e armazenadas em variáveis. Isso permite programação funcional expressiva e idiomática.

---

## Funções Básicas

### Declaração e Retorno

```kotlin
// Função com corpo de bloco
fun somar(a: Int, b: Int): Int {
    return a + b
}

// Função com corpo de expressão (uma linha)
fun somar2(a: Int, b: Int): Int = a + b

// Tipo de retorno inferido na expressão
fun somar3(a: Int, b: Int) = a + b

// Retorno Unit (void) — pode ser omitido
fun saudar(nome: String) {
    println("Olá, $nome!")
}
```

### Parâmetros com Valor Padrão

```kotlin
fun criarsaudacao(nome: String, saudacao: String = "Olá"): String =
    "$saudacao, $nome!"

println(criarsaudacao("Alice"))           // "Olá, Alice!"
println(criarsaudacao("Bob", "Boa tarde")) // "Boa tarde, Bob!"
```

### Named Arguments (Argumentos Nomeados)

```kotlin
fun configurar(
    host: String = "localhost",
    porta: Int = 8080,
    debug: Boolean = false
): String = "$host:$porta (debug=$debug)"

//Only named arguments — ordem não importa
println(configurar(debug = true, porta = 3000))
// "localhost:3000 (debug=true)"
```

### Varargs

```kotlin
fun somarTodos(vararg numeros: Int): Int =
    numeros.sum()

println(somarTodos(1, 2, 3))          // 6
println(somarTodos(10, 20, 30, 40))   // 100

// Expandir array com spread operator
val nums = intArrayOf(1, 2, 3)
println(somarTodos(*nums))            // 6
```

---

## Lambdas

### Sintaxe

```kotlin
// Lambda básico: { parâmetros -> corpo }
val somar = { a: Int, b: Int -> a + b }
println(somar(3, 4))  // 7

// Parâmetro único: usar 'it'
val dobrar = { x: Int -> x * 2 }
val dobrar2 = { it * 2 }  // 'it' inferido como Int no contexto

// Lambda sem parâmetros
val saudar = { println("Olá!") }
saudar()  // "Olá!"

// Lambda multi-linha
val processar = { lista: List<Int> ->
    val filtrado = lista.filter { it > 0 }
    filtrado.sum()
}
```

### Lambda como Último Argumento (Trailing Lambda)

```kotlin
// Sem trailing lambda
listOf(3, 1, 2).sortedWith(Comparator { a, b -> a - b })

// COM trailing lambda — mais legível
listOf(3, 1, 2).sortedWith { a, b -> a - b }

// Exemplo com repeat
repeat(3) { i ->
    println("Iteração $i")
}
```

---

## Higher-Order Functions

Funções que recebem ou retornam outras funções.

### Recebendo uma Função como Parâmetro

```kotlin
// Tipo de função: (Int) -> Int
fun aplicar(valor: Int, operacao: (Int) -> Int): Int =
    operacao(valor)

println(aplicar(5) { it * it })      // 25
println(aplicar(10) { it + 3 })      // 13

// Tipo mais complexo: (String, String) -> Boolean
fun filtrarPor(lista: List<String>, predicado: (String) -> Boolean): List<String> =
    lista.filter(predicado)

val nomes = listOf("Alice", "Bob", "Carlos", "Ana")
println(filtrarPor(nomes) { it.startsWith("A") })  // [Alice, Ana]
```

### Retornando uma Função

```kotlin
// Retorna uma função (Int) -> Int
fun multiplicadorDe(fator: Int): (Int) -> Int =
    { valor -> valor * fator }

val triplo = multiplicadorDe(3)
println(triplo(5))   // 15
println(triplo(10))  // 30

// Uso diretamente
println(multiplicadorDe(4)(7))  // 28
```

### Armazenando Funções em Variáveis

```kotlin
val operacoes = mapOf<String, (Int, Int) -> Int>(
    "soma"       to { a, b -> a + b },
    "subtracao"  to { a, b -> a - b },
    "multiplicacao" to { a, b -> a * b }
)

val resultado = operacoes["soma"]?.invoke(10, 5)
println(resultado)  // 15
```

---

## Extension Functions (Funções de Extensão)

Permitem adicionar funções a classes existentes sem modificá-las ou herdar delas.

### Declaração

```kotlin
// Adiciona função à classe String
fun String.inverter(): String = this.reversed()

// Adiciona função à classe Int
fun Int.ehPar(): Boolean = this % 2 == 0

// Uso
println("Hello".inverter())  // "olleH"
println(4.ehPar())           // true
println(7.ehPar())           // false
```

### Extensões em Collections

```kotlin
fun <T> List<T>.segundo(): T? =
    if (size >= 2) this[1] else null

fun List<Int>.media(): Double =
    if (isEmpty()) 0.0 else sum().toDouble() / size

val lista = listOf(10, 20, 30)
println(lista.segundo())  // 20
println(lista.media())    // 20.0
```

### Extensões com Receiver Genérico

```kotlin
// Função de extensão genérica
fun <T> T.repetir(vezes: Int): List<T> =
    List(vezes) { this }

println("Ha".repetir(3))  // [Ha, Ha, Ha]
println(42.repetir(2))    // [42, 42]
```

### Extensões vs Métodos da Classe

```kotlin
class Exemplo {
    fun metodo() = "classe"
}

// Extensão com mesmo nome
fun Exemplo.metodo() = "extensão"

val obj = Exemplo()
println(obj.metodo())  // "classe" — método da classe SEMPRE vence
```

---

## Inline Functions

Funções `inline` são inseridas no ponto de chamada em compile-time, eliminando overhead de criação de objetos lambda.

### Quando Usar

```kotlin
// Sem inline: cria objeto lambda a cada chamada
fun executar(bloco: () -> Unit) {
    bloco()
}

// Com inline: bloco é "copiado" no ponto de chamada
inline fun executarInline(bloco: () -> Unit) {
    bloco()
}

// Para lambdas simples que são chamados muitas vezes, inline reduz overhead
inline fun medirTempo(bloco: () -> Unit): Long {
    val inicio = System.currentTimeMillis()
    bloco()
    return System.currentTimeMillis() - inicio
}

val tempo = medirTempo {
    Thread.sleep(100)
}
println("Tempo: ${tempo}ms")
```

### noinline e crossinline

```kotlin
// noinline: um parâmetro específico NÃO é inlinado
inline fun exemplo(
    normal: () -> Unit,
    noinline semInline: () -> Unit  // não será inlinado
) {
    normal()
    semInline()
}

// crossinline: lambda pode ser chamado em outro contexto (não-local)
inline fun executarAsync(crossinline bloco: () -> Unit) {
    Thread {
        bloco()  // crossinline permite isso
    }.start()
}
```

### Inline com Reified Types

```kotlin
// reified permite usar T como classe em runtime (dentro de inline)
inline fun <reified T> criar(): T =
    T::class.java.getDeclaredConstructor().newInstance()

// Uso
val lista = criar<ArrayList<String>>()
```

---

## Funções Locais

Funções declaradas dentro de outras funções, com acesso ao scope da função externa.

```kotlin
fun processar(dados: List<Int>): List<Int> {
    // Função local — acessa variáveis da função externa
    fun validar(valor: Int): Boolean {
        return valor > 0 && valor < 100
    }

    fun transformar(valor: Int): Int {
        return valor * 2
    }

    return dados
        .filter { validar(it) }
        .map { transformar(it) }
}

println(processar(listOf(-5, 10, 50, 150, 75)))  // [20, 100, 150]
```

---

## Tipos de Função (Function Types)

```kotlin
// Tipo básico: (Parâmetros) -> Retorno
val funcao: (Int, Int) -> Int = { a, b -> a + b }

// Sem parâmetros
val saudacao: () -> String = { "Olá!" }

// Com receiver (extension function type)
val extensao: String.() -> String = { this.uppercase() }
println(extensao("hello"))  // "HELLO"

// Nullable function type
val opcional: ((Int) -> Int)? = null
opcional?.invoke(5)  // safe call — não executa se null
```

---

## Best Practices

### Usar

```kotlin
// Usar trailing lambdas para legibilidade
listOf(1, 2, 3).forEach { println(it) }

// Usar extension functions para funcionalidade reutilizável
fun String.capitalizar() = replaceFirstChar { it.uppercase() }

// Usar inline para funções com lambdas que são chamadas frequentemente
inline fun com(bloco: () -> Unit) { bloco() }

// Usar named arguments para clareza
configurar(porta = 8080, debug = true)

// Usar valor padrão para parâmetros opcionais
fun buscar(query: String, limite: Int = 10): List<String> = listOf()
```

### Evitar

```kotlin
// NÃO usar lambda quando named function é mais legível
// Evitar: complexidade escondida em lambdas extensos
val complexo = { lista: List<Any> ->
    // 20+ linhas de lógica aqui
}
// Extrair para função nomeada

// NÃO abusar de extension functions em tipos básicos
// Pode causar conflitos e confusão no namespace

// NÃO usar inline em funções sem parâmetros de lambda
inline fun semLambda(): String = "sem benefício"  // inline inútil aqui
```

---

## Referências

- [Kotlin Functions](https://kotlinlang.org/docs/functions.html) — Documentação oficial
- [Kotlin Lambdas](https://kotlinlang.org/docs/lambdas.html) — Guia de lambdas e tipos de função
- [Kotlin Inline Functions](https://kotlinlang.org/docs/inline-functions.html) — Detalhes de inline
- [Effective Kotlin — Functions](https://effectivekotlin.com/) — Boas práticas
