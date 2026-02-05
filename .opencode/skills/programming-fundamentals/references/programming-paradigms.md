# Programming Paradigms

Comprehensive guide to programming paradigms including Object-Oriented, Functional, Structured, and when to use each approach.

---

## Overview

Programming paradigms are fundamental styles of programming that provide frameworks for structuring code.

### Main Paradigms

1. **Imperative** - How to do it (step-by-step)
   - Procedural/Structured
   - Object-Oriented

2. **Declarative** - What to do (describe desired result)
   - Functional
   - Logic

---

## Procedural/Structured Programming

### Principles

- Sequential execution
- Procedures/functions as code units
- Local and global variables
- Control structures: if, while, for

### Example
```pseudocode
// Procedural approach
global_counter = 0

function increment_counter():
  global_counter = global_counter + 1

function process_data(data):
  result = []
  
  for item in data:
    if item > 0:
      increment_counter()
      result.append(item * 2)
  
  return result

// Usage
data = [1, -2, 3, 4, -5]
processed = process_data(data)
print(global_counter)  // 3
```

### Advantages
- Simple and intuitive
- Efficient execution
- Easy to understand flow
- Good for scripts and utilities

### Disadvantages
- Global state management
- Code reusability issues
- Difficult to maintain large systems
- Limited abstraction

### Best Use Cases
- System programming
- Scripts and utilities
- Performance-critical code
- Small to medium projects

---

## Object-Oriented Programming (OOP)

### Core Principles

**1. Encapsulation**
```pseudocode
class BankAccount:
  private balance: float
  
  constructor(initial_balance):
    this.balance = initial_balance
  
  public deposit(amount):
    if amount > 0:
      this.balance += amount
      return true
    return false
  
  public withdraw(amount):
    if amount > 0 and amount <= this.balance:
      this.balance -= amount
      return true
    return false
  
  public get_balance():
    return this.balance

// Usage
account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
// Cannot directly access account.balance from outside
```

**2. Inheritance**
```pseudocode
class Animal:
  protected name: string
  protected age: integer
  
  constructor(name, age):
    this.name = name
    this.age = age
  
  public make_sound():
    // Abstract method
    pass
  
  public get_info():
    return "Name: " + this.name + ", Age: " + this.age

class Dog extends Animal:
  private breed: string
  
  constructor(name, age, breed):
    super(name, age)
    this.breed = breed
  
  public make_sound():
    return "Woof!"
  
  public get_breed():
    return this.breed

class Cat extends Animal:
  constructor(name, age):
    super(name, age)
  
  public make_sound():
    return "Meow!"

// Usage
dog = Dog("Buddy", 3, "Golden Retriever")
cat = Cat("Whiskers", 2)

print(dog.make_sound())  // "Woof!"
print(cat.make_sound())  // "Meow!"
```

**3. Polymorphism**
```pseudocode
function animal_chorus(animals):
  for animal in animals:
    print(animal.make_sound())

// Different types, same interface
animals = [Dog("Rex", 5, "Bulldog"), Cat("Mittens", 3), Dog("Max", 2, "Beagle")]
animal_chorus(animals)
// Output:
// Woof!
// Meow!
// Woof!
```

**4. Abstraction**
```pseudocode
abstract class Shape:
  abstract calculate_area(): float
  abstract calculate_perimeter(): float
  
  public describe():
    return "Area: " + this.calculate_area() + 
           ", Perimeter: " + this.calculate_perimeter()

class Rectangle extends Shape:
  private width: float
  private height: float
  
  constructor(width, height):
    this.width = width
    this.height = height
  
  public calculate_area():
    return this.width * this.height
  
  public calculate_perimeter():
    return 2 * (this.width + this.height)

class Circle extends Shape:
  private radius: float
  
  constructor(radius):
    this.radius = radius
  
  public calculate_area():
    return 3.14159 * this.radius * this.radius
  
  public calculate_perimeter():
    return 2 * 3.14159 * this.radius
```

### OOP Design Patterns Preview

**Singleton**
```pseudocode
class Database:
  private static instance: Database = null
  private connection: Connection
  
  private constructor():
    this.connection = establish_connection()
  
  public static get_instance():
    if Database.instance == null:
      Database.instance = new Database()
    return Database.instance

// Usage
db1 = Database.get_instance()
db2 = Database.get_instance()
// db1 and db2 are the same instance
```

