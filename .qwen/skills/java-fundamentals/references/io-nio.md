# Java I/O & NIO

> **Referência avançada de**: java-fundamentals  
> **Tópico**: File Operations, Streams, NIO.2, Path API

---

## Overview

Java oferece duas APIs principais para I/O:
- **java.io**: API clássica baseada em streams (Java 1.0+)
- **java.nio**: New I/O com buffers e channels (Java 1.4+)
- **java.nio.file**: Modern file API (Java 7+)

---

## Reading Files

### Método 1: Files.readString() (Java 11+)

```java
// Mais simples e moderno
String content = Files.readString(Path.of("file.txt"));
```

### Método 2: Files.readAllLines() (Java 7+)

```java
List<String> lines = Files.readAllLines(Path.of("file.txt"));
for (String line : lines) {
    System.out.println(line);
}
```

### Método 3: BufferedReader

```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
}
```

### Método 4: Files.lines() Stream (Java 8+)

```java
try (Stream<String> lines = Files.lines(Path.of("file.txt"))) {
    lines.filter(line -> line.contains("keyword"))
         .forEach(System.out::println);
}
```

---

## Writing Files

### Método 1: Files.writeString() (Java 11+)

```java
Files.writeString(Path.of("output.txt"), "Hello World");
```

### Método 2: Files.write() (Java 7+)

```java
List<String> lines = Arrays.asList("Line 1", "Line 2", "Line 3");
Files.write(Path.of("output.txt"), lines);
```

### Método 3: BufferedWriter

```java
try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
    writer.write("Hello World");
    writer.newLine();
    writer.write("Second line");
}
```

---

## Path API (Java 7+)

### Creating Paths

```java
// Método estático (Java 11+)
Path path = Path.of("dir", "subdir", "file.txt");

// Método get (Java 7+)
Path path = Paths.get("dir/subdir/file.txt");

// Absolute path
Path absolute = Path.of("C:\\Users\\user\\file.txt");

// Relative path
Path relative = Path.of("../parent/file.txt");
```

### Path Operations

```java
Path path = Path.of("dir/subdir/file.txt");

// Get components
Path fileName = path.getFileName();        // file.txt
Path parent = path.getParent();            // dir/subdir
Path root = path.getRoot();                 // null (relativo)

// Resolve paths
Path base = Path.of("C:\\Users");
Path resolved = base.resolve("user/file.txt");  // C:\Users\user\file.txt

// Normalize paths
Path messy = Path.of("dir/../file.txt");
Path clean = messy.normalize();  // file.txt

// Convert to absolute
Path abs = path.toAbsolutePath();
```

---

## File Operations

### Check Existence

```java
Path path = Path.of("file.txt");

if (Files.exists(path)) {
    System.out.println("File exists");
}

if (Files.notExists(path)) {
    System.out.println("File does not exist");
}

// Check if regular file or directory
boolean isFile = Files.isRegularFile(path);
boolean isDir = Files.isDirectory(path);
```

### Create/Delete

```java
// Create file
Path newFile = Path.of("newfile.txt");
Files.createFile(newFile);

// Create directory
Path newDir = Path.of("newdir");
Files.createDirectory(newDir);

// Create directories (including parents)
Path nestedDir = Path.of("parent/child/grandchild");
Files.createDirectories(nestedDir);

// Delete file/empty directory
Files.delete(path);

// Delete if exists (não lança exception)
Files.deleteIfExists(path);
```

### Copy/Move

```java
Path source = Path.of("source.txt");
Path target = Path.of("target.txt");

// Copy file
Files.copy(source, target);

// Copy with options
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

// Move file
Files.move(source, target);

// Move with options
Files.move(source, target, StandardCopyOption.ATOMIC_MOVE);
```

### List Directory

```java
Path dir = Path.of("mydir");

// List files (shallow)
try (Stream<Path> files = Files.list(dir)) {
    files.forEach(System.out::println);
}

// Walk tree (recursive)
try (Stream<Path> files = Files.walk(dir)) {
    files.filter(Files::isRegularFile)
         .forEach(System.out::println);
}

// Walk tree with depth limit
try (Stream<Path> files = Files.walk(dir, 2)) {
    files.forEach(System.out::println);
}
```

