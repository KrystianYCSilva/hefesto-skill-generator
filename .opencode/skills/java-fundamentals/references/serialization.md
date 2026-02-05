# Serialization & JSON

> **Referência avançada de**: java-fundamentals  
> **Tópico**: Object Serialization, JSON Parsing

---

## Overview

Serialization converte objetos Java em bytes (e vice-versa) para:
- Persistência em arquivos
- Transmissão via rede
- Armazenamento em cache

---

## Java Serialization (Built-in)

### Serializable Interface

```java
import java.io.Serializable;

public class Person implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String name;
    private int age;
    private transient String password;  // NÃO será serializado
    
    public Person(String name, int age, String password) {
        this.name = name;
        this.age = age;
        this.password = password;
    }
    
    // Getters/setters...
}
```

### Serializing Objects

```java
Person person = new Person("Alice", 30, "secret123");

// Write to file
try (ObjectOutputStream out = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    out.writeObject(person);
}
```

### Deserializing Objects

```java
// Read from file
try (ObjectInputStream in = new ObjectInputStream(
        new FileInputStream("person.ser"))) {
    Person person = (Person) in.readObject();
    System.out.println(person.getName());  // Alice
    System.out.println(person.getPassword());  // null (transient)
}
```

### serialVersionUID

```java
// SEMPRE declare serialVersionUID explicitamente
private static final long serialVersionUID = 1L;

// Se não declarar, será gerado automaticamente
// Mudanças na classe invalidam serialização antiga!
```

### transient Keyword

```java
public class User implements Serializable {
    private String username;
    private transient String password;  // NÃO serializa
    private transient Connection db;    // NÃO serializa
    
    // password e db não são salvos
}
```

---

## JSON with Jackson (Recomendado)

### Setup (Maven)

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.15.2</version>
</dependency>
```

### Object to JSON

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class Person {
    private String name;
    private int age;
    
    // Construtores, getters, setters...
}

// Serializar para JSON
ObjectMapper mapper = new ObjectMapper();
Person person = new Person("Alice", 30);

// Para String
String json = mapper.writeValueAsString(person);
// {"name":"Alice","age":30}

// Para arquivo
mapper.writeValue(new File("person.json"), person);
```

### JSON to Object

```java
ObjectMapper mapper = new ObjectMapper();

// De String
String json = "{\"name\":\"Alice\",\"age\":30}";
Person person = mapper.readValue(json, Person.class);

// De arquivo
Person person = mapper.readValue(new File("person.json"), Person.class);

// De URL
Person person = mapper.readValue(
    new URL("https://api.example.com/person/1"), 
    Person.class
);
```

### Collections

```java
ObjectMapper mapper = new ObjectMapper();

// List to JSON
List<Person> people = Arrays.asList(
    new Person("Alice", 30),
    new Person("Bob", 25)
);
String json = mapper.writeValueAsString(people);

// JSON to List
List<Person> people = mapper.readValue(
    json,
    new TypeReference<List<Person>>() {}
);

// Map to JSON
Map<String, Person> map = new HashMap<>();
map.put("person1", new Person("Alice", 30));
String json = mapper.writeValueAsString(map);

// JSON to Map
Map<String, Person> map = mapper.readValue(
    json,
    new TypeReference<Map<String, Person>>() {}
);
```

### Annotations

```java
import com.fasterxml.jackson.annotation.*;

public class Person {
    @JsonProperty("full_name")  // Mapear para nome diferente
    private String name;
    
    @JsonIgnore  // Não serializar
    private String password;
    
    @JsonFormat(pattern = "yyyy-MM-dd")  // Formatar data
    private Date birthDate;
    
    @JsonInclude(JsonInclude.Include.NON_NULL)  // Ignorar se null
    private String middleName;
    
    // Getters/setters...
}

// JSON gerado:
// {"full_name":"Alice","birthDate":"1990-01-15"}
// password não aparece
```

### Custom Serialization

```java
public class PersonSerializer extends JsonSerializer<Person> {
    @Override
    public void serialize(Person person, JsonGenerator gen, SerializerProvider provider)
            throws IOException {
        gen.writeStartObject();
        gen.writeStringField("name", person.getName().toUpperCase());
        gen.writeNumberField("age", person.getAge());
        gen.writeEndObject();
    }
}

// Usar serializer
@JsonSerialize(using = PersonSerializer.class)
public class Person {
    // ...
}
```

---

## JSON with Gson (Alternativa)

### Setup (Maven)

```xml
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.10.1</version>
</dependency>
```

### Object to JSON

```java
import com.google.gson.Gson;

Gson gson = new Gson();
Person person = new Person("Alice", 30);

// Para String
String json = gson.toJson(person);

// Para Writer
try (Writer writer = new FileWriter("person.json")) {
    gson.toJson(person, writer);
}
```

### JSON to Object

```java
Gson gson = new Gson();

// De String
String json = "{\"name\":\"Alice\",\"age\":30}";
Person person = gson.fromJson(json, Person.class);

// De Reader
try (Reader reader = new FileReader("person.json")) {
    Person person = gson.fromJson(reader, Person.class);
}

// Collections
Type listType = new TypeToken<List<Person>>(){}.getType();
List<Person> people = gson.fromJson(json, listType);
```

### Gson Annotations

```java
import com.google.gson.annotations.*;

public class Person {
    @SerializedName("full_name")  // Mapear nome
    private String name;
    
    @Expose(serialize = false)  // Não serializar
    private String password;
    
    @Since(1.0)  // Desde versão 1.0
    private String email;
    
    @Until(2.0)  // Até versão 2.0
    private String oldField;
}
```

---

## Best Practices

### ✅ DO

```java
// SEMPRE declarar serialVersionUID
private static final long serialVersionUID = 1L;

// Usar transient para dados sensíveis
private transient String password;

// Preferir Jackson/Gson para JSON
ObjectMapper mapper = new ObjectMapper();

// Usar try-with-resources
try (ObjectOutputStream out = new ObjectOutputStream(...)) {
    out.writeObject(obj);
}
```

### ❌ DON'T

```java
// NÃO serializar dados sensíveis
public class User implements Serializable {
    private String password;  // ❌ Usar transient
}

// NÃO esquecer serialVersionUID
public class Data implements Serializable {
    // ❌ FALTA: serialVersionUID
}

// NÃO usar Serialization Java para APIs REST
// ❌ Use JSON (Jackson/Gson)
```

---

## Common Patterns

### Deep Clone via Serialization

```java
public static <T extends Serializable> T deepClone(T object) {
    try {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(object);
        
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        return (T) ois.readObject();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
```

### Pretty Print JSON

```java
// Jackson
ObjectMapper mapper = new ObjectMapper();
mapper.enable(SerializationFeature.INDENT_OUTPUT);
String json = mapper.writeValueAsString(person);

// Gson
Gson gson = new GsonBuilder().setPrettyPrinting().create();
String json = gson.toJson(person);
```

---

## References

- [Java Serialization](https://docs.oracle.com/javase/tutorial/jndi/objects/serial.html) - Oracle tutorial
- [Jackson Documentation](https://github.com/FasterXML/jackson-docs) - Jackson oficial
- [Gson User Guide](https://github.com/google/gson/blob/master/UserGuide.md) - Gson oficial
