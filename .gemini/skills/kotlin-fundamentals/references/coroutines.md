# Coroutines em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Suspend Functions, Scopes, Dispatchers, Channels

---

## Overview

Coroutines são o mecanismo de concorrência estruturada do Kotlin. Permitem escrever código assíncrono de forma sequencial, sem callbacks ou threads explícitas.

**Disponível desde**: Kotlin 1.3 (estável)
**Biblioteca**: `kotlinx-coroutines-core`

---

## Conceitos Fundamentais

### suspend functions

Funções marcadas com `suspend` podem pausar a execução e ser retomadas mais tarde. Só podem ser chamadas de outras funções `suspend` ou de um coroutine scope.

```kotlin
import kotlinx.coroutines.*

// Função suspensa: pode pausar sem bloquear a thread
suspend fun buscarUsuario(id: Int): String {
    delay(500)  // pausa por 500ms sem bloquear thread
    return "Usuário $id"
}

// Chamada de dentro de um scope
fun main() = runBlocking {
    val usuario = buscarUsuario(1)
    println(usuario)  // "Usuário 1"
}
```

**Bloqueio vs Suspensão**: `Thread.sleep()` ocupa a thread inteira; `delay()` suspende o coroutine e libera a thread para outras tarefas.

---

## Scopes Principais

### runBlocking

Usado como ponto de entrada. Bloqueia a thread chamadora até todos os coroutines filhos terminarem.

```kotlin
fun main() = runBlocking {
    println("Início")
    delay(1000)
    println("Fim")
}
// Output:
// Início
// (pausa 1s)
// Fim
```

### launch

Inicia um coroutine que não retorna valor. Retorna um `Job` para controle do ciclo de vida.

```kotlin
fun main() = runBlocking {
    val job1 = launch {
        delay(500)
        println("Job 1 finalizado")
    }

    val job2 = launch {
        delay(300)
        println("Job 2 finalizado")
    }

    // Aguarda ambos automaticamente (structured concurrency)
    println("Aguardando...")
}
// Output:
// Aguardando...
// Job 2 finalizado  (300ms)
// Job 1 finalizado  (500ms)
```

### async / await

Usado quando o coroutine precisa retornar um valor. Retorna um `Deferred<T>`.

```kotlin
fun main() = runBlocking {
    // Inicia dois coroutines em paralelo
    val deferred1 = async {
        delay(500)
        10
    }

    val deferred2 = async {
        delay(300)
        20
    }

    // await bloqueia (suspende) até o resultado estar pronto
    val soma = deferred1.await() + deferred2.await()
    println("Soma: $soma")  // Soma: 30
    // Tempo total: ~500ms (não 800ms, pois executaram em paralelo)
}
```

### CoroutineScope

Cria um escopo customizado para gerenciar o ciclo de vida dos coroutines.

```kotlin
class ServicoFetch {
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun buscar(url: String) {
        scope.launch {
            val dados = buscarUrl(url)
            println(dados)
        }
    }

    fun cancelar() = scope.cancel()  // cancela todos os coroutines

    private suspend fun buscarUrl(url: String): String {
        delay(1000)
        return "Dados de $url"
    }
}
```

---

## Dispatchers

Dispatchers controlam em qual thread o coroutine executa.

### Dispatchers.Main

Thread principal da aplicação. Usado para operações de UI.

```kotlin
// Executa na main thread
launch(Dispatchers.Main) {
    // atualizar UI aqui
}
```

### Dispatchers.IO

Thread pool otimizada para operações de I/O (rede, disco).

```kotlin
launch(Dispatchers.IO) {
    val dados = lerArquivo("dados.txt")
    println(dados)
}
```

### Dispatchers.Default

Thread pool para operações CPU-intensive (cálculos pesados).

```kotlin
launch(Dispatchers.Default) {
    val resultado = calcularPrimos(1_000_000)
    println("Primos encontrados: $resultado")
}
```

### withContext

Muda o dispatcher dentro de um coroutine existente, sem criar novo scope.

```kotlin
suspend fun processarDados(): String {
    // Busca no IO
    val dados = withContext(Dispatchers.IO) {
        lerArquivo("entrada.txt")
    }

    // Processa no Default (CPU-intensive)
    val resultado = withContext(Dispatchers.Default) {
        transformar(dados)
    }

    return resultado
}
```

---

## Job e Controle de Ciclo de Vida

### Cancelamento

