# Generics & Type Safety

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Generics, Type Parameters, Wildcards

---

## Overview

Generics permitem escrever código type-safe e reutilizável, detectando erros em compile-time ao invés de runtime.

**Disponível desde**: Java 5 (2004)

---

## Type Parameters Básicos

### Classe Genérica

```java
// Container genérico
public class Box<T> {
    private T content;
    
    public void set(T content) {
        this.content = content;
    }
    
    public T get() {
        return content;
    }
}

// Uso
Box<String> stringBox = new Box<>();
stringBox.set("Hello");
String value = stringBox.get();  // Sem cast necessário

Box<Integer> intBox = new Box<>();
intBox.set(42);
// intBox.set("String");  // ERRO de compilação ✅
```

### Método Genérico

```java
public class Utils {
    // Método genérico estático
    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }
}

// Uso
String[] names = {"Alice", "Bob"};
Integer[] numbers = {1, 2, 3};

Utils.printArray(names);     // T = String
Utils.printArray(numbers);   // T = Integer
```

---

## Bounded Type Parameters

### Upper Bound (extends)

```java
// Aceita apenas Number e subtipos
public class NumberBox<T extends Number> {
    private T number;
    
    public double doubleValue() {
        return number.doubleValue();  // Pode chamar métodos de Number
    }
}

// Uso
NumberBox<Integer> intBox = new NumberBox<>();    // OK
NumberBox<Double> doubleBox = new NumberBox<>();  // OK
// NumberBox<String> strBox = new NumberBox<>();  // ERRO ✅
```

### Multiple Bounds

```java
// T deve implementar AMBAS as interfaces
public class ComparableList<T extends Comparable<T> & Serializable> {
    private List<T> items = new ArrayList<>();
    
    public void add(T item) {
        items.add(item);
    }
    
    public T max() {
        return Collections.max(items);  // Usa Comparable
    }
}
```

---

## Wildcards

### Unbounded Wildcard (?)

```java
// Aceita List de qualquer tipo
public void printList(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}

// Uso
printList(Arrays.asList("A", "B"));      // List<String>
printList(Arrays.asList(1, 2, 3));       // List<Integer>
```

### Upper Bounded Wildcard (? extends T)

```java
// Aceita List de Number ou subtipos (LEITURA)
public double sum(List<? extends Number> numbers) {
    double total = 0;
    for (Number num : numbers) {
        total += num.doubleValue();
    }
    return total;
}

// Uso
List<Integer> ints = Arrays.asList(1, 2, 3);
List<Double> doubles = Arrays.asList(1.5, 2.5);

double sumInts = sum(ints);       // OK
double sumDoubles = sum(doubles); // OK

// IMPORTANTE: Não pode adicionar elementos
// numbers.add(42);  // ERRO de compilação ✅
```

### Lower Bounded Wildcard (? super T)

```java
// Aceita List de Integer ou supertipos (ESCRITA)
public void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
    list.add(3);
    // Integer value = list.get(0);  // ERRO: retorna Object
}

// Uso
List<Number> numbers = new ArrayList<>();
List<Object> objects = new ArrayList<>();

addIntegers(numbers);  // OK
addIntegers(objects);  // OK
```

### PECS Principle

**Producer Extends, Consumer Super**

```java
// Se você LÊ de uma estrutura: use <? extends T>
public void processProducers(List<? extends Number> producers) {
    for (Number num : producers) {  // Lendo ✅
        System.out.println(num);
    }
    // producers.add(42);  // Escrevendo ✗
}

// Se você ESCREVE em uma estrutura: use <? super T>
public void processConsumers(List<? super Integer> consumers) {
    consumers.add(42);  // Escrevendo ✅
    // Integer num = consumers.get(0);  // Lendo (como Integer) ✗
}
```

---

## Type Erasure

**IMPORTANTE**: Generics são removidos em runtime (type erasure).

```java
// Em compile-time
List<String> strings = new ArrayList<>();
List<Integer> numbers = new ArrayList<>();

// Em runtime (após type erasure)
List strings = new ArrayList();  // Raw type
List numbers = new ArrayList();  // Raw type

// Consequências:
strings.getClass() == numbers.getClass();  // true! ⚠️

// NÃO FUNCIONA: instanceof com type parameter
// if (obj instanceof List<String>) {}  // ERRO de compilação

// FUNCIONA: instanceof com raw type
if (obj instanceof List) {  // OK, mas perde type safety
    List<?> list = (List<?>) obj;
}
```

### Limitações do Type Erasure

```java
public class GenericArray<T> {
    // ERRO: Não pode criar array de type parameter
    // private T[] array = new T[10];
    
    // WORKAROUND: Usar Object[] com cast
    private Object[] array = new Object[10];
    
    @SuppressWarnings("unchecked")
    public T get(int index) {
        return (T) array[index];
    }
    
    public void set(int index, T value) {
        array[index] = value;
    }
}

// MELHOR: Usar ArrayList
public class GenericList<T> {
    private List<T> list = new ArrayList<>();  // ✅ Funciona perfeitamente
}
```

---

## Generics em Interfaces

```java
// Interface genérica
public interface Repository<T, ID> {
    T findById(ID id);
    List<T> findAll();
    void save(T entity);
    void delete(ID id);
}

// Implementação concreta
public class UserRepository implements Repository<User, Long> {
    @Override
    public User findById(Long id) {
        // implementação
        return null;
    }
    
    @Override
    public List<User> findAll() {
        return new ArrayList<>();
    }
    
    @Override
    public void save(User entity) {
        // implementação
    }
    
    @Override
    public void delete(Long id) {
        // implementação
    }
}
```

---

## Best Practices

### ✅ DO

```java
// Use generics para type safety
List<String> names = new ArrayList<>();

// Use bounded types quando necessário
public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// Use PECS principle
public void copy(List<? extends T> source, List<? super T> dest) {
    for (T item : source) {
        dest.add(item);
    }
}
```

### ❌ DON'T

```java
// NÃO use raw types (perde type safety)
List names = new ArrayList();  // ❌ Evitar

// NÃO ignore warnings sem razão
@SuppressWarnings("unchecked")  // ❌ Só use quando inevitável
List<String> list = (List<String>) obj;

// NÃO use instanceof com type parameter
if (obj instanceof List<String>) {}  // ❌ ERRO de compilação
```

---

## References

- [Java Generics Tutorial](https://docs.oracle.com/javase/tutorial/java/generics/) - Oracle oficial
- [Effective Java, Item 26-33](https://www.oreilly.com/library/view/effective-java/9780134686097/) - Joshua Bloch sobre Generics
- [Java Generics FAQ](http://www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html) - FAQ completo
