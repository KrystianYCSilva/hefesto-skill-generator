# Advanced Programming Techniques

## Overview

Advanced programming techniques optimize performance, reduce memory usage, and solve complex problems elegantly. This guide covers memoization, lazy evaluation, tail recursion, bit manipulation, and algorithmic optimization strategies.

## Memoization

### Definition

Memoization is an optimization technique that stores the results of expensive function calls and returns the cached result when the same inputs occur again.

### Basic Implementation

```pseudo
cache = {}

function memoizedFunction(n):
    if n in cache:
        return cache[n]
    
    result = expensiveComputation(n)
    cache[n] = result
    return result
```

### Fibonacci Example

**Without Memoization (Exponential Time: O(2^n)):**

```pseudo
function fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(40) → ~2 billion recursive calls
```

**With Memoization (Linear Time: O(n)):**

```pseudo
fibCache = {}

function fibonacci(n):
    if n in fibCache:
        return fibCache[n]
    
    if n <= 1:
        return n
    
    result = fibonacci(n - 1) + fibonacci(n - 2)
    fibCache[n] = result
    return result

fibonacci(40) → 40 recursive calls
```

### Automatic Memoization (Decorator Pattern)

```pseudo
function memoize(func):
    cache = {}
    
    function memoized(args...):
        key = serializeArgs(args)
        
        if key in cache:
            return cache[key]
        
        result = func(args...)
        cache[key] = result
        return result
    
    return memoized

fibonacci = memoize(function(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
)
```

### Advanced Memoization: LRU Cache

```pseudo
class LRUCache:
    capacity, cache, order
    
    function constructor(capacity):
        this.capacity = capacity
        this.cache = {}
        this.order = []
    
    function get(key):
        if key not in this.cache:
            return null
        
        this.moveToFront(key)
        return this.cache[key]
    
    function put(key, value):
        if key in this.cache:
            this.moveToFront(key)
        else:
            if this.order.length >= this.capacity:
                oldest = this.order.removeLast()
                delete this.cache[oldest]
            this.order.addFirst(key)
        
        this.cache[key] = value
    
    function moveToFront(key):
        this.order.remove(key)
        this.order.addFirst(key)

memoizedWithLRU = memoize(expensiveFunction, capacity=100)
```

### Practical Examples

**Example 1: Expensive API Calls**

```pseudo
apiCache = {}

function fetchUserData(userId):
    if userId in apiCache:
        return apiCache[userId]
    
    data = httpGet("/api/users/" + userId)
    apiCache[userId] = data
    return data
```

**Example 2: Dynamic Programming (Longest Common Subsequence)**

```pseudo
memo = {}

function lcs(str1, str2, i, j):
    key = i + "," + j
    
    if key in memo:
        return memo[key]
    
    if i == 0 or j == 0:
        return 0
    
    if str1[i-1] == str2[j-1]:
        result = 1 + lcs(str1, str2, i-1, j-1)
    else:
        result = max(lcs(str1, str2, i-1, j), lcs(str1, str2, i, j-1))
    
    memo[key] = result
    return result
```

## Lazy Evaluation

### Definition

Lazy evaluation delays computation until the result is actually needed, improving performance by avoiding unnecessary calculations.

### Generator Functions

```pseudo
function range(start, end):
    current = start
    while current < end:
        yield current
        current += 1

for num in range(0, 1000000):
    if num > 10:
        break
```

### Lazy Sequences

```pseudo
class LazySequence:
    generator
    
    function constructor(generator):
        this.generator = generator
    
    function map(func):
        return new LazySequence(function():
            for item in this.generator():
                yield func(item)
        )
    
    function filter(predicate):
        return new LazySequence(function():
            for item in this.generator():
                if predicate(item):
                    yield item
        )
    
    function take(n):
        result = []
        count = 0
        for item in this.generator():
            if count >= n:
                break
            result.append(item)
            count += 1
        return result

numbers = new LazySequence(() => range(0, 1000000))
    .filter(x => x % 2 == 0)
    .map(x => x * x)
    .take(10)
```

### Lazy Properties

```pseudo
class DataProcessor:
    rawData
    processedDataCache
    
    function get processedData():
        if this.processedDataCache is null:
            this.processedDataCache = this.expensiveProcessing(this.rawData)
        return this.processedDataCache
    
    function expensiveProcessing(data):
        ...
```

### Stream Processing

```pseudo
function processLargeFile(filename):
    file = openFile(filename)
    
    for line in file.readLines():
        if shouldProcess(line):
            yield processLine(line)
    
    file.close()

for result in processLargeFile("huge.txt"):
    handleResult(result)
```

