# Evolução do Kotlin: Versões e o Compilador K2

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: Diferenças entre versões Kotlin 1.x e 2.x, compilador K2, migração

---

## Visão Geral da Evolução

O Kotlin passou por fases claras de maturação. Cada versão principal introduziu recursos que mudaram como a linguagem é usada na prática. O maior salto técnico foi a introdução do **compilador K2** em 2024, que substituiu o compilador original (K1) como padrão no Kotlin 2.0.

```
Kotlin 1.0 (2016) — Lançamento oficial, basics
  │
  ├── 1.1-1.2  — Coroutines experimentais, multiplatform experimentais
  ├── 1.3      — Coroutines estáveis, inline classes experimentais
  ├── 1.4      — SAM conversions, fun interfaces
  ├── 1.5      — Sealed interfaces, value classes estáveis, SAM estáveis
  ├── 1.6      — Sealed when obrigatório (warning), opt-in APIs
  ├── 1.7      — Builder inference, IR backend padrão
  ├── 1.8      — Compatibilidade JVM aprimorada
  ├── 1.9      — K2 compiler experimentais, stdlib estabilizações
  └── 2.0 (2024) — K2 compiler padrão, breaking changes mínimos
```

---

## Kotlin 1.x — Fundação (2016-2023)

### 1.0 – 1.2: O Início

Versões de fundação. Étableceram o sistema de tipos null-safe, data classes, companion objects e a base da linguagem.

```kotlin
// Kotlin 1.0+: básicos sempre disponíveis
val nome: String = "Alice"
val idade: Int? = null

data class Pessoa(val nome: String, val idade: Int)

companion object {
    fun criar(): Pessoa = Pessoa("Bob", 30)
}
```

### 1.3: Coroutines Estáveis

Maior marco da série 1.x. Coroutines saíram de experimentais para estáveis, habilitando programação assíncrona sem callbacks.

```kotlin
// Disponível desde 1.3 estável
import kotlinx.coroutines.*

suspend fun buscar(id: Int): String {
    delay(100)
    return "Item $id"
}

fun main() = runBlocking {
    val resultado = buscar(1)
    println(resultado)
}
```

Também nesta versão: `inline classes` experimentais (que se tornaram `value classes` em 1.5).

### 1.4 – 1.5: Interfaces e Types

**1.4** introduziu `fun interface` — permite usar interfaces com um único método como SAM (Single Abstract Method), similar ao Java:

```kotlin
// Disponível desde 1.4
fun interface Validador {
    fun validar(valor: String): Boolean
}

// Uso com lambda (sem precisar de classe anônima)
val naoVazio = Validador { it.isNotBlank() }
println(naoVazio.validar("hello"))  // true
```

**1.5** estabilizou `sealed interfaces` e `value classes`:

```kotlin
// Sealed interface: disponível desde 1.5
sealed interface Forma {
    data class Circulo(val raio: Double) : Forma
    data class Retangulo(val w: Double, val h: Double) : Forma
}

// Value class estável desde 1.5
@JvmInline
value class Email(val endereco: String) {
    init { require("@" in endereco) }
}
```

### 1.6 – 1.9: Refinamentos e Preparação para K2

**1.6** começou a exigir branches exhaustivos em `when` com sealed types (warning, não erro ainda):

```kotlin
// 1.6+: warning se 'else' faltante em when com sealed
fun area(forma: Forma): Double = when (forma) {
    is Forma.Circulo    -> Math.PI * forma.raio * forma.raio
    is Forma.Retangulo  -> forma.w * forma.h
    // sem else: warning em 1.6, erro em 2.0
}
```

**1.7** trouxe `builder inference` — o compilador infere tipos em lambdas de builder automaticamente:

```kotlin
// Builder inference (1.7+)
val mapa = buildMap {
    put("a", 1)
    put("b", 2)
}  // Tipo inferido: Map<String, Int>
```

**1.9** foi a última versão com K1 como padrão. Muitas estabilizações da stdlib e preparação para K2.

---

## Kotlin 2.0 e o Compilador K2

### O Que Mudou no Compilador

O **K2** é uma reescrita completa do frontend do compilador Kotlin. Ele não muda a linguagem em si, mas muda **como** o compilador processa e valida o código.

| Aspecto | K1 (compilador original) | K2 (novo, padrão em 2.0) |
|---------|--------------------------|--------------------------|
| **Velocidade** | Baseline | 1.5x – 2x mais rápido em média |
| **Smart Cast** | Limitado a controle de fluxo simples | Muito mais poderoso — funciona com `var` mutable em mais contextos |
| **Diagnósticos** | Mensagens de erro básicas | Mensagens mais descritivas e úteis |
| **IDE Support** | Funciona com todos os plugins | Melhor integração com IntelliJ/Android Studio |
| **Multiplatform** | Suporte básico | Suporte aprimorado e mais estável |

### Smart Cast Aprimorado no K2

Esta é a maior diferença prática para o código do usuário:

```kotlin
// K1: smart cast NÃO funcionava com var mutable em muitos casos
var valor: String? = obter()

if (valor != null) {
    // K1: erro potencial — valor é var, pode mudar entre a verificação e o uso
    // K2: OK em contextos single-threaded, compilador rastreia melhor
    println(valor.length)
}
```

```kotlin
// K2 smart cast com open val em classes
open class Base {
    open val nome: String? = null
}

class Derivada : Base() {
    override val nome = "Teste"
}

fun processar(obj: Base) {
    if (obj.nome != null) {
        // K1: não fazia smart cast (open val pode ser sobrescrito)
        // K2: faz smart cast se não for open no contexto ou se for val final
        println(obj.nome.length)
    }
}
```

