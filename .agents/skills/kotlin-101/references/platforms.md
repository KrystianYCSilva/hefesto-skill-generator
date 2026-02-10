---
name: platforms
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Kotlin Platforms

Kotlin allows compiling the same code to different targets.

## Kotlin/JVM
Compiles to Java bytecode.
- **Use case**: Backend (Spring, Ktor), Android, Desktop (Compose Multiplatform).
- **Interop**: 100% interoperable with Java. Can use all Java libraries.

## Kotlin/JS
Transpiles to JavaScript (ES5/ES2015).
- **Use case**: Frontend web apps (React wrappers), Node.js scripts.
- **Interop**: Can call DOM API and use NPM packages.
- **IR Compiler**: New compiler for better optimization and strictness.

## Kotlin/Native
Compiles to native binaries via LLVM (no VM required).
- **Use case**: iOS (shared logic), Desktop CLI tools, Embedded systems.
- **Interop**: Interoperates with C libraries (via `.def` files) and Objective-C/Swift.
- **Memory Management**: New memory manager (1.9+) handles GC automatically.

## Kotlin/Wasm (WebAssembly)
Compiles to WebAssembly (experimental/alpha).
- **Use case**: High-performance web modules, Compose for Web.
- **Targets**: `wasm-js` (browser), `wasm-wasi` (server-side).