## Tail Recursion Optimization

### Definition

Tail recursion occurs when the recursive call is the last operation in the function. Many languages can optimize this to iteration, preventing stack overflow.

### Tail Recursive vs Non-Tail Recursive

**Non-Tail Recursive (Stack builds up):**

```pseudo
function factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(5):
  5 * factorial(4)
  5 * (4 * factorial(3))
  5 * (4 * (3 * factorial(2)))
  5 * (4 * (3 * (2 * factorial(1))))
  5 * (4 * (3 * (2 * 1)))
  ...
```

**Tail Recursive (Can be optimized to iteration):**

```pseudo
function factorial(n, accumulator = 1):
    if n <= 1:
        return accumulator
    return factorial(n - 1, n * accumulator)

factorial(5, 1):
  factorial(4, 5)
  factorial(3, 20)
  factorial(2, 60)
  factorial(1, 120)
  120
```

### Converting to Tail Recursion

**Original:**

```pseudo
function sum(list):
    if list.isEmpty():
        return 0
    return list.first() + sum(list.rest())
```

**Tail Recursive:**

```pseudo
function sum(list, accumulator = 0):
    if list.isEmpty():
        return accumulator
    return sum(list.rest(), accumulator + list.first())
```

### Manual Conversion to Iteration

```pseudo
function factorial(n):
    accumulator = 1
    while n > 1:
        accumulator = accumulator * n
        n = n - 1
    return accumulator
```

### Trampoline Pattern (Simulating TCO)

```pseudo
function trampoline(func):
    result = func
    while isFunction(result):
        result = result()
    return result

function factorial(n, acc = 1):
    if n <= 1:
        return acc
    return () => factorial(n - 1, n * acc)

result = trampoline(factorial(5))
```

## Bit Manipulation

### Basic Operations

```pseudo
AND:  a & b   (both bits are 1)
OR:   a | b   (at least one bit is 1)
XOR:  a ^ b   (bits are different)
NOT:  ~a      (flip all bits)
Left shift:  a << n  (multiply by 2^n)
Right shift: a >> n  (divide by 2^n)
```

### Common Techniques

**Check if even/odd:**

```pseudo
function isEven(n):
    return (n & 1) == 0

function isOdd(n):
    return (n & 1) == 1
```

**Multiply/Divide by powers of 2:**

```pseudo
function multiplyBy8(n):
    return n << 3

function divideBy4(n):
    return n >> 2
```

**Check if power of 2:**

```pseudo
function isPowerOfTwo(n):
    return n > 0 && (n & (n - 1)) == 0

Examples:
8 = 1000, 7 = 0111, 8 & 7 = 0000
6 = 0110, 5 = 0101, 6 & 5 = 0100 (not power of 2)
```

**Count set bits (Hamming weight):**

```pseudo
function countSetBits(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count

function countSetBitsFast(n):
    count = 0
    while n > 0:
        n &= (n - 1)
        count += 1
    return count
```

**Swap two numbers without temporary variable:**

```pseudo
function swap(a, b):
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b
```

**Get/Set/Clear/Toggle bit:**

```pseudo
function getBit(num, i):
    return (num & (1 << i)) != 0

function setBit(num, i):
    return num | (1 << i)

function clearBit(num, i):
    return num & ~(1 << i)

function toggleBit(num, i):
    return num ^ (1 << i)
```

### Bit Flags

```pseudo
READ_PERMISSION = 1    # 001
WRITE_PERMISSION = 2   # 010
EXECUTE_PERMISSION = 4 # 100

function hasPermission(permissions, flag):
    return (permissions & flag) != 0

function addPermission(permissions, flag):
    return permissions | flag

function removePermission(permissions, flag):
    return permissions & ~flag

user_permissions = READ_PERMISSION | WRITE_PERMISSION

if hasPermission(user_permissions, READ_PERMISSION):
    allowRead()
```

### Bit Masks

```pseudo
function extractRed(rgb):
    return (rgb >> 16) & 0xFF

function extractGreen(rgb):
    return (rgb >> 8) & 0xFF

function extractBlue(rgb):
    return rgb & 0xFF

function createRGB(r, g, b):
    return (r << 16) | (g << 8) | b

color = createRGB(255, 128, 64)
red = extractRed(color)
```

### XOR Tricks

**Find single non-duplicate:**

```pseudo
function findSingle(array):
    result = 0
    for num in array:
        result ^= num
    return result

[4, 2, 4, 5, 2] → 5
```

