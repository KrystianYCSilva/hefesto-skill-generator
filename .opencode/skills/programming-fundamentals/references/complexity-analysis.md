# Complexity Analysis

Comprehensive guide to analyzing algorithm complexity using Big O notation, space complexity, and performance trade-offs.

---

## Big O Notation Fundamentals

### Definition
Big O describes the **upper bound** of an algorithm's growth rate as input size n approaches infinity.

Formally: f(n) = O(g(n)) if there exist constants c > 0 and n₀ ≥ 0 such that:
```
f(n) ≤ c · g(n) for all n ≥ n₀
```

### Common Complexity Classes

```
O(1)         Constant
O(log n)     Logarithmic
O(n)         Linear
O(n log n)   Linearithmic
O(n²)        Quadratic
O(n³)        Cubic
O(2ⁿ)        Exponential
O(n!)        Factorial
```

### Visual Comparison (n = 100)

| Complexity | Operations | Example |
|------------|-----------|---------|
| O(1) | 1 | Array access |
| O(log n) | 7 | Binary search |
| O(n) | 100 | Linear search |
| O(n log n) | 664 | Merge sort |
| O(n²) | 10,000 | Bubble sort |
| O(2ⁿ) | 1.27 × 10³⁰ | Subset generation |
| O(n!) | 9.33 × 10¹⁵⁷ | Permutation generation |

---

## Analyzing Time Complexity

### Rule 1: Drop Constants
```pseudocode
// Both are O(n)
algorithm_1(array):
  for i from 0 to n - 1:
    print(array[i])

algorithm_2(array):
  for i from 0 to n - 1:
    print(array[i])
  for i from 0 to n - 1:
    print(array[i])
```

3n + 5 → O(n)  
n/2 → O(n)  
100n → O(n)

### Rule 2: Drop Non-Dominant Terms
```pseudocode
algorithm(array):
  // O(n) loop
  for i from 0 to n - 1:
    print(array[i])
  
  // O(n²) nested loops
  for i from 0 to n - 1:
    for j from 0 to n - 1:
      print(array[i], array[j])
```

Total: O(n) + O(n²) = O(n²)

n³ + n² + n + 1 → O(n³)  
2ⁿ + n³ → O(2ⁿ)

### Rule 3: Different Inputs, Different Variables
```pseudocode
algorithm(array_a, array_b):
  for item in array_a:     // O(a)
    print(item)
  
  for item in array_b:     // O(b)
    print(item)
```

Total: O(a + b), NOT O(n)

```pseudocode
algorithm(array_a, array_b):
  for a in array_a:        // O(a)
    for b in array_b:      // O(b)
      print(a, b)
```

Total: O(a × b), NOT O(n²)

### Rule 4: Best, Average, Worst Case

Example: Quick Sort
```pseudocode
quick_sort(array):
  // Best/Average: O(n log n)  - balanced partitions
  // Worst: O(n²)              - already sorted
```

**Always specify which case when discussing complexity!**

---

## Constant Time - O(1)

Operations that take the same time regardless of input size.

```pseudocode
// O(1) examples
get_first(array):
  return array[0]

get_last(array):
  return array[array.length - 1]

hash_table_lookup(hash, key):
  return hash[key]

push_to_stack(stack, value):
  stack.push(value)

// Still O(1) even with multiple operations
swap(array, i, j):
  temp = array[i]
  array[i] = array[j]
  array[j] = temp
```

**Key Insight:** Number of operations is fixed, not dependent on n.

---

## Logarithmic Time - O(log n)

Input size halves with each iteration.

```pseudocode
binary_search(array, target):
  left = 0
  right = n - 1
  
  while left <= right:           // log n iterations
    mid = (left + right) / 2
    
    if array[mid] == target:
      return mid
    elif array[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  
  return -1
```

**Analysis:**
- n = 32: 5 iterations (2⁵ = 32)
- n = 1024: 10 iterations (2¹⁰ = 1024)
- n = 1,000,000: 20 iterations

**Other Examples:**
- Binary search tree operations (balanced)
- Finding element in balanced BST
- Certain divide-and-conquer algorithms

