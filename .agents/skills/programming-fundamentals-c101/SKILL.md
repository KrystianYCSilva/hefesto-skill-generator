---
name: programming-fundamentals-c101
description: |
  Teach fundamental programming concepts and C language basics including variables, arrays, matrices, files, pointers, loops, functions, and control structures.
  Use when: introducing programming fundamentals, learning C basics, understanding core programming concepts, or establishing foundational knowledge for developers.
---

# Programming Fundamentals and C Language Basics (C-101)

Programming fundamentals form the foundation for all software development. This skill covers essential concepts including variables, data structures, control flow, and the C programming language basics that every programmer needs to understand.

## How to work with variables

Variables are named storage locations in memory that hold values of specific data type.

- **Declaration**: Specify the type followed by the variable name (e.g., `int age;`, `float price;`, `char letter;`)
- **Initialization**: Assign a value at declaration (`int count = 0;`)
- **Naming**: Use meaningful names following conventions (lowercase with underscores: `student_name`)
- **Data Types**: Common types include `int`, `float`, `double`, `char`, and `void`
- **Scope**: Variables have local (within function/block) or global (throughout program) scope

## How to use arrays and matrices

Arrays and matrices store collections of elements of the same data type.

### Arrays (One-dimensional)
- **Declaration**: `int numbers[10];` creates array of 10 integers
- **Access**: Use index starting from 0 (`numbers[0]` is first element)
- **Initialization**: `int values[] = {1, 2, 3, 4, 5};` (size determined automatically)

### Matrices (Two-dimensional arrays)
- **Declaration**: `int matrix[3][4];` creates 3x4 matrix (3 rows, 4 columns)
- **Access**: Use two indices (`matrix[row][column]`)
- **Initialization**: `int grid[][2] = {{1, 2}, {3, 4}, {5, 6}};`

## How to implement control structures and loops

Control structures determine the flow of execution in programs.

### Conditional Structures
- **if-else**: Execute code based on conditions (`if (condition) { /* code */ } else { /* alternative */ }`)
- **switch**: Multiple condition evaluation (`switch (variable) { case value1: /* code */ break; }`)

### Loops
- **for loop**: Known number of iterations (`for (int i = 0; i < 10; i++) { /* code */ }`)
- **while loop**: Continue while condition is true (`while (condition) { /* code */ }`)
- **do-while**: Execute at least once (`do { /* code */ } while (condition);`)

## How to create and use functions

Functions are reusable blocks of code that perform specific tasks.

- **Function Declaration**: Specify return type, name, and parameters (`int add(int a, int b);`)
- **Function Definition**: Implement the function body
```c
int add(int a, int b) {
    return a + b;
}
```
- **Function Call**: Use function name with arguments (`result = add(5, 3);`)
- **Return Statement**: Send value back to caller (`return value;`)
- **Void Functions**: Functions that don't return values (`void print_message()`)

## How to work with pointers

Pointers are variables that store memory addresses of other variables.

- **Declaration**: Use asterisk (`int *ptr;` declares pointer to integer)
- **Address Operator**: `&variable` gets the address of a variable
- **Dereference**: `*ptr` accesses the value at the address stored in pointer
- **Initialization**: `int value = 10; int *ptr = &value;`
- **Pointer Arithmetic**: Move through memory (`ptr++`, `ptr--`, `ptr + n`)

## How to handle files

File operations allow reading from and writing to external files.

- **File Pointer**: Declare with `FILE *fp;`
- **Opening Files**: Use `fopen("filename", "mode")` where modes include:
  - `"r"` - read, `"w"` - write, `"a"` - append
  - `"rb"`, `"wb"` - binary modes
- **Reading/Writing**: 
  - `fprintf(fp, "text");` writes formatted text
  - `fscanf(fp, "%d", &var);` reads formatted input
  - `fgets(buffer, size, fp);` reads string
- **Closing Files**: Always close with `fclose(fp);`

## How to apply best practices for beginners

Follow these principles to become a better programmer:

- **Code Readability**: Use meaningful variable names and consistent indentation
- **Comments**: Add explanations for complex logic (`// single line` or `/* multi-line */`)
- **Modularity**: Break complex problems into smaller functions
- **Memory Management**: Free allocated memory to prevent leaks
- **Error Handling**: Check return values and handle potential errors
- **Testing**: Verify code works with different inputs