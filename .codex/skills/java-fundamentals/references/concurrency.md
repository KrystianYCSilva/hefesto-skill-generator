# Concurrency & Multithreading

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Threads, Synchronization, Concurrent Collections

---

## Overview

Programação concorrente permite executar múltiplas tarefas simultaneamente, aproveitando CPUs multi-core.

**Disponível desde**: Java 1.0 (threads básicas), Java 5 (java.util.concurrent)

---

## Criando Threads

### Método 1: Extends Thread

```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + getName());
    }
}

// Uso
MyThread thread = new MyThread();
thread.start();  // NÃO chamar run() diretamente!
```

### Método 2: Implements Runnable (RECOMENDADO)

```java
public class MyTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Task running");
    }
}

// Uso
Thread thread = new Thread(new MyTask());
thread.start();

// Ou com lambda (Java 8+)
Thread thread2 = new Thread(() -> {
    System.out.println("Lambda task");
});
thread2.start();
```

### Método 3: ExecutorService (MELHOR PRÁTICA)

```java
// Thread pool com 4 threads
ExecutorService executor = Executors.newFixedThreadPool(4);

// Submeter tarefas
executor.submit(() -> {
    System.out.println("Task 1");
});

executor.submit(() -> {
    System.out.println("Task 2");
});

// Shutdown quando terminar
executor.shutdown();

// Aguardar conclusão (opcional)
try {
    executor.awaitTermination(1, TimeUnit.MINUTES);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

---

## Synchronization

### Problema: Race Condition

```java
public class Counter {
    private int count = 0;
    
    // UNSAFE: Race condition
    public void increment() {
        count++;  // Não é atômico! (read-modify-write)
    }
    
    public int getCount() {
        return count;
    }
}
```

### Solução 1: synchronized Method

```java
public class SafeCounter {
    private int count = 0;
    
    // SAFE: synchronized
    public synchronized void increment() {
        count++;
    }
    
    public synchronized int getCount() {
        return count;
    }
}
```

### Solução 2: synchronized Block

```java
public class SafeCounter {
    private int count = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized (lock) {  // Bloco sincronizado
            count++;
        }
    }
    
    public int getCount() {
        synchronized (lock) {
            return count;
        }
    }
}
```

### Solução 3: AtomicInteger (MELHOR)

```java
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicCounter {
    private AtomicInteger count = new AtomicInteger(0);
    
    // SAFE e mais performático
    public void increment() {
        count.incrementAndGet();
    }
    
    public int getCount() {
        return count.get();
    }
}
```

---

## volatile Keyword

```java
public class StoppableTask implements Runnable {
    // volatile garante visibilidade entre threads
    private volatile boolean running = true;
    
    @Override
    public void run() {
        while (running) {
            // Fazer trabalho
        }
    }
    
    public void stop() {
        running = false;  // Visível para a thread do run()
    }
}
```

---

## Concurrent Collections

### ConcurrentHashMap

```java
// Thread-safe sem synchronized
Map<String, Integer> map = new ConcurrentHashMap<>();

// Múltiplas threads podem acessar simultaneamente
map.put("key1", 1);
map.put("key2", 2);

// Operações atômicas
map.putIfAbsent("key3", 3);
map.computeIfAbsent("key4", k -> 4);
map.merge("key1", 10, Integer::sum);  // Soma valores
```

### CopyOnWriteArrayList

```java
// Ideal para muitas leituras, poucas escritas
List<String> list = new CopyOnWriteArrayList<>();

list.add("item1");
list.add("item2");

// Iterator nunca lança ConcurrentModificationException
for (String item : list) {
    System.out.println(item);
    // Outra thread pode modificar durante iteração ✅
}
```

### BlockingQueue

```java
// Fila thread-safe com bloqueio
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);

// Producer thread
Thread producer = new Thread(() -> {
    try {
        queue.put("item1");  // Bloqueia se fila cheia
        queue.put("item2");
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
});

// Consumer thread
Thread consumer = new Thread(() -> {
    try {
        String item = queue.take();  // Bloqueia se fila vazia
        System.out.println("Consumed: " + item);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
});

producer.start();
consumer.start();
```

---

## ExecutorService Patterns

### Fixed Thread Pool

```java
// Pool fixo de N threads
ExecutorService executor = Executors.newFixedThreadPool(4);
// Ideal para: Número previsível de tarefas
```

### Cached Thread Pool

```java
// Cria threads sob demanda, reusa threads ociosas
ExecutorService executor = Executors.newCachedThreadPool();
// Ideal para: Muitas tarefas de curta duração
```

### Single Thread Executor

```java
// Garante execução sequencial (FIFO)
ExecutorService executor = Executors.newSingleThreadExecutor();
// Ideal para: Tarefas que devem executar em ordem
```

### Scheduled Thread Pool

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

// Executar uma vez com delay
scheduler.schedule(() -> {
    System.out.println("Executed after 5s");
}, 5, TimeUnit.SECONDS);

// Executar periodicamente (fixed rate)
scheduler.scheduleAtFixedRate(() -> {
    System.out.println("Every 10s");
}, 0, 10, TimeUnit.SECONDS);
```

---

## Future & Callable

```java
// Callable retorna valor (diferente de Runnable)
Callable<Integer> task = () -> {
    Thread.sleep(1000);
    return 42;
};

ExecutorService executor = Executors.newSingleThreadExecutor();

// Future representa resultado futuro
Future<Integer> future = executor.submit(task);

// Fazer outras coisas...

// Bloquear até resultado estar pronto
try {
    Integer result = future.get();  // Bloqueia
    System.out.println("Result: " + result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}

executor.shutdown();
```

---

## CompletableFuture (Java 8+)

```java
// Execução assíncrona
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    try { Thread.sleep(1000); } catch (InterruptedException e) {}
    return "Result";
});

// Encadear operações
future.thenApply(result -> result.toUpperCase())
      .thenAccept(upper -> System.out.println("Upper: " + upper));

// Combinar múltiplos futures
CompletableFuture<Integer> future1 = CompletableFuture.supplyAsync(() -> 10);
CompletableFuture<Integer> future2 = CompletableFuture.supplyAsync(() -> 20);

CompletableFuture<Integer> combined = future1.thenCombine(future2, (a, b) -> a + b);
System.out.println("Sum: " + combined.get());  // 30
```

---

## Best Practices

### ✅ DO

```java
// Usar ExecutorService ao invés de Thread diretamente
ExecutorService executor = Executors.newFixedThreadPool(10);

// Sempre fazer shutdown de ExecutorService
executor.shutdown();

// Usar concurrent collections
Map<String, Integer> map = new ConcurrentHashMap<>();

// Tratar InterruptedException adequadamente
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new RuntimeException(e);
}
```

### ❌ DON'T

```java
// NÃO ignorar InterruptedException
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    // VAZIO - ❌ NUNCA fazer isso
}

// NÃO chamar run() ao invés de start()
thread.run();  // ❌ Executa na thread atual

// NÃO esquecer de fazer shutdown
// ❌ FALTA: executor.shutdown();
```

---

## References

- [Java Concurrency Tutorial](https://docs.oracle.com/javase/tutorial/essential/concurrency/) - Oracle oficial
- [Java Concurrency in Practice - Brian Goetz](https://www.oreilly.com/library/view/java-concurrency-in/0321349601/) - Livro definitivo
