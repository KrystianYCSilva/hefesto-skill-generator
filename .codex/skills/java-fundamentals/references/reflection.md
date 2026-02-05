# Reflection & Annotations

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Class Introspection, Custom Annotations, Runtime Processing

---

## Overview

Reflection permite inspecionar e modificar estrutura/comportamento de classes em runtime.

**Disponível desde**: Java 1.1  
**Uso comum**: Frameworks (Spring, Hibernate), testes, serialização

---

## Class Introspection

### Obtaining Class Objects

```java
// Método 1: .class literal
Class<String> clazz1 = String.class;

// Método 2: .getClass()
String str = "Hello";
Class<?> clazz2 = str.getClass();

// Método 3: Class.forName() (FQCN)
Class<?> clazz3 = Class.forName("java.lang.String");
```

### Class Information

```java
Class<?> clazz = Person.class;

// Nome
String simpleName = clazz.getSimpleName();     // "Person"
String canonicalName = clazz.getCanonicalName();  // "com.example.Person"
String name = clazz.getName();                 // "com.example.Person"

// Package
Package pkg = clazz.getPackage();

// Modifiers
int modifiers = clazz.getModifiers();
boolean isPublic = Modifier.isPublic(modifiers);
boolean isFinal = Modifier.isFinal(modifiers);
boolean isAbstract = Modifier.isAbstract(modifiers);

// Hierarquia
Class<?> superclass = clazz.getSuperclass();
Class<?>[] interfaces = clazz.getInterfaces();
```

---

## Fields (Campos)

### Listing Fields

```java
Class<?> clazz = Person.class;

// Campos públicos (incluindo herdados)
Field[] publicFields = clazz.getFields();

// Todos os campos (apenas desta classe)
Field[] allFields = clazz.getDeclaredFields();

// Campo específico
Field nameField = clazz.getDeclaredField("name");
```

### Reading/Writing Fields

```java
public class Person {
    private String name = "Alice";
    private int age = 30;
}

Person person = new Person();
Field nameField = Person.class.getDeclaredField("name");

// Tornar acessível (bypass private)
nameField.setAccessible(true);

// Ler valor
String name = (String) nameField.get(person);  // "Alice"

// Escrever valor
nameField.set(person, "Bob");
System.out.println(person.getName());  // "Bob"
```

---

## Methods (Métodos)

### Listing Methods

```java
Class<?> clazz = Person.class;

// Métodos públicos (incluindo herdados)
Method[] publicMethods = clazz.getMethods();

// Todos os métodos (apenas desta classe)
Method[] allMethods = clazz.getDeclaredMethods();

// Método específico
Method setNameMethod = clazz.getDeclaredMethod("setName", String.class);
```

### Invoking Methods

```java
Person person = new Person();
Method setNameMethod = Person.class.getMethod("setName", String.class);

// Invocar método
setNameMethod.invoke(person, "Charlie");  // person.setName("Charlie")

// Método com retorno
Method getNameMethod = Person.class.getMethod("getName");
String name = (String) getNameMethod.invoke(person);  // person.getName()

// Método estático
Method staticMethod = Math.class.getMethod("max", int.class, int.class);
int result = (int) staticMethod.invoke(null, 10, 20);  // Math.max(10, 20)
```

---

## Constructors

### Listing Constructors

```java
Class<?> clazz = Person.class;

// Todos os construtores
Constructor<?>[] constructors = clazz.getConstructors();

// Construtor específico
Constructor<?> constructor = clazz.getConstructor(String.class, int.class);
```

### Creating Instances

```java
// Método 1: newInstance() (deprecated Java 9+)
Person person = Person.class.newInstance();  // ❌ Deprecated

// Método 2: Constructor.newInstance() (RECOMENDADO)
Constructor<Person> constructor = Person.class.getConstructor(String.class, int.class);
Person person = constructor.newInstance("Alice", 30);
```

---

## Annotations

### Built-in Annotations

```java
@Override  // Indica override de método
public String toString() {
    return "...";
}

@Deprecated  // Marca como deprecated
public void oldMethod() {
    // ...
}

@SuppressWarnings("unchecked")  // Suprime warnings
public void method() {
    List list = new ArrayList();
}

@FunctionalInterface  // Marca interface funcional
public interface Calculator {
    int calculate(int a, int b);
}
```

### Custom Annotations

```java
// Definir annotation
@Retention(RetentionPolicy.RUNTIME)  // Disponível em runtime
@Target(ElementType.METHOD)          // Aplicável apenas a métodos
public @interface TestMethod {
    String description() default "";
    int priority() default 0;
}

// Usar annotation
public class Calculator {
    @TestMethod(description = "Test addition", priority = 1)
    public void testAdd() {
        // ...
    }
    
    @TestMethod(description = "Test subtraction", priority = 2)
    public void testSubtract() {
        // ...
    }
}
```

### Reading Annotations