---

## Linear Time - O(n)

Iterate through entire input once.

```pseudocode
find_max(array):
  max_value = array[0]
  
  for i from 1 to n - 1:        // n iterations
    if array[i] > max_value:
      max_value = array[i]
  
  return max_value

print_array(array):
  for item in array:            // n iterations
    print(item)
```

**Key Insight:** Single pass through data.

---

## Linearithmic Time - O(n log n)

Common in efficient sorting algorithms.

```pseudocode
merge_sort(array):
  if array.length <= 1:
    return array
  
  mid = array.length / 2
  left = merge_sort(array[0..mid])      // T(n/2)
  right = merge_sort(array[mid..n])     // T(n/2)
  
  return merge(left, right)             // O(n)
```

**Recurrence:** T(n) = 2T(n/2) + O(n) = O(n log n)

**Analysis:**
- log n levels of recursion
- n work per level
- Total: n × log n

**Examples:**
- Merge Sort
- Quick Sort (average case)
- Heap Sort

---

## Quadratic Time - O(n²)

Nested loops over the same input.

```pseudocode
bubble_sort(array):
  for i from 0 to n - 1:              // n iterations
    for j from 0 to n - i - 2:        // n iterations
      if array[j] > array[j + 1]:
        swap(array[j], array[j + 1])
```

**Analysis:**
- Outer loop: n times
- Inner loop: n times
- Total: n × n = n²

```pseudocode
// Common patterns

// Pattern 1: All pairs
for i from 0 to n - 1:
  for j from 0 to n - 1:
    process(i, j)                     // O(n²)

// Pattern 2: Unique pairs
for i from 0 to n - 1:
  for j from i + 1 to n - 1:
    process(i, j)                     // Still O(n²)
// Iterations: n(n-1)/2 = O(n²)
```

**Examples:**
- Selection Sort
- Insertion Sort (worst case)
- Checking all pairs

---

## Polynomial Time - O(nᵏ)

Multiple nested loops.

```pseudocode
// O(n³)
three_sum(array, target):
  for i from 0 to n - 1:
    for j from i + 1 to n - 1:
      for k from j + 1 to n - 1:
        if array[i] + array[j] + array[k] == target:
          return true
  return false
```

**Examples:**
- O(n³): Matrix multiplication (naive), three nested loops
- O(n⁴): Four nested loops

---

## Exponential Time - O(2ⁿ)

Recursive algorithms with branching.

```pseudocode
// Naive Fibonacci
fibonacci(n):
  if n <= 1:
    return n
  return fibonacci(n - 1) + fibonacci(n - 2)
```

**Analysis:**
```
fib(5)
├─ fib(4)
│  ├─ fib(3)
│  │  ├─ fib(2)
│  │  │  ├─ fib(1)
│  │  │  └─ fib(0)
│  │  └─ fib(1)
│  └─ fib(2)
│     ├─ fib(1)
│     └─ fib(0)
└─ fib(3)
   ├─ fib(2)
   │  ├─ fib(1)
   │  └─ fib(0)
   └─ fib(1)
```

Recursive calls: 2⁰ + 2¹ + 2² + ... + 2ⁿ ≈ 2ⁿ⁺¹ = O(2ⁿ)

**Examples:**
- Naive recursive Fibonacci
- Power set generation
- Subset sum (brute force)

---

## Factorial Time - O(n!)

Generating all permutations.

```pseudocode
permutations(array):
  if array.length == 0:
    return [[]]
  
  result = []
  for i from 0 to array.length - 1:
    rest = array without element at i
    for perm in permutations(rest):
      result.append([array[i]] + perm)
  
  return result
```

**Analysis:**
- n choices for first position
- n-1 for second
- ...
- 1 for last
- Total: n! permutations

**Examples:**
- Traveling Salesman (brute force)
- Generating all permutations

---

## Space Complexity

Measures memory usage as function of input size.

### Auxiliary Space vs Total Space

**Auxiliary Space:** Extra space beyond input  
**Total Space:** Input + auxiliary space

