# Collections em Kotlin

> **Referência avançada de**: kotlin-fundamentals
> **Tópico**: List, Set, Map, Sequences, Operações Funcionais

---

## Overview

Kotlin oferece uma hierarquia de collections rica com suporte nativo a collections mutáveis e imutáveis, além de um conjunto extenso de funções de extensão para processamento funcional.

**Princípio**: Collections são **imutáveis por padrão**. Versões mutáveis são explícitas.

---

## List

### Criação

```kotlin
// Imutável (somente leitura)
val frutas: List<String> = listOf("Maçã", "Banana", "Laranja")

// Mutável
val frutas2: MutableList<String> = mutableListOf("Maçã", "Banana")
frutas2.add("Laranja")
frutas2.remove("Banana")

// Vazio
val vazio: List<Int> = emptyList()

// Com valor repetido
val uns: List<Int> = List(5) { 1 }          // [1, 1, 1, 1, 1]

// Com gerador
val quadrados: List<Int> = List(5) { it * it }  // [0, 1, 4, 9, 16]

// ArrayList explícito
val arrayList = ArrayList<String>()
arrayList.add("Item 1")
```

### Acesso

```kotlin
val lista = listOf("A", "B", "C", "D")

lista[0]                    // "A" — acesso por índice
lista.first()               // "A"
lista.last()                // "D"
lista.getOrNull(10)         // null (sem exceção)
lista.getOrElse(10) { "?" } // "?" (valor padrão)
lista.size                  // 4
lista.isEmpty()             // false
lista.contains("B")         // true
lista.indexOf("C")          // 2
```

### Iteração

```kotlin
val nomes = listOf("Alice", "Bob", "Carlos")

// forEach
nomes.forEach { println(it) }

// forEachIndexed
nomes.forEachIndexed { index, nome ->
    println("$index: $nome")
}

// for tradicionai
for (nome in nomes) {
    println(nome)
}

// for com índice
for (i in nomes.indices) {
    println("${i}: ${nomes[i]}")
}
```

---

## Set

```kotlin
// Imutável — sem duplicatas, sem ordem garantida
val cores: Set<String> = setOf("Vermelho", "Azul", "Verde")

// Mutável
val cores2: MutableSet<String> = mutableSetOf("Vermelho", "Azul")
cores2.add("Verde")
cores2.add("Vermelho")  // ignorado — já existe
println(cores2.size)     // 2 (sem duplicata)

// LinkedHashSet — mantém ordem de inserção
val ordenado: MutableSet<String> = linkedSetOf("C", "A", "B")
// Iteração: C, A, B

// TreeSet — ordenado naturalmente
val sorted = sortedSetOf("Banana", "Maçã", "Laranja")
// Iteração: Banana, Laranja, Maçã (ordem alfabética)

// Operações de conjunto
val a = setOf(1, 2, 3, 4)
val b = setOf(3, 4, 5, 6)

val uniao        = a + b            // [1, 2, 3, 4, 5, 6]  (union)
val intersecao   = a.intersect(b)   // [3, 4]
val diferenca    = a - b            // [1, 2]  (subtraction)
val simetrica    = a.subtract(b) + b.subtract(a)  // diferença simétrica
```

---

## Map

### Criação

```kotlin
// Imutável
val idades: Map<String, Int> = mapOf(
    "Alice" to 30,
    "Bob" to 25,
    "Carlos" to 35
)

// Mutável
val idades2: MutableMap<String, Int> = mutableMapOf()
idades2["Alice"] = 30
idades2["Bob"] = 25

// HashMap explícito
val hashMap = HashMap<String, Int>()
hashMap["chave"] = 42

// LinkedHashMap — mantém ordem de inserção
val linkedMap = linkedMapOf("C" to 3, "A" to 1, "B" to 2)

// TreeMap — chaves ordenadas
val treeMap = sortedMapOf("Banana" to 2, "Maçã" to 1)
```

### Acesso

