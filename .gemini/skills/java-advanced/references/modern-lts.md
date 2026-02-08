# Modern LTS Features (Java 17 & 21)

## Java 17 (LTS)
- **Sealed Classes**:
  ```java
  sealed interface Shape permits Circle, Square {}
  final class Circle implements Shape {}
  ```
  Enables exhaustive compile-time checking in switch expressions.

- **Foreign Function & Memory API (Incubator)**: Safer, faster alternative to JNI.

## Java 21 (LTS)
- **Virtual Threads**:
  ```java
  try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
      IntStream.range(0, 10_000).forEach(i ->
          executor.submit(() -> {
              Thread.sleep(Duration.ofSeconds(1));
              return i;
          }));
  }
  ```

- **Sequenced Collections**: `getFirst()`, `removeLast()` unified across List, Deque, SortedSet.
- **Record Patterns**:
  ```java
  if (obj instanceof Point(int x, int y)) {
      System.out.println(x + y);
  }
  ```