**Swap array elements:**

```pseudo
function swapElements(array, i, j):
    if i != j:
        array[i] ^= array[j]
        array[j] ^= array[i]
        array[i] ^= array[j]
```

## Space-Time Trade-offs

### Hash Tables for Fast Lookup

**Time-Optimized (O(1) lookup, O(n) space):**

```pseudo
function twoSum(array, target):
    seen = {}
    
    for i, num in enumerate(array):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return null
```

**Space-Optimized (O(n^2) time, O(1) space):**

```pseudo
function twoSum(array, target):
    for i in range(array.length):
        for j in range(i + 1, array.length):
            if array[i] + array[j] == target:
                return [i, j]
    return null
```

### Prefix Sum Arrays

**Naive Range Sum (O(n) per query):**

```pseudo
function rangeSum(array, left, right):
    sum = 0
    for i in range(left, right + 1):
        sum += array[i]
    return sum
```

**Optimized with Prefix Sum (O(1) per query, O(n) space):**

```pseudo
function buildPrefixSum(array):
    prefix = [0]
    for num in array:
        prefix.append(prefix[prefix.length - 1] + num)
    return prefix

function rangeSum(prefix, left, right):
    return prefix[right + 1] - prefix[left]

prefix = buildPrefixSum([1, 2, 3, 4, 5])
rangeSum(prefix, 1, 3) → 9
```

## Cache-Friendly Algorithms

### Array Traversal Patterns

**Cache-Friendly (Row-major order):**

```pseudo
for i in range(rows):
    for j in range(cols):
        process(matrix[i][j])
```

**Cache-Unfriendly (Column-major order for row-major storage):**

```pseudo
for j in range(cols):
    for i in range(rows):
        process(matrix[i][j])
```

### Data Structure Alignment

```pseudo
struct CacheFriendly:
    int a, b, c, d
    
    function process():
        return a + b + c + d

struct CacheUnfriendly:
    int a
    char padding1[60]
    int b
    char padding2[60]
    int c
    char padding3[60]
    int d
    
    function process():
        return a + b + c + d
```

### Blocking/Tiling

```pseudo
function matrixMultiply(A, B, C, n, blockSize):
    for i in range(0, n, blockSize):
        for j in range(0, n, blockSize):
            for k in range(0, n, blockSize):
                for ii in range(i, min(i + blockSize, n)):
                    for jj in range(j, min(j + blockSize, n)):
                        for kk in range(k, min(k + blockSize, n)):
                            C[ii][jj] += A[ii][kk] * B[kk][jj]
```

## SIMD Considerations

### Vectorization

**Scalar Processing:**

```pseudo
function addArrays(a, b, result, n):
    for i in range(n):
        result[i] = a[i] + b[i]
```

**Vectorized Processing (4 elements at once):**

```pseudo
function addArraysVectorized(a, b, result, n):
    i = 0
    while i + 4 <= n:
        result[i:i+4] = a[i:i+4] + b[i:i+4]
        i += 4
    
    while i < n:
        result[i] = a[i] + b[i]
        i += 1
```

### Data Alignment

```pseudo
aligned_data = allocateAligned(size, 16)
```

## Advanced Recursion Patterns

### Divide and Conquer

```pseudo
function mergeSort(array):
    if array.length <= 1:
        return array
    
    mid = array.length / 2
    left = mergeSort(array[0:mid])
    right = mergeSort(array[mid:])
    
    return merge(left, right)

function merge(left, right):
    result = []
    i = 0, j = 0
    
    while i < left.length && j < right.length:
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### Backtracking

```pseudo
function solveNQueens(n):
    board = createBoard(n)
    solutions = []
    
    function backtrack(row):
        if row == n:
            solutions.append(copyBoard(board))
            return
        
        for col in range(n):
            if isSafe(board, row, col):
                placeQueen(board, row, col)
                backtrack(row + 1)
                removeQueen(board, row, col)
    
    backtrack(0)
    return solutions
```

## Summary

Advanced techniques optimize code performance and solve complex problems efficiently:

- **Memoization**: Cache expensive computations (O(2^n) → O(n))
- **Lazy Evaluation**: Compute only what's needed
- **Tail Recursion**: Convert recursion to iteration
- **Bit Manipulation**: Fast, space-efficient operations
- **Space-Time Trade-offs**: Balance memory and speed
- **Cache-Friendly Algorithms**: Optimize memory access patterns
- **SIMD**: Process multiple data points simultaneously

Choose techniques based on specific performance requirements and constraints.