**Factory**
```pseudocode
class ShapeFactory:
  public static create_shape(type, params):
    if type == "circle":
      return Circle(params.radius)
    elif type == "rectangle":
      return Rectangle(params.width, params.height)
    elif type == "triangle":
      return Triangle(params.base, params.height)
    else:
      throw InvalidShapeType(type)

// Usage
circle = ShapeFactory.create_shape("circle", {radius: 5})
rectangle = ShapeFactory.create_shape("rectangle", {width: 10, height: 5})
```

### Advantages
- Modularity and reusability
- Real-world modeling
- Encapsulation of complexity
- Polymorphism flexibility
- Maintainable large systems

### Disadvantages
- Overhead and complexity
- Can be over-engineered
- Steep learning curve
- Performance overhead
- Not always natural fit

### Best Use Cases
- Large applications
- GUI applications
- Game development
- Enterprise software
- When modeling real-world entities

---

## Functional Programming

### Core Principles

**1. Pure Functions**
```pseudocode
// Pure function - same input, same output, no side effects
function add(a, b):
  return a + b

// Impure function - depends on external state
global_value = 10

function impure_add(a):
  return a + global_value  // Depends on global state

// Impure function - modifies external state
function impure_increment(counter):
  counter.value += 1  // Side effect
```

**2. Immutability**
```pseudocode
// Mutable approach (avoid in FP)
function add_item_mutable(list, item):
  list.append(item)  // Modifies original
  return list

// Immutable approach (preferred in FP)
function add_item_immutable(list, item):
  return list + [item]  // Returns new list

// Usage
original = [1, 2, 3]
new_list = add_item_immutable(original, 4)
// original: [1, 2, 3]
// new_list: [1, 2, 3, 4]
```

**3. First-Class and Higher-Order Functions**
```pseudocode
// First-class: functions as values
function multiply(a, b):
  return a * b

operation = multiply  // Assign function to variable
result = operation(3, 4)  // 12

// Higher-order: functions that take/return functions
function apply_twice(func, value):
  return func(func(value))

function add_one(x):
  return x + 1

result = apply_twice(add_one, 5)  // 7

// Returning functions
function create_multiplier(factor):
  return function(x):
    return x * factor

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  // 10
print(triple(5))  // 15
```

**4. Map, Filter, Reduce**
```pseudocode
// Map: transform each element
function square(x):
  return x * x

numbers = [1, 2, 3, 4, 5]
squared = map(square, numbers)  // [1, 4, 9, 16, 25]

// Filter: select elements
function is_even(x):
  return x % 2 == 0

evens = filter(is_even, numbers)  // [2, 4]

// Reduce: combine elements
function sum(accumulator, value):
  return accumulator + value

total = reduce(sum, numbers, 0)  // 15

// Chaining
result = reduce(sum, map(square, filter(is_even, numbers)), 0)
// [1,2,3,4,5] → [2,4] → [4,16] → 20
```

**5. Recursion**
```pseudocode
// Factorial
function factorial(n):
  if n <= 1:
    return 1
  return n * factorial(n - 1)

// Tail recursion (optimizable)
function factorial_tail(n, accumulator = 1):
  if n <= 1:
    return accumulator
  return factorial_tail(n - 1, n * accumulator)

// List processing
function sum_list(list):
  if list.is_empty():
    return 0
  return list.first() + sum_list(list.rest())

// Filter with recursion
function filter_recursive(predicate, list):
  if list.is_empty():
    return []
  
  first = list.first()
  rest = filter_recursive(predicate, list.rest())
  
  if predicate(first):
    return [first] + rest
  else:
    return rest
```

**6. Function Composition**
```pseudocode
function compose(f, g):
  return function(x):
    return f(g(x))

function add_one(x):
  return x + 1

function double(x):
  return x * 2

// Compose: (f ∘ g)(x) = f(g(x))
add_one_then_double = compose(double, add_one)
print(add_one_then_double(5))  // 12: (5 + 1) * 2

// Pipe: reverse composition
function pipe(g, f):
  return compose(f, g)

double_then_add_one = pipe(double, add_one)
print(double_then_add_one(5))  // 11: (5 * 2) + 1
```

