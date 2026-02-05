# Functional Programming in Java

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Advanced Lambdas, Method References, Functional Interfaces

---

## Overview

Java 8+ introduziu programação funcional com:
- Lambdas
- Streams
- Functional Interfaces
- Method References

---

## Lambdas

### Syntax

```java
// Syntax completa
(int a, int b) -> { return a + b; }

// Parâmetros inferidos
(a, b) -> { return a + b; }

// Sem chaves (expressão única)
(a, b) -> a + b

// Parâmetro único (sem parênteses)
x -> x * 2

// Sem parâmetros
() -> System.out.println("Hello")
```

### Examples

```java
// Runnable
Runnable r = () -> System.out.println("Running");

// Comparator
Comparator<String> comp = (s1, s2) -> s1.compareTo(s2);

// Custom functional interface
Calculator calc = (a, b) -> a + b;
int result = calc.calculate(10, 20);  // 30
```

---

## Functional Interfaces

### Built-in Interfaces

```java
// Function<T, R>: T -> R
Function<String, Integer> length = s -> s.length();
int len = length.apply("Hello");  // 5

// Predicate<T>: T -> boolean
Predicate<Integer> isEven = n -> n % 2 == 0;
boolean result = isEven.test(4);  // true

// Consumer<T>: T -> void
Consumer<String> printer = s -> System.out.println(s);
printer.accept("Hello");  // Imprime "Hello"

// Supplier<T>: () -> T
Supplier<Double> random = () -> Math.random();
double value = random.get();  // Número aleatório

// BiFunction<T, U, R>: (T, U) -> R
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
int sum = add.apply(10, 20);  // 30

// UnaryOperator<T>: T -> T (extends Function<T, T>)
UnaryOperator<Integer> square = x -> x * x;
int squared = square.apply(5);  // 25

// BinaryOperator<T>: (T, T) -> T (extends BiFunction<T, T, T>)
BinaryOperator<Integer> max = (a, b) -> a > b ? a : b;
int maximum = max.apply(10, 20);  // 20
```

### Custom Functional Interface

```java
@FunctionalInterface  // Opcional mas recomendado
public interface Calculator {
    int calculate(int a, int b);
    
    // Pode ter métodos default
    default int multiplyAndCalculate(int a, int b, int multiplier) {
        return calculate(a, b) * multiplier;
    }
    
    // Pode ter métodos static
    static Calculator getAdder() {
        return (a, b) -> a + b;
    }
}

// Uso
Calculator adder = (a, b) -> a + b;
Calculator multiplier = (a, b) -> a * b;

int sum = adder.calculate(10, 20);       // 30
int product = multiplier.calculate(10, 20);  // 200
```

---

## Method References

### Types of Method References

```java
// 1. Static method reference
Function<String, Integer> parseInt = Integer::parseInt;
int num = parseInt.apply("123");  // 123

// 2. Instance method reference (bound)
String str = "Hello";
Supplier<Integer> length = str::length;
int len = length.get();  // 5

// 3. Instance method reference (unbound)
Function<String, Integer> length = String::length;
int len = length.apply("Hello");  // 5

// 4. Constructor reference
Supplier<List<String>> listFactory = ArrayList::new;
List<String> list = listFactory.get();

Function<Integer, List<String>> sizedListFactory = ArrayList::new;
List<String> list10 = sizedListFactory.apply(10);
```

### Examples

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// Lambda
names.forEach(name -> System.out.println(name));

// Method reference (mais conciso)
names.forEach(System.out::println);

// Lambda
names.stream()
     .map(name -> name.toUpperCase())
     .collect(Collectors.toList());

// Method reference
names.stream()
     .map(String::toUpperCase)
     .collect(Collectors.toList());
```

---

## Composing Functions

### Function Composition

```java
Function<Integer, Integer> addOne = x -> x + 1;
Function<Integer, Integer> multiplyTwo = x -> x * 2;

// andThen: f.andThen(g) = g(f(x))
Function<Integer, Integer> addThenMultiply = addOne.andThen(multiplyTwo);
int result = addThenMultiply.apply(5);  // (5 + 1) * 2 = 12

// compose: f.compose(g) = f(g(x))
Function<Integer, Integer> multiplyThenAdd = addOne.compose(multiplyTwo);
int result = multiplyThenAdd.apply(5);  // (5 * 2) + 1 = 11
```

### Predicate Composition

```java
Predicate<Integer> isEven = n -> n % 2 == 0;
Predicate<Integer> isPositive = n -> n > 0;

// and
Predicate<Integer> isEvenAndPositive = isEven.and(isPositive);
boolean result = isEvenAndPositive.test(4);  // true

// or
Predicate<Integer> isEvenOrNegative = isEven.or(n -> n < 0);

