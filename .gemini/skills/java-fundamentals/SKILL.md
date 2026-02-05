---
name: java-fundamentals
description: |
  Auxilia no desenvolvimento de código Java seguindo boas práticas de POO, 
  padrões de código limpo e recursos modernos da linguagem (Java 6-25).
  Use quando: criar classes Java, refatorar código, aplicar design patterns,
  trabalhar com collections, streams, exceções ou recursos da JVM.
license: MIT
metadata: ./metadata.yaml
---

# Java Fundamentals

Skill para desenvolvimento em Java seguindo fundamentos sólidos de programação orientada a objetos, clean code e recursos idiomáticos da linguagem.

---

## When to Use

Use esta skill quando precisar:

- **Criar classes e estruturas Java** com POO adequada (encapsulamento, herança, polimorfismo)
- **Refatorar código existente** para melhorar legibilidade e manutenibilidade
- **Aplicar design patterns** clássicos (GoF) em Java
- **Trabalhar com Collections** (List, Set, Map) e suas implementações
- **Usar Streams API** para processamento funcional de dados (Java 8+)
- **Tratar exceções** de forma robusta e idiomática
- **Aplicar recursos modernos** (records, sealed classes, switch expressions) quando disponíveis
- **Escrever código compatível** entre diferentes versões de Java (6-25)

**Não use para**: Frameworks específicos (Spring, Jakarta EE), build tools, deployment.

---

## Instructions

### Step 1: Analisar Contexto Java

Antes de gerar código, identifique:

1. **Versão do Java alvo**
   - Verifique `javac -version` ou arquivos de build (pom.xml, build.gradle)
   - Se versão não especificada: assumir Java 11 (LTS mais comum)

2. **Padrões de código existentes**
   - Convenções de nomenclatura (camelCase, PascalCase)
   - Estrutura de pacotes
   - Estilo de indentação (2 ou 4 espaços)

3. **Recursos disponíveis**
   - Java 6-7: Generics, enhanced for, autoboxing
   - Java 8+: Lambdas, Streams, Optional, default methods
   - Java 11+: var, HTTP Client, String methods
   - Java 17+: Records, sealed classes, switch expressions
   - Java 21+: Virtual threads, pattern matching
   - Java 25: Latest features (se disponível)

### Step 2: Aplicar Boas Práticas de POO

Ao criar/refatorar classes Java:

**Princípios SOLID:**
- **S**ingle Responsibility: Cada classe faz uma coisa bem
- **O**pen/Closed: Aberto para extensão, fechado para modificação
- **L**iskov Substitution: Subtipos substituíveis
- **I**nterface Segregation: Interfaces pequenas e coesas
- **D**ependency Inversion: Dependa de abstrações, não de implementações

**Encapsulamento:**
```java
// CORRETO: Campos privados, getters/setters quando necessário
public class Person {
    private final String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}

// EVITAR: Campos públicos expõem implementação
public class Person {
    public String name;
    public int age;
}
```

**Imutabilidade quando possível:**
```java
// Java 17+: Use records para DTOs
public record Point(int x, int y) {}

// Java 8-16: final fields + sem setters
public final class Point {
    private final int x;
    private final int y;
    
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    public int getX() { return x; }
    public int getY() { return y; }
}
```

### Step 3: Escrever Código Limpo

**Nomenclatura descritiva:**
```java
// CORRETO: Nomes revelam intenção
List<Customer> activeCustomers = getActiveCustomers();
boolean isEligibleForDiscount = age > 65 || isMember;

// EVITAR: Nomes genéricos ou abreviados
List<Customer> list = getList();
boolean flag = age > 65 || b;
```

**Métodos pequenos e focados:**
```java
// CORRETO: Método faz uma coisa
public boolean isAdult(int age) {
    return age >= 18;
}

// EVITAR: Método faz muitas coisas (> 20 linhas)
public void processUser(User user) {
    // validar
    // salvar no DB
    // enviar email
    // logar
    // atualizar cache
}
```