```kotlin
val map = mapOf("nome" to "Alice", "cidade" to "SP")

map["nome"]                          // "Alice"
map["inexistente"]                   // null
map.getOrDefault("inexistente", "?") // "?"
map.getValue("nome")                 // "Alice" (throws se não existir)
map.containsKey("nome")              // true
map.containsValue("Alice")           // true
map.keys                             // Set<String>
map.values                           // Collection<String>
map.entries                          // Set<Map.Entry<String, String>>
```

### Iteração

```kotlin
val capitais = mapOf("BR" to "Brasília", "US" to "Washington", "FR" to "Paris")

// forEach com destructuring
capitais.forEach { (pais, capital) ->
    println("$pais -> $capital")
}

// Iteração sobre entries
for ((pais, capital) in capitais) {
    println("$pais: $capital")
}

// Apenas chaves ou valores
capitais.keys.forEach { println(it) }
capitais.values.forEach { println(it) }
```

### Operações Comuns

```kotlin
val mapa = mutableMapOf("a" to 1, "b" to 2)

// putIfAbsent
mapa.putIfAbsent("c", 3)   // adiciona "c" -> 3
mapa.putIfAbsent("a", 99)  // não altera, "a" já existe

// getOrPut
val valor = mapa.getOrPut("d") { 4 }  // adiciona "d" -> 4 se não existir

// merge
mapa.merge("a", 10) { antigo, novo -> antigo + novo }
// "a" -> 11 (1 + 10)

// computeIfAbsent
mapa.computeIfAbsent("e") { 5 }
```

---

## Sequences (Lazy Evaluation)

Sequences processam elementos sob demanda (lazy), evitando criação de coleções intermediárias. Ideal para dados grandes.

### Criação

```kotlin
// De uma lista existente
val seq = listOf(1, 2, 3, 4, 5).asSequence()

// Gerador infinito
val naturais = generateSequence(1) { it + 1 }  // 1, 2, 3, 4, ...

// Gerador com semente
val potencias = generateSequence(1) { it * 2 }  // 1, 2, 4, 8, 16, ...
```

### Comparação: List vs Sequence

```kotlin
val numeros = (1..1_000_000).toList()

// COM List: cria intermediários na memória
val resultadoList = numeros
    .filter { it % 2 == 0 }      // cria lista com 500k elementos
    .map { it * it }              // cria outra lista com 500k elementos
    .take(5)                      // pega apenas 5

// COM Sequence: lazy, sem intermediários
val resultadoSeq = numeros.asSequence()
    .filter { it % 2 == 0 }      // não executa ainda
    .map { it * it }              // não executa ainda
    .take(5)                      // não executa ainda
    .toList()                     // NOW executa — processa apenas os necessários
```

### Exemplo Prático

```kotlin
// Sequência infinita: primeiros 10 números pares ao quadrado
val resultado = generateSequence(1) { it + 1 }
    .filter { it % 2 == 0 }
    .map { it * it }
    .take(10)
    .toList()
// [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]
```

---

## Operações Funcionais Comuns

### filter / reject

```kotlin
val numeros = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

val pares = numeros.filter { it % 2 == 0 }       // [2, 4, 6, 8, 10]
val impares = numeros.filter { it % 2 != 0 }     // [1, 3, 5, 7, 9]
val grandes = numeros.filter { it > 5 }           // [6, 7, 8, 9, 10]
```

### map / flatMap

```kotlin
val nomes = listOf("alice", "bob", "carlos")

// map: transforma cada elemento
val maiusculos = nomes.map { it.uppercase() }     // ["ALICE", "BOB", "CARLOS"]
val tamanhos = nomes.map { it.length }            // [5, 3, 6]

// flatMap: transforma e "achata"
val frases = listOf("Olá Mundo", "Kotlin é ótimo")
val palavras = frases.flatMap { it.split(" ") }
// ["Olá", "Mundo", "Kotlin", "é", "ótimo"]
```

### reduce / fold

```kotlin
val numeros = listOf(1, 2, 3, 4, 5)

// reduce: sem valor inicial (usa primeiro elemento)
val soma = numeros.reduce { acum, valor -> acum + valor }  // 15

// fold: com valor inicial
val somaFold = numeros.fold(0) { acum, valor -> acum + valor }  // 15
val produto = numeros.fold(1) { acum, valor -> acum * valor }   // 120

// fold para construir string
val texto = numeros.fold("Números:") { acum, valor -> "$acum $valor" }
// "Números: 1 2 3 4 5"
```