---

## File Attributes

### Basic Attributes

```java
Path path = Path.of("file.txt");

// File size
long size = Files.size(path);

// Last modified time
FileTime lastModified = Files.getLastModifiedTime(path);

// Set last modified time
Files.setLastModifiedTime(path, FileTime.fromMillis(System.currentTimeMillis()));

// Is hidden
boolean hidden = Files.isHidden(path);

// Is readable/writable/executable
boolean readable = Files.isReadable(path);
boolean writable = Files.isWritable(path);
boolean executable = Files.isExecutable(path);
```

### Advanced Attributes

```java
// Read all basic attributes at once
BasicFileAttributes attrs = Files.readAttributes(path, BasicFileAttributes.class);

System.out.println("Size: " + attrs.size());
System.out.println("Creation time: " + attrs.creationTime());
System.out.println("Last modified: " + attrs.lastModifiedTime());
System.out.println("Is directory: " + attrs.isDirectory());
System.out.println("Is regular file: " + attrs.isRegularFile());
```

---

## Binary Files

### Reading Binary

```java
// Read all bytes
byte[] bytes = Files.readAllBytes(Path.of("image.jpg"));

// Read with InputStream
try (InputStream in = Files.newInputStream(Path.of("data.bin"))) {
    byte[] buffer = new byte[1024];
    int bytesRead;
    while ((bytesRead = in.read(buffer)) != -1) {
        // Process buffer
    }
}
```

### Writing Binary

```java
// Write all bytes
byte[] data = {0x48, 0x65, 0x6C, 0x6C, 0x6F};
Files.write(Path.of("output.bin"), data);

// Write with OutputStream
try (OutputStream out = Files.newOutputStream(Path.of("data.bin"))) {
    out.write(data);
}
```

---

## Watch Service (File System Events)

```java
// Create watch service
WatchService watchService = FileSystems.getDefault().newWatchService();

// Register directory
Path dir = Path.of("watchdir");
dir.register(watchService, 
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_DELETE,
    StandardWatchEventKinds.ENTRY_MODIFY);

// Poll for events
while (true) {
    WatchKey key = watchService.take();
    
    for (WatchEvent<?> event : key.pollEvents()) {
        WatchEvent.Kind<?> kind = event.kind();
        Path filename = (Path) event.context();
        
        System.out.println(kind + ": " + filename);
    }
    
    key.reset();
}
```

---

## Best Practices

### ✅ DO

```java
// Usar try-with-resources
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    // ler arquivo
}

// Usar Path API moderna (Java 7+)
Path path = Path.of("file.txt");
String content = Files.readString(path);

// Usar Streams para processar linhas
Files.lines(Path.of("largefile.txt"))
     .filter(line -> line.contains("keyword"))
     .forEach(System.out::println);
```

### ❌ DON'T

```java
// NÃO esquecer de fechar recursos
FileReader reader = new FileReader("file.txt");
// FALTA: reader.close()

// NÃO usar File (API antiga)
File file = new File("file.txt");  // ❌ Usar Path

// NÃO carregar arquivos grandes inteiros na memória
String huge = Files.readString(Path.of("10GB.txt"));  // ❌ OutOfMemoryError
```

---

## Common Patterns

### Copy Directory Recursively

```java
public void copyDirectory(Path source, Path target) throws IOException {
    Files.walk(source).forEach(src -> {
        try {
            Path dest = target.resolve(source.relativize(src));
            if (Files.isDirectory(src)) {
                Files.createDirectories(dest);
            } else {
                Files.copy(src, dest, StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    });
}
```

### Delete Directory Recursively

```java
public void deleteDirectory(Path dir) throws IOException {
    Files.walk(dir)
         .sorted(Comparator.reverseOrder())  // Deletar filhos antes de pais
         .forEach(path -> {
             try {
                 Files.delete(path);
             } catch (IOException e) {
                 throw new UncheckedIOException(e);
             }
         });
}
```

---

## References

- [Java I/O Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/) - Oracle oficial
- [Java NIO.2 Guide](https://docs.oracle.com/javase/tutorial/essential/io/fileio.html) - File I/O moderno
- [Files Javadoc](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Files.html) - API completa
