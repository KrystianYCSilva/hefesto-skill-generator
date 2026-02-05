# OOP em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Classes, Data Classes, Sealed Classes, Interfaces, Delegação

---

## Overview

Kotlin oferece um modelo orientado a objetos refinado em relação ao Java: classes são `final` por padrão, propriedades substituem campos + getters/setters, e recursos como data classes e sealed classes reduzem boilerplate.

---

## Classes Básicas

### Declaração e Construtor Primário

```kotlin
// Construtor primário: parâmetros diretamente na classe
class Pessoa(val nome: String, var idade: Int) {
    // val -> propriedade somente leitura (gera getter)
    // var -> propriedade mutável (gera getter + setter)
}

val p = Pessoa("Alice", 30)
println(p.nome)      // "Alice"
p.idade = 31         // mutável
// p.nome = "Bob"    // erro: val não pode ser reatribuído
```

### Construtor Secundário

```kotlin
class Produto(val nome: String, val preco: Double, val categoria: String) {
    // Construtor secundário: delega para o primário
    constructor(nome: String, preco: Double) : this(nome, preco, "Geral")

    // Outro construtor secundário
    constructor(nome: String) : this(nome, 0.0, "Sem preço")
}

val p1 = Produto("Notebook", 4999.0, "Eletrônicos")
val p2 = Produto("Mouse", 49.0)        // categoria = "Geral"
val p3 = Produto("Cabo")               // preco = 0.0, categoria = "Sem preço"
```

### init block

```kotlin
class Conta(val titular: String, var saldo: Double) {
    val extrato = mutableListOf<String>()

    init {
        require(saldo >= 0) { "Saldo inicial não pode ser negativo" }
        extrato.add("Conta criada com saldo $saldo")
    }

    fun depositar(valor: Double) {
        require(valor > 0) { "Valor de depósito deve ser positivo" }
        saldo += valor
        extrato.add("Depósito: +$valor")
    }

    fun sacar(valor: Double): Boolean {
        if (valor > saldo) return false
        saldo -= valor
        extrato.add("Saque: -$valor")
        return true
    }
}
```

### Classes Abertas (Herança)

```kotlin
// Classes são final por padrão — usar 'open' para permitir herança
open class Animal(val nome: String) {
    open fun falar(): String = "..."  // open permite override
    fun respirar() = "respirando"    // sem open — não pode ser sobrescrito
}

class Cachorro(nome: String) : Animal(nome) {
    override fun falar(): String = "Au!"
}

class Gato(nome: String) : Animal(nome) {
    override fun falar(): String = "Miau!"
}

val animais = listOf(Cachorro("Rex"), Gato("Whiskers"))
animais.forEach { println("${it.nome}: ${it.falar()}") }
// Rex: Au!
// Whiskers: Miau!
```

---

## Data Classes

Data classes geram automaticamente: `equals()`, `hashCode()`, `toString()`, `copy()` e `componentN()` functions.

```kotlin
data class Ponto(val x: Double, val y: Double)

val p1 = Ponto(1.0, 2.0)
val p2 = Ponto(1.0, 2.0)
val p3 = p1.copy(x = 3.0)  // Ponto(3.0, 2.0)

println(p1 == p2)            // true (equals por valor)
println(p1)                  // Ponto(x=1.0, y=2.0) (toString)

// Destructuring (usa componentN)
val (x, y) = p1
println("x=$x, y=$y")       // x=1.0, y=2.0
```

### Data Class com Validação e Propriedades Customizadas

```kotlin
data class Email(val endereco: String) {
    init {
        require(endereco.contains("@")) { "Email inválido: $endereco" }
    }

    // Propriedade computada (não entra no equals/hashCode/toString)
    val dominio: String
        get() = endereco.substringAfter("@")
}

val email = Email("alice@gmail.com")
println(email.dominio)  // "gmail.com"
```

### Quando Usar Data Class

```kotlin
// SIM: objetos que representam dados (DTOs, value objects)
data class Usuario(val id: Long, val nome: String, val email: String)
data class Coordenada(val latitude: Double, val longitude: Double)

// NÃO: objetos com comportamento ou estado mutável complexo
// NÃO: objetos que não precisam de equals/hashCode por valor
```

---

## Sealed Classes e Interfaces

Sealed types definem hierarquias fechadas — todas as subclasses são conhecidas em compile-time, permitindo `when` exhaustivo.

### Sealed Interface (Kotlin 1.5+)

```kotlin
sealed interface Evento {
    data class Click(val x: Int, val y: Int) : Evento
    data class Teclado(val tecla: Char) : Evento
    data class Scroll(val delta: Int) : Evento
}

fun handleEvento(evento: Evento): String = when (evento) {
    is Evento.Click   -> "Clique em (${ evento.x}, ${evento.y})"
    is Evento.Teclado -> "Tecla: ${evento.tecla}"
    is Evento.Scroll  -> "Rolamento: ${evento.delta}"
    // sem necessidade de 'else' — exhaustivo
}
```

### Sealed Class (Kotlin 1.0+)

```kotlin
sealed class Forma {
    abstract fun area(): Double

    class Circulo(val raio: Double) : Forma() {
        override fun area() = Math.PI * raio * raio
    }

    class Retangulo(val largura: Double, val altura: Double) : Forma() {
        override fun area() = largura * altura
    }
}

fun descrever(forma: Forma): String = when (forma) {
    is Forma.Circulo    -> "Círculo com área ${forma.area()}"
    is Forma.Retangulo  -> "Retângulo com área ${forma.area()}"
}
```

