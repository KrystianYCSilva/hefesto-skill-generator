# Design Patterns em Java

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Gang of Four Patterns, Java-specific implementations

---

## Overview

Design Patterns são soluções reutilizáveis para problemas comuns em design de software.

**Fonte**: "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four, 1994)

---

## Creational Patterns

### Singleton

**Problema**: Garantir única instância de uma classe.

```java
// ✅ SOLUÇÃO 1: Enum Singleton (RECOMENDADO)
public enum Singleton {
    INSTANCE;
    
    public void doSomething() {
        // implementação
    }
}

// Uso
Singleton.INSTANCE.doSomething();

// ✅ SOLUÇÃO 2: Holder Class Pattern
public class Singleton {
    private Singleton() {}
    
    private static class Holder {
        private static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;  // Thread-safe, lazy
    }
}
```

### Factory Method

```java
// Interface de produto
public interface Payment {
    void processPayment(double amount);
}

// Produtos concretos
public class CreditCardPayment implements Payment {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing credit card: $" + amount);
    }
}

public class PayPalPayment implements Payment {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing PayPal: $" + amount);
    }
}

// Factory abstrata
public abstract class PaymentFactory {
    public abstract Payment createPayment();
    
    public void pay(double amount) {
        Payment payment = createPayment();
        payment.processPayment(amount);
    }
}

// Factories concretas
public class CreditCardFactory extends PaymentFactory {
    @Override
    public Payment createPayment() {
        return new CreditCardPayment();
    }
}
```

### Builder

```java
public class Person {
    private final String name;
    private final int age;
    private final String address;
    private final String phone;
    
    private Person(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.address = builder.address;
        this.phone = builder.phone;
    }
    
    public static class Builder {
        private final String name;
        private int age = 0;
        private String address = "";
        private String phone = "";
        
        public Builder(String name) {
            this.name = name;
        }
        
        public Builder age(int age) {
            this.age = age;
            return this;
        }
        
        public Builder address(String address) {
            this.address = address;
            return this;
        }
        
        public Builder phone(String phone) {
            this.phone = phone;
            return this;
        }
        
        public Person build() {
            if (age < 0) throw new IllegalArgumentException("Age cannot be negative");
            return new Person(this);
        }
    }
}

// Uso
Person person = new Person.Builder("Alice")
    .age(30)
    .address("123 Main St")
    .phone("555-1234")
    .build();
```

---

## Structural Patterns

### Adapter

**Problema**: Converter interface incompatível.

```java
// Interface alvo
public interface MediaPlayer {
    void play(String filename);
}

// Classe incompatível (legado)
public class LegacyAudioPlayer {
    public void playAudio(String filename) {
        System.out.println("Playing audio: " + filename);
    }
}

// Adapter
public class AudioPlayerAdapter implements MediaPlayer {
    private final LegacyAudioPlayer legacyPlayer;
    
    public AudioPlayerAdapter(LegacyAudioPlayer legacyPlayer) {
        this.legacyPlayer = legacyPlayer;
    }
    
    @Override
    public void play(String filename) {
        legacyPlayer.playAudio(filename);
    }
}
```

### Decorator

**Problema**: Adicionar comportamento dinamicamente.

```java
// Component
public interface Coffee {
    String getDescription();
    double getCost();
}

// Concrete component
public class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "Simple coffee";
    }
    
    @Override
    public double getCost() {
        return 2.0;
    }
}

// Decorator base
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
}

// Concrete decorator
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", milk";
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 0.5;
    }
}

// Uso
Coffee coffee = new SimpleCoffee();
coffee = new MilkDecorator(coffee);
System.out.println(coffee.getDescription());  // "Simple coffee, milk"
System.out.println("Cost: $" + coffee.getCost());  // "Cost: $2.5"
```

---

## Behavioral Patterns

### Strategy

**Problema**: Encapsular algoritmos intercambiáveis.

