# Tratamento de Erros em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Try/Catch, Result Type, Exceções Customizadas, Erro em Coroutines

---

## Overview

Kotlin oferece duas abordagens complementares para tratamento de erros:
1. **Exceções** (try/catch) — mecanismo clássico, compatível com Java
2. **Result<T>** — tipo funcional que encapsula sucesso ou falha sem exceções

Todas as exceções em Kotlin são **unchecked** (não há checked exceptions como no Java).

---

## Try / Catch / Finally

### Básico

```kotlin
fun dividir(a: Double, b: Double): Double {
    if (b == 0.0) throw ArithmeticException("Divisão por zero")
    return a / b
}

try {
    val resultado = dividir(10.0, 0.0)
    println("Resultado: $resultado")
} catch (e: ArithmeticException) {
    println("Erro matemático: ${e.message}")
} finally {
    println("Bloco finally sempre executa")
}
// Output:
// Erro matemático: Divisão por zero
// Bloco finally sempre executa
```

### Múltiplos Catch

```kotlin
fun processar(entrada: String) {
    try {
        val numero = entrada.toInt()                   // pode lançar NumberFormatException
        val resultado = 100 / numero                   // pode lançar ArithmeticException
        println("Resultado: $resultado")
    } catch (e: NumberFormatException) {
        println("Entrada não é um número válido: ${e.message}")
    } catch (e: ArithmeticException) {
        println("Erro aritmético: ${e.message}")
    } catch (e: Exception) {
        println("Erro inesperado: ${e.message}")       // catch genérico por último
    }
}

processar("abc")   // "Entrada não é um número válido..."
processar("0")     // "Erro aritmético..."
processar("5")     // "Resultado: 20"
```

### Try como Expressão

Kotlin permite usar try como expressão que retorna valor.

```kotlin
val numero: Int = try {
    "123".toInt()
} catch (e: NumberFormatException) {
    0  // valor padrão em caso de erro
}
println(numero)  // 123

val numero2: Int = try {
    "abc".toInt()
} catch (e: NumberFormatException) {
    -1
}
println(numero2)  // -1
```

### Finally para Recursos

```kotlin
var conexao: ConexaoDB? = null
try {
    conexao = abrirConexao()
    val dados = conexao.buscar("SELECT * FROM usuarios")
    processar(dados)
} catch (e: Exception) {
    println("Erro na consulta: ${e.message}")
} finally {
    conexao?.fechar()  // sempre fechar, mesmo se houver erro
}
```

---

## Exceções Customizadas

### Declaração

```kotlin
// Exceção simples
class UsuarioNaoEncontroException(val id: String) :
    Exception("Usuário não encontrado: $id")

// Exceção com código de erro
class ErroValidacao(
    val campo: String,
    val mensagem: String
) : Exception("Validação falhou no campo '$campo': $mensagem")

// Exceção hierárquica
open class ErroAplicacao(mensagem: String) : Exception(mensagem)

class ErroAutenticacao(mensagem: String) : ErroAplicacao(mensagem)
class ErroAutorizacao(mensagem: String)   : ErroAplicacao(mensagem)
class ErroDados(mensagem: String)         : ErroAplicacao(mensagem)
```

### Uso

```kotlin
fun buscarUsuario(id: String): Usuario {
    val usuario = repositorio.findById(id)
    return usuario ?: throw UsuarioNaoEncontroException(id)
}

fun validarEmail(email: String) {
    if (!email.contains("@")) {
        throw ErroValidacao("email", "deve conter @")
    }
    if (email.length > 255) {
        throw ErroValidacao("email", "máximo 255 caracteres")
    }
}

// Tratamento com hierarquia
try {
    autenticar(credenciais)
} catch (e: ErroAutenticacao) {
    println("Credenciais inválidas")
} catch (e: ErroAutorizacao) {
    println("Sem permissão")
} catch (e: ErroAplicacao) {
    println("Erro da aplicação: ${e.message}")
}
```

---

## Result<T> — Tratamento Funcional

`Result<T>` encapsula o resultado de uma operação: `Success<T>` ou `Failure`. Evita exceções para controle de fluxo.

### Criação

```kotlin
// Sucesso
val sucesso: Result<Int> = Result.success(42)

// Falha
val falha: Result<Int> = Result.failure(Exception("Algo deu errado"))

// runCatching: executa bloco e captura exceção automaticamente
val resultado: Result<Int> = runCatching {
    "123".toInt()
}

val resultado2: Result<Int> = runCatching {
    "abc".toInt()  // lança NumberFormatException — capturado automaticamente
}
```

### Verificação

```kotlin
val resultado = runCatching { "42".toInt() }

// Verificar sucesso/falha
println(resultado.isSuccess)   // true
println(resultado.isFailure)   // false

// Obter valor (lança se Failure)
val valor = resultado.getOrThrow()   // 42

// Obter valor com padrão
val valor2 = resultado.getOrDefault(0)  // 42

// Obter valor com else
val valor3 = resultado.getOrElse { 0 }  // 42
```

### Encadeamento com map / flatMap

