# Memory Management & Garbage Collection

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Heap, Stack, GC, Memory Leaks, Profiling

---

## Overview

A JVM gerencia memória automaticamente via Garbage Collection, mas entender o modelo de memória é essencial para performance e debugging.

---

## Heap vs Stack

**Stack**: 
- Armazena variáveis locais e frames de métodos
- LIFO (Last In, First Out)
- Memória gerenciada automaticamente (scope)
- Rápida, tamanho limitado

**Heap**:
- Armazena objetos e arrays
- Compartilhado entre threads
- Gerenciado por Garbage Collector
- Maior capacidade

### Exemplo Prático

```java
public void example() {
    int x = 10;              // Stack: variável primitiva
    String name = "Java";    // Stack: referência
                             // Heap: String object "Java"
    
    Person p = new Person(); // Stack: referência 'p'
                             // Heap: objeto Person
    
    p.setAge(25);            // Stack: int 25 (parâmetro)
                             // Heap: field age no objeto Person
}

// Quando method retorna:
// - Stack frame removido automaticamente
// - Objetos no heap ficam órfãos (elegíveis para GC)
```

---

## Garbage Collection

### Gerações de Objetos

**Young Generation**:
- Objetos novos alocados em **Eden**
- **Minor GC** (rápido): limpa Eden frequentemente
- Sobreviventes vão para **Survivor spaces**

**Old Generation**:
- Objetos que sobreviveram a muitos Minor GCs
- **Major GC** (Full GC): mais lento, pausa mais longa

**Metaspace** (Java 8+):
- Metadata de classes
- Substitui PermGen (Java 7)

### Tipos de Garbage Collectors

```bash
# Serial GC (single-threaded)
java -XX:+UseSerialGC -jar app.jar

# Parallel GC (multi-threaded)
java -XX:+UseParallelGC -jar app.jar

# G1 GC (Garbage First) - DEFAULT Java 9+
java -XX:+UseG1GC -jar app.jar

# ZGC (low-latency)
java -XX:+UseZGC -jar app.jar
```

---

## Memory Leaks em Java

**SIM**, Java pode ter memory leaks! GC só libera objetos *unreachable*.

### Leak 1: Static Collections

```java
public class LeakExample {
    // ❌ LEAK: static collection cresce infinitamente
    private static List<Object> cache = new ArrayList<>();
    
    public void addToCache(Object obj) {
        cache.add(obj);  // Nunca removido!
    }
}

// SOLUÇÃO: Usar WeakHashMap
private static Map<Object, Object> cache = new WeakHashMap<>();
```

### Leak 2: Listeners Não Removidos

```java
public class UIComponent {
    private List<EventListener> listeners = new ArrayList<>();
    
    public void addListener(EventListener listener) {
        listeners.add(listener);
    }
    
    // ❌ FALTA: método para remover listener
}

// SOLUÇÃO: Adicionar método de remoção
public void removeListener(EventListener listener) {
    listeners.remove(listener);
}
```

### Leak 3: ThreadLocal Não Limpo

```java
public class UserContext {
    private static ThreadLocal<User> currentUser = new ThreadLocal<>();
    
    public static void setUser(User user) {
        currentUser.set(user);
    }
    
    public static User getUser() {
        return currentUser.get();
    }
}

// SOLUÇÃO: Sempre limpar ThreadLocal
public static void clearUser() {
    currentUser.remove();
}

// Uso correto:
try {
    UserContext.setUser(user);
    // processar requisição
} finally {
    UserContext.clearUser();  // ✅ Sempre limpar
}
```

### Leak 4: Connections Não Fechadas

```java
// ❌ LEAK: Connection não fechada
public void query() throws SQLException {
    Connection conn = DriverManager.getConnection(url);
    Statement stmt = conn.createStatement();
    // FALTA: fechar recursos
}

// SOLUÇÃO: Try-with-resources
public void queryFixed() throws SQLException {
    try (Connection conn = DriverManager.getConnection(url);
         Statement stmt = conn.createStatement();
         ResultSet rs = stmt.executeQuery("SELECT * FROM users")) {
        
        while (rs.next()) {
            // processar
        }
    }  // ✅ Auto-close
}
```

---

## Profiling & Monitoring

### JVM Flags Úteis

```bash
# Ver GC logs
java -Xlog:gc* -jar app.jar

# Heap dump em OutOfMemoryError
java -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/tmp/heapdump.hprof \
     -jar app.jar

# Configurar heap size
java -Xms512m \      # Initial heap
     -Xmx2g \        # Max heap
     -jar app.jar
```

### Ferramentas de Profiling

**1. jconsole** (JDK built-in)
```bash
jconsole <pid>
```

**2. VisualVM** 
```bash
visualvm
```

**3. jstat** (estatísticas GC)
```bash
jstat -gc <pid> 1000
```

**4. jmap** (heap dump)
```bash
jmap -dump:format=b,file=heap.bin <pid>
```

---

## Best Practices

### ✅ DO

```java
// Usar try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // usar fis
}

// Limpar collections grandes
largeList.clear();
largeList = null;

// Usar StringBuilder para concatenação
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
```

### ❌ DON'T

```java
// NÃO concatenar Strings em loops
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;  // ❌ Cria 1000 objetos String
}

// NÃO manter referências desnecessárias
public class Cache {
    private static Map<String, byte[]> data = new HashMap<>();
    
    public void cache(String key, byte[] largeData) {
        data.put(key, largeData);  // ❌ Nunca limpo
    }
}
```

---

## Troubleshooting Memory Issues

### OutOfMemoryError: Java heap space

```bash
# 1. Aumentar heap
java -Xmx4g -jar app.jar

# 2. Gerar heap dump
java -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/tmp/dump.hprof \
     -jar app.jar

# 3. Analisar com Eclipse MAT
```

### OutOfMemoryError: Metaspace

```bash
# Aumentar metaspace (Java 8+)
java -XX:MaxMetaspaceSize=512m -jar app.jar
```

### StackOverflowError

```java
// CAUSA: Recursão infinita
public void recursive() {
    recursive();  // ❌ Sem condição de parada
}

// SOLUÇÃO: Adicionar base case
public void recursiveFixed(int n) {
    if (n == 0) return;  // ✅ Base case
    recursiveFixed(n - 1);
}
```

---

## References

- [Java Memory Management](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/) - Oracle GC Tuning
- [Eclipse Memory Analyzer](https://www.eclipse.org/mat/) - Heap dump analysis
- [Java Performance: The Definitive Guide](https://www.oreilly.com/library/view/java-performance-the/9781449363512/) - Scott Oaks