**7. Closures**
```pseudocode
function create_counter():
  count = 0  // Closed over
  
  return {
    increment: function():
      count += 1
      return count
    ,
    decrement: function():
      count -= 1
      return count
    ,
    get_count: function():
      return count
  }

counter = create_counter()
print(counter.increment())  // 1
print(counter.increment())  // 2
print(counter.get_count())  // 2
```

### Functional Data Structures

**Immutable List**
```pseudocode
class ImmutableList:
  constructor(head, tail):
    this.head = head
    this.tail = tail
  
  prepend(value):
    return ImmutableList(value, this)
  
  map(func):
    if this.is_empty():
      return empty_list()
    return ImmutableList(func(this.head), this.tail.map(func))
  
  filter(predicate):
    if this.is_empty():
      return empty_list()
    
    filtered_tail = this.tail.filter(predicate)
    
    if predicate(this.head):
      return ImmutableList(this.head, filtered_tail)
    else:
      return filtered_tail
```

### Advantages
- Predictable behavior (pure functions)
- Easier testing
- Parallelization friendly
- No side effects
- Immutability prevents bugs
- Composable code

### Disadvantages
- Learning curve
- Performance overhead (immutability)
- Can be verbose
- Not intuitive for all problems
- Limited language support

### Best Use Cases
- Data transformation pipelines
- Concurrent/parallel processing
- Mathematical computations
- Event-driven systems
- Data analysis

---

## Comparing Paradigms

### Example Problem: Calculate sum of squares of even numbers

**Procedural**
```pseudocode
function sum_squares_of_evens_procedural(numbers):
  sum = 0
  
  for number in numbers:
    if number % 2 == 0:
      square = number * number
      sum = sum + square
  
  return sum
```

**Object-Oriented**
```pseudocode
class NumberProcessor:
  constructor(numbers):
    this.numbers = numbers
  
  filter_evens():
    evens = []
    for number in this.numbers:
      if number % 2 == 0:
        evens.append(number)
    return NumberProcessor(evens)
  
  square():
    squared = []
    for number in this.numbers:
      squared.append(number * number)
    return NumberProcessor(squared)
  
  sum():
    total = 0
    for number in this.numbers:
      total += number
    return total

// Usage
processor = NumberProcessor([1, 2, 3, 4, 5, 6])
result = processor.filter_evens().square().sum()
```

**Functional**
```pseudocode
function sum_squares_of_evens_functional(numbers):
  is_even = function(x): return x % 2 == 0
  square = function(x): return x * x
  sum = function(acc, x): return acc + x
  
  return reduce(sum, map(square, filter(is_even, numbers)), 0)

// Or with composition
sum_squares_of_evens = compose(
  partial(reduce, sum_func, _, 0),
  partial(map, square),
  partial(filter, is_even)
)
```

---

## Hybrid Approaches

Modern languages often support multiple paradigms.

### Functional + OOP
```pseudocode
class StreamProcessor:
  constructor(data):
    this.data = data
  
  // Functional methods
  map(transform):
    return StreamProcessor(map(transform, this.data))
  
  filter(predicate):
    return StreamProcessor(filter(predicate, this.data))
  
  reduce(combiner, initial):
    return reduce(combiner, this.data, initial)
  
  // Chaining
  process():
    return this

// Usage
result = StreamProcessor([1, 2, 3, 4, 5])
  .filter(is_even)
  .map(square)
  .reduce(sum, 0)
```

### OOP with Immutability
```pseudocode
class ImmutablePoint:
  constructor(x, y):
    this.x = x
    this.y = y
  
  // Return new instance instead of modifying
  move(dx, dy):
    return ImmutablePoint(this.x + dx, this.y + dy)
  
  scale(factor):
    return ImmutablePoint(this.x * factor, this.y * factor)

// Usage
p1 = ImmutablePoint(10, 20)
p2 = p1.move(5, 5)  // p1 unchanged
p3 = p2.scale(2)    // p2 unchanged
```

---

## Choosing the Right Paradigm

### Use OOP When:
- Modeling real-world entities
- Building large systems with many interacting components
- Need polymorphism and inheritance
- State management is complex
- Team is familiar with OOP

### Use Functional When:
- Data transformation is primary task
- Concurrency is important
- Need predictable, testable code
- Working with immutable data
- Mathematical or algorithmic problems