```kotlin
fun parseIdade(entrada: String): Result<Int> = runCatching {
    val idade = entrada.toInt()
    require(idade in 0..150) { "Idade fora do intervalo" }
    idade
}

fun validarMaioridade(idade: Int): Result<Int> = runCatching {
    require(idade >= 18) { "Deve ser maior de idade" }
    idade
}

// Encadeamento
val resultado = parseIdade("25")
    .flatMap { validarMaioridade(it) }
    .map { idade -> "Idade válida: $idade" }

println(resultado)  // Success(Idade válida: 25)

// Com entrada inválida
val falha = parseIdade("abc")
    .flatMap { validarMaioridade(it) }
    .map { idade -> "Idade válida: $idade" }

println(falha)  // Failure(NumberFormatException)
```

### Tratamento Final

```kotlin
val resultado = processarDados(entrada)

resultado
    .onSuccess { dados -> println("Dados processados: $dados") }
    .onFailure { erro -> println("Falha: ${erro.message}") }

// fold: trata ambos os casos
val mensagem = resultado.fold(
    onSuccess = { dados -> "OK: $dados" },
    onFailure = { erro  -> "Erro: ${erro.message}" }
)
println(mensagem)
```

---

## Exceções em Coroutines

### Comportamento Padrão

Exceções não tratadas em coroutines cancelam o scope pai (structured concurrency).

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    try {
        launch {
            delay(100)
            throw RuntimeException("Falha no coroutine!")
        }
        // Sem try/catch, a exceção propaga para runBlocking
    } catch (e: Exception) {
        println("Capturado: ${e.message}")
    }
}
```

### CoroutineExceptionHandler

Handler global para exceções não tratadas dentro de um scope.

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    println("Handler capturou: ${exception.message}")
}

fun main() = runBlocking {
    val scope = CoroutineScope(Dispatchers.Default + handler)

    scope.launch {
        throw RuntimeException("Erro não tratado")
        // NÃO cancela outros coroutines no scope quando usa handler
    }

    scope.launch {
        delay(500)
        println("Este coroutine executa normalmente")
    }

    delay(1000)
}
```

### SupervisorJob: Isolando Falhas

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

scope.launch { throw RuntimeException("Job 1 falhou") }  // não cancela Job 2

scope.launch {
    delay(200)
    println("Job 2 completou")  // executa normalmente
}
```

### Tratando Exceções com async/await

```kotlin
val deferred = async {
    delay(100)
    throw IllegalStateException("Erro assíncrono")
}

try {
    deferred.await()  // exceção é lançada no ponto do await
} catch (e: IllegalStateException) {
    println("Capturado: ${e.message}")
}
```

---

## Patterns Comuns

### Either Pattern (Alternativa ao Result)

```kotlin
sealed class Either<out L, out R> {
    data class Left<L>(val valor: L) : Either<L, Nothing>   // erro
    data class Right<R>(val valor: R) : Either<Nothing, R>  // sucesso
}

fun dividir(a: Double, b: Double): Either<String, Double> =
    if (b == 0.0) Either.Left("Divisão por zero")
    else Either.Right(a / b)

when (val resultado = dividir(10.0, 3.0)) {
    is Either.Left  -> println("Erro: ${resultado.valor}")
    is Either.Right -> println("Resultado: ${resultado.valor}")
}
```

### Retry com Backoff

```kotlin
suspend fun <T> retry(tentativas: Int = 3, delayInicial: Long = 1000L, bloco: suspend () -> T): T {
    var ultima: Exception? = null
    for (tentativa in 1..tentativas) {
        try { return bloco() }
        catch (e: Exception) {
            ultima = e
            if (tentativa < tentativas) delay(delayInicial * tentativa)
        }
    }
    throw ultima!!
}

val dados = retry(tentativas = 3) { buscarDadosRemoto() }
```

---

## Best Practices

### Usar

```kotlin
// Usar Result para operações que podem falhar de forma previsível
fun buscar(id: String): Result<Usuario> = runCatching {
    repositorio.findById(id) ?: throw UsuarioNaoEncontroException(id)
}

// Usar exceções customizadas para erros do domínio
class SaldoInsuficenteException(val saldo: Double, val valorPedido: Double) :
    Exception("Saldo insuficiente: tem $saldo, pediu $valorPedido")

// Usar finally para liberar recursos
try { /* ... */ } finally { recurso.fechar() }

// Usar SupervisorJob em coroutines independentes
val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
```

### Evitar

```kotlin
// NÃO usar exceções para controle de fluxo normal
// Evitar:
try {
    val item = lista[indice]  // IndexOutOfBoundsException para fluxo normal
} catch (e: IndexOutOfBoundsException) { }
// Usar:
val item = lista.getOrNull(indice)

// NÃO engolir exceções em silêncio
catch (e: Exception) {
    // VAZIO — nunca fazer isso
}
// Pelo menos logar:
catch (e: Exception) {
    logger.error("Erro:", e)
}

// NÃO abusar de catch genérico (Exception)
catch (e: Exception) { }  // prefer tipos específicos

// NÃO ignorar CancellationException em coroutines
catch (e: CancellationException) {
    throw e  // SEMPRE re-throw
}
```

---

## Referências

- [Kotlin Exceptions](https://kotlinlang.org/docs/exceptions.html) — Documentação oficial
- [Kotlin Result](https://kotlinlang.org/docs/api/latest/jvm/stdlib/kotlin/-result/) — API oficial
- [Kotlin Coroutine Exceptions](https://kotlinlang.org/docs/exceptions.html) — Guia de exceções em coroutines
- [Effective Kotlin — Error Handling](https://effectivekotlin.com/) — Boas práticas