```java
// Strategy interface
public interface PaymentStrategy {
    void pay(double amount);
}

// Concrete strategies
public class CreditCardStrategy implements PaymentStrategy {
    private final String cardNumber;
    
    public CreditCardStrategy(String cardNumber) {
        this.cardNumber = cardNumber;
    }
    
    @Override
    public void pay(double amount) {
        System.out.println("Paid $" + amount + " with credit card " + cardNumber);
    }
}

public class PayPalStrategy implements PaymentStrategy {
    private final String email;
    
    public PayPalStrategy(String email) {
        this.email = email;
    }
    
    @Override
    public void pay(double amount) {
        System.out.println("Paid $" + amount + " via PayPal to " + email);
    }
}

// Context
public class ShoppingCart {
    private PaymentStrategy paymentStrategy;
    
    public void setPaymentStrategy(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }
    
    public void checkout(double amount) {
        paymentStrategy.pay(amount);
    }
}

// Uso
ShoppingCart cart = new ShoppingCart();
cart.setPaymentStrategy(new CreditCardStrategy("1234-5678"));
cart.checkout(100.0);
```

### Observer

**Problema**: Notificar múltiplos objetos sobre mudanças.

```java
// Subject interface
public interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers();
}

// Observer interface
public interface Observer {
    void update(String message);
}

// Concrete subject
public class NewsAgency implements Subject {
    private List<Observer> observers = new ArrayList<>();
    private String news;
    
    @Override
    public void attach(Observer observer) {
        observers.add(observer);
    }
    
    @Override
    public void detach(Observer observer) {
        observers.remove(observer);
    }
    
    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(news);
        }
    }
    
    public void setNews(String news) {
        this.news = news;
        notifyObservers();
    }
}

// Concrete observer
public class NewsChannel implements Observer {
    private final String name;
    
    public NewsChannel(String name) {
        this.name = name;
    }
    
    @Override
    public void update(String message) {
        System.out.println(name + " received news: " + message);
    }
}

// Uso
NewsAgency agency = new NewsAgency();
Observer channel1 = new NewsChannel("CNN");
Observer channel2 = new NewsChannel("BBC");

agency.attach(channel1);
agency.attach(channel2);

agency.setNews("Breaking news!");
// Output:
// CNN received news: Breaking news!
// BBC received news: Breaking news!
```

---

## Java-Specific Patterns

### Template Method

```java
public abstract class DataParser {
    // Template method (final)
    public final void parse(String filename) {
        openFile(filename);
        readData();
        processData();
        closeFile();
    }
    
    private void openFile(String filename) {
        System.out.println("Opening " + filename);
    }
    
    private void closeFile() {
        System.out.println("Closing file");
    }
    
    protected abstract void readData();
    protected abstract void processData();
}

public class CSVParser extends DataParser {
    @Override
    protected void readData() {
        System.out.println("Reading CSV data");
    }
    
    @Override
    protected void processData() {
        System.out.println("Processing CSV data");
    }
}
```

### Null Object Pattern

```java
// Interface
public interface Logger {
    void log(String message);
}

// Real object
public class ConsoleLogger implements Logger {
    @Override
    public void log(String message) {
        System.out.println("[LOG] " + message);
    }
}

// Null object
public class NullLogger implements Logger {
    @Override
    public void log(String message) {
        // Do nothing
    }
}

// Uso
public class Service {
    private final Logger logger;
    
    public Service(Logger logger) {
        this.logger = logger != null ? logger : new NullLogger();
    }
    
    public void doSomething() {
        logger.log("Doing something");  // Sem null check!
    }
}
```

---

## Anti-Patterns a Evitar

### God Object

```java
// ❌ EVITAR: Classe faz tudo
public class UserManager {
    public void createUser() { }
    public void deleteUser() { }
    public void sendEmail() { }
    public void logActivity() { }
    public void generateReport() { }
    // 50+ métodos...
}

// ✅ SOLUÇÃO: Single Responsibility
public class UserRepository {
    public void save(User user) { }
    public void delete(Long id) { }
}

public class EmailService {
    public void send(String to, String message) { }
}
```

---

## References

- [Design Patterns - Gang of Four](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/) - Livro original
- [Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/0596007124/) - Introdução didática
- [Effective Java](https://www.oreilly.com/library/view/effective-java/9780134686097/) - Patterns específicos de Java