**DRY (Don't Repeat Yourself):**
```java
// CORRETO: Extrair lógica duplicada
private boolean isValidEmail(String email) {
    return email != null && email.contains("@");
}

public void registerUser(String email) {
    if (!isValidEmail(email)) throw new IllegalArgumentException();
    // ...
}

public void updateEmail(String email) {
    if (!isValidEmail(email)) throw new IllegalArgumentException();
    // ...
}
```

### Step 4: Usar Collections Idiomaticamente

**Escolher implementação adequada:**

```java
// List: Ordem importa, permite duplicatas
List<String> names = new ArrayList<>();  // Acesso rápido por índice
List<String> linkedNames = new LinkedList<>();  // Inserções/remoções frequentes

// Set: Sem duplicatas, ordem não garante (HashSet) ou garante (LinkedHashSet, TreeSet)
Set<String> uniqueEmails = new HashSet<>();  // Busca O(1)
Set<String> sortedNames = new TreeSet<>();   // Ordenação natural

// Map: Chave-valor
Map<String, Integer> ages = new HashMap<>();  // Busca O(1)
Map<String, Integer> sortedAges = new TreeMap<>();  // Chaves ordenadas
```

**Iterar corretamente:**
```java
// Java 8+: forEach com lambda
list.forEach(item -> System.out.println(item));

// Enhanced for (Java 5+)
for (String item : list) {
    System.out.println(item);
}

// Iterator (quando precisar remover durante iteração)
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String item = it.next();
    if (shouldRemove(item)) {
        it.remove();  // Seguro
    }
}
```

### Step 5: Aproveitar Streams API (Java 8+)

**Quando usar Streams:**
- Transformações de dados (map, filter, reduce)
- Processamento funcional (operações declarativas)
- Pipeline de operações legível

```java
// Filtrar e transformar
List<String> upperNames = names.stream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Agregações
int totalAge = people.stream()
    .mapToInt(Person::getAge)
    .sum();

// Buscar primeiro elemento
Optional<Person> firstAdult = people.stream()
    .filter(p -> p.getAge() >= 18)
    .findFirst();
```

**Quando evitar Streams:**
- Loops simples (for mais legível)
- Modificações de estado externo
- Performance crítica (overhead de streams)

### Step 6: Tratar Exceções Adequadamente

**Exceções Checked vs Unchecked:**
```java
// Checked: Cliente deve tratar (IOException, SQLException)
public String readFile(String path) throws IOException {
    return Files.readString(Paths.get(path));
}

// Unchecked: Erros de programação (NullPointerException, IllegalArgumentException)
public void setAge(int age) {
    if (age < 0) throw new IllegalArgumentException("Age cannot be negative");
    this.age = age;
}
```

**Try-with-resources (Java 7+):**
```java
// CORRETO: Auto-close de recursos
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    return reader.readLine();
}

// EVITAR: Fechar manualmente
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    return reader.readLine();
} finally {
    if (reader != null) reader.close();
}
```

**Optional para evitar null (Java 8+):**
```java
// CORRETO: Retornar Optional
public Optional<User> findUserById(String id) {
    User user = database.get(id);
    return Optional.ofNullable(user);
}

// Consumir Optional
findUserById("123")
    .ifPresent(user -> System.out.println(user.getName()));

String name = findUserById("123")
    .map(User::getName)
    .orElse("Unknown");
```

### Step 7: Usar Recursos Modernos Quando Disponível

**Java 17+: Records para DTOs:**
```java
// ANTES (Java 8-16): Boilerplate
public final class Point {
    private final int x, y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int x() { return x; }
    public int y() { return y; }
    @Override public boolean equals(Object o) { /* ... */ }
    @Override public int hashCode() { /* ... */ }
}

// DEPOIS (Java 17+): Conciso
public record Point(int x, int y) {}
```

**Java 17+: Sealed Classes para hierarquia controlada:**
```java
public sealed interface Shape permits Circle, Rectangle, Triangle {}

public final class Circle implements Shape { /* ... */ }
public final class Rectangle implements Shape { /* ... */ }
public final class Triangle implements Shape { /* ... */ }
```

**Java 21+: Pattern Matching for switch:**
```java
// Java 21+
String formatted = switch (obj) {
    case Integer i -> "int: " + i;
    case String s -> "string: " + s;
    case null -> "null";
    default -> "unknown";
};

// Java 8-20: instanceof + cast
String formatted;
if (obj == null) {
    formatted = "null";
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    formatted = "int: " + i;
} else if (obj instanceof String) {
    String s = (String) obj;
    formatted = "string: " + s;
} else {
    formatted = "unknown";
}
```

### Step 8: Validar e Entregar

**Checklist Final:**
- [ ] Código compila sem warnings (`javac -Xlint:all`)
- [ ] Nomes descritivos (classes, métodos, variáveis)
- [ ] Métodos < 20 linhas (regra geral)
- [ ] Sem código duplicado
- [ ] Exceções tratadas adequadamente
- [ ] Recursos fechados corretamente (try-with-resources)
- [ ] Imutabilidade aplicada onde possível
- [ ] Compatível com versão Java alvo

---

## Advanced Topics (JIT References)

Para tópicos avançados, consulte as referências detalhadas:

- **[Generics & Type Safety](./references/generics.md)** - Type parameters, wildcards, bounded types, type erasure
- **[Concurrency & Multithreading](./references/concurrency.md)** - Threads, ExecutorService, synchronization, concurrent collections
- **[Java I/O & NIO](./references/io-nio.md)** - File operations, streams, NIO.2, Path API
- **[Serialization & JSON](./references/serialization.md)** - Object serialization, JSON parsing (Jackson/Gson)
- **[Reflection & Annotations](./references/reflection.md)** - Class introspection, custom annotations, runtime processing
- **[Memory Management & GC](./references/memory.md)** - Heap/stack, garbage collectors, memory leaks, profiling
- **[Functional Programming](./references/functional.md)** - Advanced lambdas, method references, functional interfaces
- **[Design Patterns](./references/design-patterns.md)** - GoF patterns implementados em Java

Estas referências são carregadas just-in-time quando necessário.

---

## Quick Examples

### Streams API
```java
// Filtrar adultos, ordernar, pegar top 10
List<User> top10Adults = users.stream()
    .filter(user -> user.getAge() >= 18)
    .sorted(Comparator.comparing(User::getName))
    .limit(10)
    .collect(Collectors.toList());
```

### Java 17+ Records
```java
// ANTES: Boilerplate (50+ linhas)
public final class Product {
    private final String id, name;
    private final double price;
    // construtor, getters, equals, hashCode, toString...
}

// DEPOIS: Conciso
public record Product(String id, String name, double price) {
    public Product {  // Validação customizada
        if (price < 0) throw new IllegalArgumentException("Invalid price");
    }
}
```

Para exemplos detalhados de refatoração, consulte as **[referências JIT](#advanced-topics-jit-references)**.

---

## Compatibility

| CLI | Status | Notes |
|-----|--------|-------|
| Claude Code | ✅ | Fully supported |
| Gemini CLI | ✅ | Fully supported |
| OpenAI Codex | ✅ | Fully supported |
| GitHub Copilot | ✅ | Fully supported |
| OpenCode | ✅ | Fully supported |
| Cursor | ✅ | Fully supported |
| Qwen Code | ✅ | Fully supported |

**Requires:**
- Acesso ao filesystem para ler código existente
- Capacidade de executar `javac -version` (detecção de versão)

---

## References

- [Oracle Java Documentation](https://docs.oracle.com/en/java/) - Documentação oficial
- [Effective Java, 3rd Ed. - Joshua Bloch](https://www.oreilly.com/library/view/effective-java/9780134686097/) - Boas práticas
- [Java Language Specification](https://docs.oracle.com/javase/specs/) - Especificação da linguagem
- [Clean Code - Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Princípios de código limpo
- [Design Patterns - Gang of Four](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/) - Padrões de design

---

**Version**: 1.0.0  
**Created**: 2026-02-04  
**License**: MIT