```pseudocode
// O(1) auxiliary space
bubble_sort(array):
  // Only uses constant extra variables
  for i from 0 to n - 1:
    for j from 0 to n - i - 2:
      if array[j] > array[j + 1]:
        temp = array[j]              // O(1) extra
        array[j] = array[j + 1]
        array[j + 1] = temp

// O(n) auxiliary space
merge_sort(array):
  if array.length <= 1:
    return array
  
  mid = array.length / 2
  left = array[0..mid]               // O(n) extra
  right = array[mid..n]              // O(n) extra
  
  return merge(left, right)
```

### Recursive Space Complexity

Recursion uses stack space.

```pseudocode
// O(n) space due to recursion
factorial(n):
  if n == 0:
    return 1
  return n * factorial(n - 1)        // n stack frames
```

**Call stack:**
```
factorial(5)
  factorial(4)
    factorial(3)
      factorial(2)
        factorial(1)
          factorial(0) → return 1
```

Maximum depth: n → O(n) space

```pseudocode
// O(log n) space
binary_search_recursive(array, target, left, right):
  if left > right:
    return -1
  
  mid = (left + right) / 2
  
  if array[mid] == target:
    return mid
  elif array[mid] < target:
    return binary_search_recursive(array, target, mid + 1, right)
  else:
    return binary_search_recursive(array, target, left, mid - 1)
```

Maximum depth: log n → O(log n) space

---

## Amortized Analysis

Average time per operation over a sequence of operations.

### Dynamic Array Append

```pseudocode
DynamicArray:
  capacity = 1
  size = 0
  data = new array[capacity]
  
  append(value):
    if size == capacity:
      resize()                       // O(n) occasionally
    data[size++] = value             // O(1) usually
  
  resize():
    new_capacity = capacity * 2
    new_data = new array[new_capacity]
    copy(data, new_data)             // O(n)
    data = new_data
    capacity = new_capacity
```

**Analysis:**
- n appends total
- Resizes at: 1, 2, 4, 8, 16, ..., n
- Total copy cost: 1 + 2 + 4 + ... + n = 2n - 1 = O(n)
- Average per append: O(n) / n = O(1)

**Amortized O(1) per append!**

### Aggregate Method

Total cost of n operations / n

### Accounting Method

Assign costs to operations:
- Cheap operations: charge more (save credit)
- Expensive operations: use saved credit

For Dynamic Array:
- Append without resize: charge 3
  - 1 for insert
  - 2 for future resize
- Append with resize: use saved credit

### Potential Method

Define potential function φ:
- Amortized cost = actual cost + Δφ

---

## Best, Average, Worst Case Analysis

### Example: Quick Sort

```pseudocode
quick_sort(array, low, high):
  if low < high:
    pivot_index = partition(array, low, high)
    quick_sort(array, low, pivot_index - 1)
    quick_sort(array, pivot_index + 1, high)
```

**Best Case: O(n log n)**
- Pivot divides array evenly every time
- Recurrence: T(n) = 2T(n/2) + O(n)

**Average Case: O(n log n)**
- Pivot reasonably balanced most of the time
- Even 9:1 split gives O(n log n)

**Worst Case: O(n²)**
- Pivot is always smallest or largest
- Recurrence: T(n) = T(n-1) + O(n)
- Example: Already sorted array with first element as pivot

### Example: Binary Search

**Best Case: O(1)**
- Target is at middle position

**Average Case: O(log n)**
- Target found after log n comparisons on average

**Worst Case: O(log n)**
- Target at leaf or not present

---

## Time-Space Trade-offs

### Fibonacci: Time vs Space

**Naive Recursive: O(2ⁿ) time, O(n) space**
```pseudocode
fib(n):
  if n <= 1:
    return n
  return fib(n - 1) + fib(n - 2)
```

**Memoization: O(n) time, O(n) space**
```pseudocode
fib_memo(n, memo):
  if n in memo:
    return memo[n]
  
  if n <= 1:
    return n
  
  memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
  return memo[n]
```

