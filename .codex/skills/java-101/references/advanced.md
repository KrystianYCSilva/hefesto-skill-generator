# Advanced Java Patterns & Techniques

## Gang of Four (GoF) Design Patterns

Complete list of standard design patterns. *See [Refactoring.guru](https://refactoring.guru/design-patterns/java) for implementation details.*

### Creational
*Concerned with the way objects are created.*
- **Abstract Factory**: Families of related objects.
- **Builder**: Constructing complex objects step-by-step.
- **Factory Method**: Defer instantiation to subclasses.
- **Prototype**: Cloning objects.
- **Singleton**: Restrict class to one instance (Prefer Enum).

### Structural
*Concerned with class and object composition.*
- **Adapter**: Compatible interfaces.
- **Bridge**: Split abstraction from implementation.
- **Composite**: Tree structures of objects.
- **Decorator**: Add dynamic responsibilities.
- **Facade**: Simplified interface to complex system.
- **Flyweight**: Efficient sharing of fine-grained objects.
- **Proxy**: Surrogate/placeholder for another object.

### Behavioral
*Concerned with communication between objects.*
- **Chain of Responsibility**: Pass request along a chain.
- **Command**: Encapsulate request as object.
- **Interpreter**: Grammar representation.
- **Iterator**: Sequential access.
- **Mediator**: Simplified communication.
- **Memento**: Capture/restore state.
- **Observer**: Publish/Subscribe.
- **State**: Alter behavior when state changes.
- **Strategy**: Interchangeable algorithms.
- **Template Method**: Skeleton of an algorithm.
- **Visitor**: Separate operations from object structure.

## Concurrency Models

### Modern Concurrency
- **CompletableFuture**: Composable asynchronous programming.
- **Virtual Threads (Java 21+)**: Write blocking code that scales like non-blocking code.
- **Structured Concurrency**: Treat related tasks as a single unit of work (Incubator).

## Performance Tuning
- **Garbage Collection (GC)**:
  - **G1GC**: Default, balanced throughput/latency.
  - **ZGC**: Low latency (<10ms pauses) for large heaps.
- **JIT Compiler**: C1 (Client) vs C2 (Server) compilation tiers.
- **Profiling**: Using Java Flight Recorder (JFR) and Java Mission Control (JMC).