```java
Class<?> clazz = Calculator.class;

// Annotations da classe
Annotation[] classAnnotations = clazz.getAnnotations();

// Annotations de métodos
for (Method method : clazz.getDeclaredMethods()) {
    if (method.isAnnotationPresent(TestMethod.class)) {
        TestMethod annotation = method.getAnnotation(TestMethod.class);
        System.out.println("Method: " + method.getName());
        System.out.println("Description: " + annotation.description());
        System.out.println("Priority: " + annotation.priority());
    }
}
```

### Retention Policies

```java
// SOURCE: Descartado após compilação (ex: @Override)
@Retention(RetentionPolicy.SOURCE)

// CLASS: Mantido em .class mas não em runtime (padrão)
@Retention(RetentionPolicy.CLASS)

// RUNTIME: Disponível em runtime via reflection
@Retention(RetentionPolicy.RUNTIME)
```

### Target Types

```java
@Target(ElementType.TYPE)          // Classes, interfaces, enums
@Target(ElementType.FIELD)         // Campos
@Target(ElementType.METHOD)        // Métodos
@Target(ElementType.PARAMETER)     // Parâmetros de métodos
@Target(ElementType.CONSTRUCTOR)   // Construtores
@Target(ElementType.LOCAL_VARIABLE)  // Variáveis locais
@Target(ElementType.ANNOTATION_TYPE) // Annotations
@Target(ElementType.PACKAGE)       // Packages

// Múltiplos targets
@Target({ElementType.METHOD, ElementType.FIELD})
```

---

## Practical Examples

### Simple Test Framework

```java
// Annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Test {}

// Test runner
public class TestRunner {
    public static void run(Class<?> testClass) throws Exception {
        Object instance = testClass.getDeclaredConstructor().newInstance();
        
        for (Method method : testClass.getDeclaredMethods()) {
            if (method.isAnnotationPresent(Test.class)) {
                try {
                    method.invoke(instance);
                    System.out.println("✓ " + method.getName() + " passed");
                } catch (Exception e) {
                    System.out.println("✗ " + method.getName() + " failed: " + e.getCause());
                }
            }
        }
    }
}

// Uso
public class MathTest {
    @Test
    public void testAddition() {
        assert 2 + 2 == 4;
    }
    
    @Test
    public void testSubtraction() {
        assert 5 - 3 == 2;
    }
}

TestRunner.run(MathTest.class);
```

### Dependency Injection (Simples)

```java
// Annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface Inject {}

// Container
public class InjectorContainer {
    private Map<Class<?>, Object> registry = new HashMap<>();
    
    public <T> void register(Class<T> clazz, T instance) {
        registry.put(clazz, instance);
    }
    
    public void inject(Object target) throws Exception {
        for (Field field : target.getClass().getDeclaredFields()) {
            if (field.isAnnotationPresent(Inject.class)) {
                Class<?> type = field.getType();
                Object dependency = registry.get(type);
                
                if (dependency != null) {
                    field.setAccessible(true);
                    field.set(target, dependency);
                }
            }
        }
    }
}

// Uso
public class UserService {
    @Inject
    private Database database;
    
    public void save(User user) {
        database.save(user);  // Injetado automaticamente
    }
}

InjectorContainer container = new InjectorContainer();
container.register(Database.class, new MySQLDatabase());

UserService service = new UserService();
container.inject(service);  // Injeta database
```

---

## Best Practices

### ✅ DO

```java
// Cachear Class objects
private static final Class<Person> PERSON_CLASS = Person.class;

// Tratar exceções adequadamente
try {
    Method method = clazz.getMethod("getName");
    String name = (String) method.invoke(obj);
} catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
    // Tratar erro
}

// Usar annotations para metadados
@Entity
@Table(name = "users")
public class User { }
```

### ❌ DON'T

```java
// NÃO usar reflection quando não necessário (performance)
// ❌ Lento:
Method method = obj.getClass().getMethod("getName");
String name = (String) method.invoke(obj);

// ✅ Rápido:
String name = obj.getName();

// NÃO abusar de setAccessible()
field.setAccessible(true);  // ⚠️ Quebra encapsulamento
```

---

## Performance Considerations

Reflection é **10-50x mais lento** que acesso direto:

```java
// Benchmark (1 milhão de iterações)
// Acesso direto: 1ms
person.getName();

// Reflection: 50ms
Method method = person.getClass().getMethod("getName");
method.invoke(person);
```

**Quando usar Reflection**:
- Frameworks (DI, ORM, serialization)
- Testes (mocking, inspection)
- APIs genéricas

**Quando NÃO usar**:
- Hot paths (código executado frequentemente)
- Quando existe alternativa direta

---

## References

- [Java Reflection Tutorial](https://docs.oracle.com/javase/tutorial/reflect/) - Oracle oficial
- [Reflection API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/reflect/package-summary.html) - Javadoc
- [Effective Java, Item 65](https://www.oreilly.com/library/view/effective-java/9780134686097/) - Prefer interfaces to reflection