### Caso de Uso: Estado de uma Requisição

```kotlin
sealed interface EstadoRequisicao<out T> {
    object Carregando : EstadoRequisicao<Nothing>
    data class Sucesso<T>(val dados: T) : EstadoRequisicao<T>
    data class Erro(val mensagem: String) : EstadoRequisicao<Nothing>
}

fun <T> renderizar(estado: EstadoRequisicao<T>) {
    when (estado) {
        is EstadoRequisicao.Carregando -> println("Carregando...")
        is EstadoRequisicao.Sucesso    -> println("Dados: ${estado.dados}")
        is EstadoRequisicao.Erro       -> println("Erro: ${estado.mensagem}")
    }
}
```

---

## Interfaces

### Interface com Métodos Default

```kotlin
interface Imprimível {
    fun conteudo(): String

    // Método default (implementação padrão)
    fun imprimir() {
        println("=== Impressão ===")
        println(conteudo())
        println("=================")
    }
}

class Relatório(val titulo: String, val corpo: String) : Imprimível {
    override fun conteudo() = "$titulo\n$corpo"
    // imprimir() herda a implementação default
}
```

### Interface com Propriedades

```kotlin
interface Identificável {
    val id: String
}

interface Nomeável {
    val nome: String
}

// Implementar múltiplas interfaces
class Funcionário(
    override val id: String,
    override val nome: String,
    val departamento: String
) : Identificável, Nomeável

val func = Funcionário("F001", "Alice", "Engenharia")
println(func.id)   // "F001"
println(func.nome) // "Alice"
```

---

## Delegação por Propriedade

Delegação permite reutilizar implementações sem herança, usando `by`.

### Delegação de Interface

```kotlin
interface Logger {
    fun log(mensagem: String)
}

class ConsoleLogger : Logger {
    override fun log(mensagem: String) {
        println("[LOG] $mensagem")
    }
}

// Delega a implementação de Logger para uma instância
class Servico(private val logger: Logger = ConsoleLogger()) : Logger by logger {
    fun executar() {
        log("Executando serviço...")  // delega para logger
        // lógica do serviço
        log("Serviço finalizado.")
    }
}

val servico = Servico()
servico.executar()
// [LOG] Executando serviço...
// [LOG] Serviço finalizado.
```

### Delegação de Propriedade com `by lazy`

```kotlin
class ConfiguracaoHeavy {
    // Lazy: calcula apenas na primeira vez que for acessada
    val dados: List<String> by lazy {
        println("Carregando dados pesados...")
        listOf("dado1", "dado2", "dado3")
    }
}

val config = ConfiguracaoHeavy()  // não carrega ainda
println("Criado")
println(config.dados)             // NOW carrega
println(config.dados)             // usa valor em cache, não recomputa
// Output:
// Criado
// Carregando dados pesados...
// [dado1, dado2, dado3]
// [dado1, dado2, dado3]
```

---

## Objetos e Companions

### object (Singleton)

```kotlin
object Configuracao {
    var tema = "claro"
    var idioma = "pt-BR"

    fun resetar() {
        tema = "claro"
        idioma = "pt-BR"
    }
}

// Uso direto, sem instância
println(Configuracao.tema)     // "claro"
Configuracao.tema = "escuro"
```

### companion object (Métodos Estáticos)

```kotlin
class Moeda(val valor: Double, val moeda: String) {
    companion object {
        fun real(valor: Double) = Moeda(valor, "BRL")
        fun dolar(valor: Double) = Moeda(valor, "USD")
        fun euro(valor: Double) = Moeda(valor, "EUR")
    }

    override fun toString() = "$valor $moeda"
}

val preco = Moeda.real(99.90)  // factory method
println(preco)                 // "99.9 BRL"
```

---

## Best Practices

### Usar

```kotlin
// Usar data classes para objetos de dados
data class Item(val nome: String, val quantidade: Int)

// Usar sealed interfaces para estados e hierarquias fechadas
sealed interface Status { /* ... */ }

// Usar val onde possível
class Imutavel(val valor: String)

// Usar delegação ao invés de herança quando possível
class Servico(logger: Logger) : Logger by logger

// Usar by lazy para inicialização pesada adiada
val recurso by lazy { carregarRecurso() }
```

### Evitar

```kotlin
// NÃO herdar quando delegação é suficiente
class Hijo : Padre()  // considere delegação

// NÃO usar var em data class sem necessidade real
data class Item(var nome: String)  // prefer val

// NÃO criar classes abertas sem justificativa
open class Classe  // classes são final por padrão — mantenha assim

// NÃO abusar de companion object para estado global
// Use object declarado no nível superior se for verdadeiro singleton
```

---

## Referências

- [Kotlin Classes and Objects](https://kotlinlang.org/docs/classes.html) — Documentação oficial
- [Kotlin Data Classes](https://kotlinlang.org/docs/data-classes.html) — Spec detalhada
- [Kotlin Sealed Classes](https://kotlinlang.org/docs/sealed-classes.html) — Guia oficial
- [Effective Kotlin — OOP](https://effectivekotlin.com/) — Boas práticas
