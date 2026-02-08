# Build System Configuration

## Gradle (Kotlin DSL)

### Mixed Compilation
Ensure Kotlin compiles alongside Java.

```kotlin
plugins {
    java
    kotlin("jvm") version "1.9.22"
}

sourceSets {
    main {
        java.srcDirs("src/main/java", "src/main/kotlin")
    }
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "17"
    }
}
```

## Maven

### Execution Order
Kotlin must compile before Java if they mix.

```xml
<plugin>
    <groupId>org.jetbrains.kotlin</groupId>
    <artifactId>kotlin-maven-plugin</artifactId>
    <version>${kotlin.version}</version>
    <executions>
        <execution>
            <id>compile</id>
            <goals><goal>compile</goal></goals>
            <configuration>
                <sourceDirs>
                    <sourceDir>${project.basedir}/src/main/kotlin</sourceDir>
                    <sourceDir>${project.basedir}/src/main/java</sourceDir>
                </sourceDirs>
            </configuration>
        </execution>
    </executions>
</plugin>
```