### Use Procedural When:
- Simple scripts or utilities
- Performance is critical
- Small codebase
- Sequential processing
- Low-level programming

### Hybrid Approach When:
- Leveraging strengths of multiple paradigms
- Modern application development
- Flexible architecture needed
- Team has diverse skills

---

## Common Patterns Across Paradigms

### Iterator Pattern

**OOP**
```pseudocode
class Iterator:
  has_next(): boolean
  next(): element

class Collection:
  create_iterator(): Iterator
```

**Functional**
```pseudocode
function iterate(collection, func):
  if collection.is_empty():
    return
  func(collection.first())
  iterate(collection.rest(), func)
```

### Strategy Pattern

**OOP**
```pseudocode
interface SortStrategy:
  sort(array): array

class QuickSort implements SortStrategy:
  sort(array):
    // Quick sort implementation

class MergeSort implements SortStrategy:
  sort(array):
    // Merge sort implementation

class Sorter:
  constructor(strategy):
    this.strategy = strategy
  
  sort(array):
    return this.strategy.sort(array)
```

**Functional**
```pseudocode
function sort_with_strategy(array, strategy):
  return strategy(array)

// Usage
sorted = sort_with_strategy(data, quick_sort)
sorted = sort_with_strategy(data, merge_sort)
```

---

## Performance Considerations

### OOP
- Virtual function call overhead
- Object allocation overhead
- Better cache locality with data-oriented design

### Functional
- Immutability creates temporary objects
- Tail call optimization important
- Lazy evaluation can improve performance

### Procedural
- Minimal overhead
- Direct memory access
- Cache-friendly for simple structures

---

## Testing Across Paradigms

### OOP Testing
```pseudocode
class BankAccountTest:
  test_deposit():
    account = BankAccount(100)
    account.deposit(50)
    assert account.get_balance() == 150
  
  test_withdraw():
    account = BankAccount(100)
    result = account.withdraw(50)
    assert result == true
    assert account.get_balance() == 50
```

### Functional Testing
```pseudocode
function test_add():
  assert add(2, 3) == 5
  assert add(0, 0) == 0
  assert add(-1, 1) == 0

function test_map():
  result = map(double, [1, 2, 3])
  assert result == [2, 4, 6]
```

**Functional code is often easier to test (pure functions).**

---

## Real-World Examples

### Web Framework (Hybrid)
```pseudocode
// OOP for structure
class Router:
  routes: Map
  
  add_route(path, handler):
    this.routes.set(path, handler)
  
  handle_request(request):
    handler = this.routes.get(request.path)
    return handler(request)

// Functional for request processing
function authenticate(request):
  // Return new request with auth info
  return {...request, user: get_user(request.token)}

function validate(request):
  // Return new request if valid, else error
  if is_valid(request):
    return request
  else:
    throw ValidationError()

function log_request(request):
  log(request)
  return request

// Middleware composition (functional)
function compose_middleware(...middlewares):
  return function(request):
    return reduce(apply, middlewares, request)

pipeline = compose_middleware(log_request, authenticate, validate)
```

### Data Processing (Functional)
```pseudocode
function process_sales_data(data):
  return data
    .filter(sale => sale.amount > 100)
    .map(sale => ({...sale, tax: sale.amount * 0.1}))
    .reduce((acc, sale) => acc + sale.amount + sale.tax, 0)
```

### Game Engine (OOP)
```pseudocode
class GameObject:
  update(delta_time): void
  render(): void

class Player extends GameObject:
  // Player-specific implementation

class Enemy extends GameObject:
  // Enemy-specific implementation

class GameEngine:
  objects: List<GameObject>
  
  game_loop():
    while running:
      delta = calculate_delta_time()
      
      for object in this.objects:
        object.update(delta)
        object.render()
```

---

## Summary

| Aspect | OOP | Functional | Procedural |
|--------|-----|------------|------------|
| **Data** | Objects with state | Immutable values | Variables |
| **Behavior** | Methods | Functions | Procedures |
| **Abstraction** | Classes/interfaces | Functions | Functions |
| **Code Reuse** | Inheritance | Composition | Function calls |
| **State** | Encapsulated | Avoided | Global/local |
| **Best For** | Complex systems | Data transformation | Simple scripts |

**Modern best practice: Use the right tool for the job, often combining paradigms.**