**Bottom-up DP: O(n) time, O(n) space**
```pseudocode
fib_dp(n):
  dp = new array[n + 1]
  dp[0] = 0
  dp[1] = 1
  
  for i from 2 to n:
    dp[i] = dp[i - 1] + dp[i - 2]
  
  return dp[n]
```

**Optimized: O(n) time, O(1) space**
```pseudocode
fib_optimized(n):
  if n <= 1:
    return n
  
  prev2 = 0
  prev1 = 1
  
  for i from 2 to n:
    current = prev1 + prev2
    prev2 = prev1
    prev1 = current
  
  return prev1
```

### Hash Table: O(1) vs O(n)

**Trade:** More space → Faster lookup

- Small hash table: O(n) chains
- Large hash table: O(1) lookup (more space)

---

## Practical Complexity Considerations

### Hidden Constants

O(n) with constant 1000 vs O(n²) with constant 0.001:
- n < 1000: O(n²) faster
- n > 1000: O(n) faster

### Cache Effects

Array (cache-friendly) vs Linked List (cache-unfriendly):
- Array: Sequential memory → good cache locality
- Linked List: Random memory → cache misses

### Real-World Performance

```
Algorithm A: 100n operations
Algorithm B: n log n operations

n = 10:
  A: 1,000
  B: 33

n = 1000:
  A: 100,000
  B: 9,966

n = 1,000,000:
  A: 100,000,000
  B: 19,931,569
```

**Big O is asymptotic - matters for large n!**

---

## Complexity Analysis Techniques

### 1. Count Loop Iterations

```pseudocode
for i from 0 to n - 1:              // n times
  for j from 0 to n - 1:            // n times
    operation()                     // O(1)

Total: n × n × O(1) = O(n²)
```

### 2. Solve Recurrence Relations

```pseudocode
T(n) = 2T(n/2) + O(n)

Using Master Theorem:
T(n) = aT(n/b) + f(n)

a = 2, b = 2, f(n) = n
n^(log_b a) = n^(log_2 2) = n

f(n) = Θ(n^(log_b a))
Therefore: T(n) = Θ(n log n)
```

### 3. Master Theorem

For T(n) = aT(n/b) + f(n):

**Case 1:** f(n) = O(n^(log_b a - ε)) for ε > 0  
Result: T(n) = Θ(n^(log_b a))

**Case 2:** f(n) = Θ(n^(log_b a))  
Result: T(n) = Θ(n^(log_b a) log n)

**Case 3:** f(n) = Ω(n^(log_b a + ε)) and af(n/b) ≤ cf(n)  
Result: T(n) = Θ(f(n))

### 4. Substitution Method

Guess the form, then prove by induction.

Example: T(n) = 2T(n/2) + n

Guess: T(n) = O(n log n)

Prove: T(n) ≤ cn log n for some c > 0

```
T(n) = 2T(n/2) + n
     ≤ 2(c(n/2)log(n/2)) + n
     = cn(log n - log 2) + n
     = cn log n - cn + n
     ≤ cn log n  (if c ≥ 1)
```

---

## Common Mistakes

### Mistake 1: Ignoring Input Size
```pseudocode
// NOT O(1)! It's O(n)
sum_array(array):
  sum = 0
  for item in array:
    sum += item
  return sum
```

### Mistake 2: Confusing Best with Average
"Binary search is O(1)" - Wrong! That's best case.

### Mistake 3: Adding When Should Multiply
```pseudocode
// This is O(n × m), not O(n + m)
for i in array1:        // n times
  for j in array2:      // m times
    operation()
```

### Mistake 4: Ignoring Nested Operations
```pseudocode
// This is O(n²), not O(n)
for i from 0 to n - 1:
  // slice() is O(n)
  subarray = array[0..i]      // O(i)
  process(subarray)
```

---

## Quick Reference

| Data Structure | Access | Search | Insert | Delete |
|----------------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| Hash Table | - | O(1)* | O(1)* | O(1)* |
| Binary Search Tree | O(log n)* | O(log n)* | O(log n)* | O(log n)* |
| Binary Heap | O(log n) | O(n) | O(log n) | O(log n) |

*Average case; worst case may differ

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
