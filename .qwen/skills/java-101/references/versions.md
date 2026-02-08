# Java Version History

Evolution of Java. Legacy systems often run on modern JVMs (e.g., code written in Java 6 running on Java 17).

## Legacy Era (Java 5 - 7)
*Found in many enterprise legacy systems.*

### Java 5 (Tiger)
- **Generics**: Type safety (`List<String>`).
- **Annotations**: Metadata (`@Override`).
- **Enums**: Type-safe enumerations.
- **Varargs**: Variable arguments (`String... args`).
- **Enhanced For-Loop**: `for (String s : list)`.
- **Autoboxing/Unboxing**: Automatic conversion between primitives and wrappers.

### Java 6 (Mustang)
- **Scripting Support**: JSR 223 (Rhino).
- **Pluggable Annotations**: Compiler API.
- **Performance**: Major speed improvements in JVM.

### Java 7 (Dolphin)
- **Try-with-resources**: Auto-closing streams/connections.
- **Diamond Operator**: `new ArrayList<>()`.
- **Switch on String**: `switch(stringVal)`.
- **NIO.2**: Better file I/O (`Path`, `Files`).
- **Multi-catch**: `catch (IOException | SQLException e)`.

## Modern Era (LTS Versions)

### Java 8 (LTS) - The Turning Point
- **Lambdas & Functional Interfaces**: Concise code.
- **Streams API**: Functional-style operations.
- **Optional**: Null-safety container.
- **Date/Time API (java.time)**: Replaced `Date`/`Calendar`.

### Java 11 (LTS)
- **HTTP Client (Standard)**: Non-blocking HTTP.
- **String Methods**: `isBlank()`, `lines()`, `strip()`.
- **Launch Single-File Source Code**: `java Script.java`.

### Java 17 (LTS)
- **Sealed Classes**: Control inheritance hierarchy.
- **Records**: Concise data carriers.
- **Pattern Matching for `instanceof`**.
- **Text Blocks**: Multiline strings (`"""`).

### Java 21 (LTS)
- **Virtual Threads**: High-concurrency lightweight threads.
- **Sequenced Collections**: `getFirst()`, `getLast()`.
- **Pattern Matching for Switch**.

## Intermediate Releases (Features often standardized in next LTS)
- **Java 9/10**: Modules (Jigsaw), `var`.
- **Java 12-16**: Switch Expressions, Records preview.
- **Java 18-20**: UTF-8 by default, Foreign Function & Memory API previews.