```kotlin
fun main() = runBlocking {
    val job = launch {
        repeat(10) { i ->
            delay(200)
            println("Iteração $i")
        }
    }

    delay(500)        // após 500ms...
    job.cancel()      // cancela o coroutine
    job.join()        // aguarda o cancelamento completar
    println("Job cancelado")
}
// Output:
// Iteração 0
// Iteração 1
// Iteração 2
// Job cancelado
```

### isActive

```kotlin
launch {
    while (isActive) {  // verifica se o coroutine ainda está ativo
        delay(100)
        println("Ainda ativo...")
    }
}
```

### SupervisorJob

Quando um coroutine filho falha, não cancela os outros.

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

scope.launch {
    throw RuntimeException("Falha no job 1")  // não afeta job 2
}

scope.launch {
    delay(1000)
    println("Job 2 completou")  // executa normalmente
}
```

---

## Channels Básicos

Channels são um mecanismo de comunicação entre coroutines (equivalente a filas thread-safe).

### Channel básico

```kotlin
import kotlinx.coroutines.channels.*

fun main() = runBlocking {
    val canal = Channel<Int>()

    // Producer
    launch {
        for (i in 1..5) {
            canal.send(i)
        }
        canal.close()  // sinaliza fim de envio
    }

    // Consumer
    for (valor in canal) {  // itera até o canal estar fechado
        println("Recebido: $valor")
    }
}
// Output:
// Recebido: 1
// Recebido: 2
// ...
// Recebido: 5
```

### produce (builder)

```kotlin
import kotlinx.coroutines.channels.*

fun producir(): ReceiveChannel<Int> = produce {
    for (i in 1..5) {
        delay(100)
        send(i * i)
    }
}

fun main() = runBlocking {
    for (valor in producir()) {
        println("Quadrado: $valor")  // 1, 4, 9, 16, 25
    }
}
```

### Channel com buffer

```kotlin
// Sem buffer (rendezvous): send bloqueia até alguém receber
val canal1 = Channel<String>()

// Com buffer: send não bloqueia até o buffer estar cheio
val canal2 = Channel<String>(capacity = 3)

// Buffer ilimitado
val canal3 = Channel<String>(Channel.UNLIMITED)
```

---

## Patterns Comuns

### Fan-out / Fan-in

```kotlin
fun main() = runBlocking {
    val trabalhos = Channel<Int>()
    val resultados = Channel<Int>()

    // Fan-out: 3 workers consumindo do mesmo canal
    repeat(3) {
        launch(Dispatchers.Default) {
            for (trabalho in trabalhos) {
                resultados.send(trabalho * 2)
            }
        }
    }

    launch {
        for (i in 1..9) trabalhos.send(i)
        trabalhos.close()
    }

    repeat(9) { println("Resultado: ${resultados.receive()}") }
}
```

### Timeout

```kotlin
val resultado = withTimeoutOrNull(500) {
    delay(1000)       // excede o timeout
    "Dado obtido"
}
println(resultado ?: "Timeout! Dado não obtido a tempo.")
// Output: Timeout! Dado não obtido a tempo.
```

---

## Best Practices

### Usar

```kotlin
// Usar structured concurrency: coroutines dentro de scopes definidos
runBlocking {
    launch { /* task 1 */ }
    launch { /* task 2 */ }
    // scope aguarda ambos automaticamente
}

// Usar withContext para mudar dispatcher sem novo scope
val dados = withContext(Dispatchers.IO) { lerArquivo() }

// Usar SupervisorJob para isolar falhas entre coroutines filhos
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

// Usar withTimeoutOrNull para evitar espera infinita
val resultado = withTimeoutOrNull(5000) { buscarDados() }
```

### Evitar

```kotlin
// NÃO usar GlobalScope (ciclo de vida não controlado)
GlobalScope.launch { /* ... */ }  // evitar

// NÃO misturar bloqueio com suspensão
runBlocking {
    Thread.sleep(1000)  // bloqueia a thread — usar delay()
}

// NÃO ignorar cancelamento
launch {
    try {
        delay(Long.MAX_VALUE)
    } catch (e: CancellationException) {
        // NÃO engole a exceção de silêncio
        throw e  // re-throw
    }
}

// NÃO criar coroutines sem scope definido
// Sempre use runBlocking, launch dentro de scope, ou CoroutineScope explícito
```

---

## Referências

- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html) — Documentação oficial
- [Kotlin in Action, Cap. Coroutines](https://www.manning.com/books/kotlin-in-action-second-edition) — Exemplos práticos
- [Effective Kotlin — Coroutines](https://effectivekotlin.com/) — Boas práticas