### When Exhaustivo Obrigatório

Em Kotlin 2.0 com K2, `when` em sealed types **deve** ser exhaustivo (sem `else` facultativo):

```kotlin
sealed interface Estado {
    object Carregando : Estado
    data class Carregado(val dados: String) : Estado
    data class Erro(val mensagem: String) : Estado
}

// 2.0+: compilador exige todas as branches
fun renderizar(estado: Estado): String = when (estado) {
    is Estado.Carregando -> "Carregando..."
    is Estado.Carregado  -> estado.dados
    is Estado.Erro       -> "Erro: ${estado.mensagem}"
    // sem else necessário — e sem else permitido desnecessariamente
}

// Se adicionar novo estado à sealed interface,
// o compilador aponta TODOS os when que precisam atualizar
```

### Novo Estado Padrão: `when` como Statement

```kotlin
// Como statement (não retorna valor): K2 também exige exhaustividade
// quando usado com sealed types em certas situações
val estado: Estado = Estado.Carregado("dados")

when (estado) {
    is Estado.Carregando -> println("...")
    is Estado.Carregado  -> println(estado.dados)
    is Estado.Erro       -> println(estado.mensagem)
}
```

---

## Comparação Prática: Código em 1.x vs 2.x

### Exemplo 1: Tratamento de Nullable

```kotlin
// ===== Estilo Kotlin 1.x (ainda válido em 2.x) =====
fun buscar(id: Int): String? {
    val cache = memoCache[id]
    if (cache != null) {
        return cache
    }
    return null
}

// ===== Estilo Kotlin moderno (idiomático 1.5+/2.x) =====
fun buscar(id: Int): String? =
    memoCache[id]  // retorna null automaticamente se não encontrar

// Com elvis na chamada:
val valor = buscar(42) ?: "padrão"
```

### Exemplo 2: Hierarquias de Tipo

```kotlin
// ===== Kotlin 1.0-1.4: abstract class para hierarquias =====
abstract class Evento {
    data class Click(val x: Int, val y: Int) : Evento()
    data class Teclado(val chave: String) : Evento()
}

// ===== Kotlin 1.5+/2.x: sealed interface (preferred) =====
sealed interface Evento {
    data class Click(val x: Int, val y: Int) : Evento
    data class Teclado(val chave: String) : Evento
}
// Benefício: implementações DEVEM estar no mesmo arquivo
// when é exhaustivo sem else
```

### Exemplo 3: Assincronia

```kotlin
// ===== Callbacks (pré-coroutines, evitar) =====
fun buscarAsync(id: Int, callback: (String?) -> Unit) {
    Thread {
        callback(db.buscar(id))
    }.start()
}

// ===== Coroutines 1.3+ (padrão atual) =====
suspend fun buscar(id: Int): String? = withContext(Dispatchers.IO) {
    db.buscar(id)
}

// ===== Flow para streams (1.4+) =====
fun observar(): Flow<String> = flow {
    while (true) {
        emit(db.buscar(Random.nextInt()))
        delay(1000)
    }
}
```

### Exemplo 4: Collections

```kotlin
// ===== Estilo imperativo (válido mas não idiomático) =====
val resultado = mutableListOf<String>()
for (item in lista) {
    if (item.ativo) {
        resultado.add(item.nome.uppercase())
    }
}

// ===== Estilo funcional (idiomático desde 1.0, preferred) =====
val resultado = lista
    .filter { it.ativo }
    .map { it.nome.uppercase() }

// ===== Sequences para dados grandes (1.0+, mas common desde 1.3+) =====
val resultado = lista.asSequence()
    .filter { it.ativo }
    .map { it.nome.uppercase() }
    .toList()  // avaliação lazy até aqui
```

---

## Checklist de Migração: 1.x → 2.x

Se seu projeto usa Kotlin 1.x e você está considerando migrar para 2.x:

- [ ] Atualizar `kotlin` plugin no build tool para versão 2.x
- [ ] Revisar todos os `when` com sealed types — adicionar branches ausentes
- [ ] Remover `else` desnecessários em `when` com sealed types
- [ ] Verificar uso de `!!` — K2 smart cast pode eliminar muitos
- [ ] Revisar `var` com nullable — K2 pode simplificar verificações
- [ ] Executar o compilador K2 em modo experimentai primeiro (`-Xuse-k2` em 1.9)
- [ ] Verificar compatibilidade de plugins e ferramentas com K2
- [ ] Revisar warnings de deprecação da stdlib

---

## Versões Recomendadas por Contexto

| Contexto | Versão Recomendada | Motivo |
|----------|-------------------|--------|
| Novo projeto (2024+) | **2.0** | K2 padrão, todos os recursos |
| Projeto existente estável | **1.9** | Última versão K1, mínimas breaking changes |
| Android (recente) | **2.0+** | Android Studio alinha com K2 |
| JVM backend genérico | **1.9 ou 2.0** | Ambas estáveis e bem suportadas |
| Projeto com muitas dependências | **1.9** | Maior compatibilidade com ecossistema |

---

## Referências

- [Kotlin 2.0 What's New](https://kotlinlang.org/docs/whatsnew20.html) — Documentação oficial
- [K2 Compiler Migration Guide](https://kotlinlang.org/docs/k2-migration-guide.html) — Guia de migração oficial
- [Kotlin Evolution: Versões](https://kotlinlang.org/docs/whats-new.html) — Histórico completo
- [Kotlin in Action, 2nd Edition](https://www.manning.com/books/kotlin-in-action-second-edition) — Cobre evolução até 2.0