### groupBy / partition

```kotlin
data class Pessoa(val nome: String, val idade: Int)

val pessoas = listOf(
    Pessoa("Alice", 30),
    Pessoa("Bob", 17),
    Pessoa("Carlos", 25),
    Pessoa("Diana", 15)
)

// groupBy: agrupa em Map
val porIdade = pessoas.groupBy { if (it.idade >= 18) "adulto" else "menor" }
// {"adulto": [Alice, Carlos], "menor": [Bob, Diana]}

// partition: divide em dois grupos (true/false)
val (adultos, menores) = pessoas.partition { it.idade >= 18 }
// adultos: [Alice, Carlos]
// menores: [Bob, Diana]
```

### sortedBy / sortedWith

```kotlin
val produtos = listOf(
    Produto("Notebook", 4999.0),
    Produto("Mouse", 49.0),
    Produto("Teclado", 129.0)
)

val porPreco = produtos.sortedBy { it.preco }             // crescente
val porPrecoDesc = produtos.sortedByDescending { it.preco } // decrescente

// Ordenação composta
val ordenado = produtos.sortedWith(
    compareBy<Produto> { it.preco }.thenBy { it.nome }
)
```

### find / any / all / none

```kotlin
val numeros = listOf(1, 2, 3, 4, 5)

numeros.find { it > 3 }           // 4 (primeiro que satisfaz)
numeros.any { it > 4 }            // true (pelo menos um)
numeros.all { it > 0 }            // true (todos)
numeros.none { it > 10 }          // true (nenhum)
numeros.count { it % 2 == 0 }     // 2
numeros.sum()                     // 15
numeros.min()                     // 1
numeros.max()                     // 5
```

### zip / associate

```kotlin
val nomes = listOf("Alice", "Bob", "Carlos")
val idades = listOf(30, 25, 35)

// zip: combina duas listas em pares
val pares = nomes.zip(idades)  // [(Alice,30), (Bob,25), (Carlos,35)]

// zipWith: combina com função
val descricoes = nomes.zip(idades) { nome, idade -> "$nome ($idade anos)" }

// associate: cria Map a partir de lista
val mapa = nomes.zip(idades).toMap()  // {Alice=30, Bob=25, Carlos=35}

// associateBy: cria Map usando campo como chave
val porNome = listOf(Pessoa("Alice", 30), Pessoa("Bob", 25))
    .associateBy { it.nome }
// {Alice=Pessoa(Alice,30), Bob=Pessoa(Bob,25)}
```

---

## Best Practices

### Usar

```kotlin
// Usar collections imutáveis por padrão
val lista = listOf(1, 2, 3)           // List<Int> — somente leitura
val mapa = mapOf("a" to 1)            // Map — somente leitura

// Usar sequences para dados grandes ou infinitos
val resultado = (1..Int.MAX_VALUE).asSequence()
    .filter { it % 3 == 0 }
    .take(100)
    .toList()

// Usar destructuring declarations
val (primeiro, segundo) = listOf("A", "B", "C")
val (chave, valor) = mapOf("nome" to "Alice").entries.first()
```

### Evitar

```kotlin
// NÃO usar MutableList quando List é suficiente
val lista = mutableListOf(1, 2, 3)  // evitar se não vai modificar

// NÃO criar listas intermediárias desnecessárias com dados grandes
val resultado = enormeLista
    .filter { ... }   // cria nova lista
    .map { ... }      // cria outra lista
// Usar .asSequence() antes das operações

// NÃO usar indices quando forEach ou for-in é mais legível
for (i in lista.indices) {    // menos idiomático
    println(lista[i])
}
lista.forEach { println(it) } // mais idiomático
```

---

## Referências

- [Kotlin Collections Overview](https://kotlinlang.org/docs/collections-overview.html) — Documentação oficial
- [Kotlin Sequences](https://kotlinlang.org/docs/sequences.html) — Lazy evaluation
- [Effective Kotlin — Collections](https://effectivekotlin.com/) — Boas práticas