// negate
Predicate<Integer> isOdd = isEven.negate();
```

---

## Advanced Streams

### Collectors

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// toList
List<String> list = names.stream().collect(Collectors.toList());

// toSet
Set<String> set = names.stream().collect(Collectors.toSet());

// joining
String joined = names.stream().collect(Collectors.joining(", "));
// "Alice, Bob, Charlie"

// groupingBy
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));
// {3=[Bob], 5=[Alice], 7=[Charlie]}

// partitioningBy
Map<Boolean, List<Integer>> evenOdd = Stream.of(1, 2, 3, 4, 5)
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));
// {false=[1, 3, 5], true=[2, 4]}

// counting
long count = names.stream().collect(Collectors.counting());

// summarizingInt
IntSummaryStatistics stats = Stream.of(1, 2, 3, 4, 5)
    .collect(Collectors.summarizingInt(Integer::intValue));
// stats.getSum() = 15
// stats.getAverage() = 3.0
```

### flatMap

```java
List<List<String>> nested = Arrays.asList(
    Arrays.asList("A", "B"),
    Arrays.asList("C", "D"),
    Arrays.asList("E", "F")
);

// Flatten nested lists
List<String> flattened = nested.stream()
    .flatMap(List::stream)
    .collect(Collectors.toList());
// [A, B, C, D, E, F]

// Example: Get all words from sentences
List<String> sentences = Arrays.asList("Hello world", "Java streams");
List<String> words = sentences.stream()
    .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
    .collect(Collectors.toList());
// [Hello, world, Java, streams]
```

### reduce

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Sum
int sum = numbers.stream()
    .reduce(0, (a, b) -> a + b);  // 15

// Sum (method reference)
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Product
int product = numbers.stream()
    .reduce(1, (a, b) -> a * b);  // 120

// Max
Optional<Integer> max = numbers.stream()
    .reduce((a, b) -> a > b ? a : b);

// Max (method reference)
Optional<Integer> max = numbers.stream()
    .reduce(Integer::max);
```

---

## Optional

### Creating Optionals

```java
// of: value non-null
Optional<String> opt1 = Optional.of("Hello");

// ofNullable: value pode ser null
Optional<String> opt2 = Optional.ofNullable(possiblyNull);

// empty
Optional<String> opt3 = Optional.empty();
```

### Using Optionals

```java
Optional<String> opt = Optional.of("Hello");

// isPresent/isEmpty
if (opt.isPresent()) {
    System.out.println(opt.get());
}

// ifPresent (functional)
opt.ifPresent(value -> System.out.println(value));

// ifPresentOrElse (Java 9+)
opt.ifPresentOrElse(
    value -> System.out.println(value),
    () -> System.out.println("Empty")
);

// orElse: default value
String value = opt.orElse("Default");

// orElseGet: lazy default (Supplier)
String value = opt.orElseGet(() -> computeDefault());

// orElseThrow
String value = opt.orElseThrow(() -> new IllegalStateException("Empty!"));

// map
Optional<Integer> length = opt.map(String::length);

// flatMap
Optional<String> upper = opt.flatMap(s -> Optional.of(s.toUpperCase()));

// filter
Optional<String> longString = opt.filter(s -> s.length() > 10);
```

---

## Currying

```java
// Função de 2 parâmetros
Function<Integer, Function<Integer, Integer>> add = a -> b -> a + b;

// Currying
Function<Integer, Integer> addFive = add.apply(5);
int result = addFive.apply(10);  // 15

// Ou direto
int result = add.apply(5).apply(10);  // 15
```

---

## Practical Examples

### Pipeline de Transformação

```java
List<Person> people = getPeople();

// Filtrar adultos, ordenar por nome, pegar top 5, extrair nomes
List<String> topAdults = people.stream()
    .filter(p -> p.getAge() >= 18)
    .sorted(Comparator.comparing(Person::getName))
    .limit(5)
    .map(Person::getName)
    .collect(Collectors.toList());
```

### Processamento Paralelo

```java
List<Integer> numbers = IntStream.rangeClosed(1, 1000000)
    .boxed()
    .collect(Collectors.toList());

// Stream paralelo
int sum = numbers.parallelStream()
    .mapToInt(Integer::intValue)
    .sum();
```

---

## Best Practices

### ✅ DO

```java
// Usar method references quando possível
names.forEach(System.out::println);  // ✅
names.forEach(n -> System.out.println(n));  // Menos conciso

// Preferir Streams para transformações
list.stream().filter(...).map(...).collect(...);

// Usar Optional para evitar null
public Optional<User> findUser(String id) {
    return Optional.ofNullable(database.get(id));
}
```

### ❌ DON'T

```java
// NÃO abusar de streams para loops simples
// ❌ Overkill:
IntStream.range(0, 10).forEach(i -> System.out.println(i));

// ✅ Melhor:
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// NÃO modificar estado externo em lambdas
// ❌ Evitar:
int[] counter = {0};
list.forEach(item -> counter[0]++);

// ✅ Melhor:
long count = list.size();
```

---

## References

- [Java 8 Functional Programming](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html) - Oracle tutorial
- [Stream API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/package-summary.html) - Javadoc
- [Modern Java in Action](https://www.manning.com/books/modern-java-in-action) - Livro definitivo
