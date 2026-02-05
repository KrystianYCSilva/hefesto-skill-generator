# Algorithms Fundamentals

Comprehensive guide to fundamental algorithms including sorting, searching, and algorithm design techniques.

---

## Sorting Algorithms

### Bubble Sort
```pseudocode
bubble_sort(array):
  n = array.length
  
  for i from 0 to n - 1:
    swapped = false
    
    for j from 0 to n - i - 2:
      if array[j] > array[j + 1]:
        swap(array[j], array[j + 1])
        swapped = true
    
    if not swapped:
      break  // Already sorted
```

**Time Complexity:**
- Best: O(n) - already sorted
- Average: O(n²)
- Worst: O(n²)

**Space Complexity:** O(1)

**Stable:** Yes

**Use Case:** Educational purposes, nearly sorted data

---

### Selection Sort
```pseudocode
selection_sort(array):
  n = array.length
  
  for i from 0 to n - 2:
    min_index = i
    
    for j from i + 1 to n - 1:
      if array[j] < array[min_index]:
        min_index = j
    
    if min_index != i:
      swap(array[i], array[min_index])
```

**Time Complexity:**
- Best/Average/Worst: O(n²)

**Space Complexity:** O(1)

**Stable:** No

**Use Case:** Small arrays, memory constraints

---

### Insertion Sort
```pseudocode
insertion_sort(array):
  n = array.length
  
  for i from 1 to n - 1:
    key = array[i]
    j = i - 1
    
    while j >= 0 and array[j] > key:
      array[j + 1] = array[j]
      j--
    
    array[j + 1] = key
```

**Time Complexity:**
- Best: O(n) - already sorted
- Average: O(n²)
- Worst: O(n²)

**Space Complexity:** O(1)

**Stable:** Yes

**Use Case:** Small arrays, nearly sorted data, online sorting

---

### Merge Sort
```pseudocode
merge_sort(array, left, right):
  if left < right:
    mid = (left + right) / 2
    
    merge_sort(array, left, mid)
    merge_sort(array, mid + 1, right)
    merge(array, left, mid, right)

merge(array, left, mid, right):
  n1 = mid - left + 1
  n2 = right - mid
  
  left_array = copy(array[left..mid])
  right_array = copy(array[mid+1..right])
  
  i = 0, j = 0, k = left
  
  while i < n1 and j < n2:
    if left_array[i] <= right_array[j]:
      array[k] = left_array[i]
      i++
    else:
      array[k] = right_array[j]
      j++
    k++
  
  while i < n1:
    array[k++] = left_array[i++]
  
  while j < n2:
    array[k++] = right_array[j++]
```

**Time Complexity:**
- Best/Average/Worst: O(n log n)

**Space Complexity:** O(n)

**Stable:** Yes

**Use Case:** Large datasets, linked lists, guaranteed O(n log n)

---

### Quick Sort
```pseudocode
quick_sort(array, low, high):
  if low < high:
    pivot_index = partition(array, low, high)
    
    quick_sort(array, low, pivot_index - 1)
    quick_sort(array, pivot_index + 1, high)

partition(array, low, high):
  pivot = array[high]
  i = low - 1
  
  for j from low to high - 1:
    if array[j] < pivot:
      i++
      swap(array[i], array[j])
  
  swap(array[i + 1], array[high])
  return i + 1

// Optimized: Random pivot
partition_random(array, low, high):
  random_index = random(low, high)
  swap(array[random_index], array[high])
  return partition(array, low, high)
```

**Time Complexity:**
- Best: O(n log n)
- Average: O(n log n)
- Worst: O(n²) - already sorted with bad pivot

**Space Complexity:** O(log n) - recursion stack

**Stable:** No

**Use Case:** General purpose, in-place sorting, cache-friendly

**Optimization:** Use median-of-three for pivot selection

---

### Heap Sort
```pseudocode
heap_sort(array):
  n = array.length
  
  // Build max heap
  for i from n/2 - 1 down to 0:
    heapify(array, n, i)
  
  // Extract elements from heap
  for i from n - 1 down to 1:
    swap(array[0], array[i])
    heapify(array, i, 0)

heapify(array, n, i):
  largest = i
  left = 2 * i + 1
  right = 2 * i + 2
  
  if left < n and array[left] > array[largest]:
    largest = left
  
  if right < n and array[right] > array[largest]:
    largest = right
  
  if largest != i:
    swap(array[i], array[largest])
    heapify(array, n, largest)
```

**Time Complexity:**
- Best/Average/Worst: O(n log n)

**Space Complexity:** O(1)

**Stable:** No

**Use Case:** Memory constraints, guaranteed O(n log n)

---

### Counting Sort
```pseudocode
counting_sort(array, max_value):
  n = array.length
  count = new array[max_value + 1] initialized to 0
  output = new array[n]
  
  // Count occurrences
  for i from 0 to n - 1:
    count[array[i]]++
  
  // Cumulative count
  for i from 1 to max_value:
    count[i] += count[i - 1]
  
  // Build output array
  for i from n - 1 down to 0:
    output[count[array[i]] - 1] = array[i]
    count[array[i]]--
  
  copy(output, array)
```

**Time Complexity:** O(n + k) where k is range

**Space Complexity:** O(k)

**Stable:** Yes

**Use Case:** Integer sorting with limited range

---

### Radix Sort
```pseudocode
radix_sort(array):
  max_value = find_max(array)
  
  exp = 1
  while max_value / exp > 0:
    counting_sort_by_digit(array, exp)
    exp *= 10

counting_sort_by_digit(array, exp):
  n = array.length
  output = new array[n]
  count = new array[10] initialized to 0
  
  for i from 0 to n - 1:
    digit = (array[i] / exp) % 10
    count[digit]++
  
  for i from 1 to 9:
    count[i] += count[i - 1]
  
  for i from n - 1 down to 0:
    digit = (array[i] / exp) % 10
    output[count[digit] - 1] = array[i]
    count[digit]--
  
  copy(output, array)
```

**Time Complexity:** O(d * (n + k)) where d is number of digits

**Space Complexity:** O(n + k)

**Stable:** Yes

**Use Case:** Large integers with limited digits

---

## Searching Algorithms

### Linear Search
```pseudocode
linear_search(array, target):
  for i from 0 to array.length - 1:
    if array[i] == target:
      return i
  return -1
```

**Time Complexity:** O(n)

**Space Complexity:** O(1)

**Use Case:** Unsorted data, small datasets

---

### Binary Search
```pseudocode
binary_search(array, target):
  left = 0
  right = array.length - 1
  
  while left <= right:
    mid = left + (right - left) / 2
    
    if array[mid] == target:
      return mid
    elif array[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  
  return -1

// Recursive version
binary_search_recursive(array, target, left, right):
  if left > right:
    return -1
  
  mid = left + (right - left) / 2
  
  if array[mid] == target:
    return mid
  elif array[mid] < target:
    return binary_search_recursive(array, target, mid + 1, right)
  else:
    return binary_search_recursive(array, target, left, mid - 1)
```

**Time Complexity:** O(log n)

**Space Complexity:** O(1) iterative, O(log n) recursive

**Requirement:** Sorted array

**Use Case:** Fast search in sorted data

---

### Binary Search Variants

#### Find First Occurrence
```pseudocode
find_first(array, target):
  left = 0
  right = array.length - 1
  result = -1
  
  while left <= right:
    mid = left + (right - left) / 2
    
    if array[mid] == target:
      result = mid
      right = mid - 1  // Continue searching left
    elif array[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  
  return result
```

#### Find Last Occurrence
```pseudocode
find_last(array, target):
  left = 0
  right = array.length - 1
  result = -1
  
  while left <= right:
    mid = left + (right - left) / 2
    
    if array[mid] == target:
      result = mid
      left = mid + 1  // Continue searching right
    elif array[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  
  return result
```

#### Find Insert Position
```pseudocode
find_insert_position(array, target):
  left = 0
  right = array.length
  
  while left < right:
    mid = left + (right - left) / 2
    
    if array[mid] < target:
      left = mid + 1
    else:
      right = mid
  
  return left
```

---

### Jump Search
```pseudocode
jump_search(array, target):
  n = array.length
  step = sqrt(n)
  prev = 0
  
  while array[min(step, n) - 1] < target:
    prev = step
    step += sqrt(n)
    
    if prev >= n:
      return -1
  
  while array[prev] < target:
    prev++
    
    if prev == min(step, n):
      return -1
  
  if array[prev] == target:
    return prev
  
  return -1
```

**Time Complexity:** O(√n)

**Space Complexity:** O(1)

**Requirement:** Sorted array

**Use Case:** Alternative to binary search on sorted data

---

### Interpolation Search
```pseudocode
interpolation_search(array, target):
  left = 0
  right = array.length - 1
  
  while left <= right and target >= array[left] and target <= array[right]:
    if left == right:
      if array[left] == target:
        return left
      return -1
    
    // Interpolation formula
    pos = left + ((target - array[left]) * (right - left)) / 
                  (array[right] - array[left])
    
    if array[pos] == target:
      return pos
    elif array[pos] < target:
      left = pos + 1
    else:
      right = pos - 1
  
  return -1
```

**Time Complexity:** O(log log n) average, O(n) worst

**Space Complexity:** O(1)

**Requirement:** Sorted, uniformly distributed data

**Use Case:** Large sorted datasets with uniform distribution

---

## Divide and Conquer

### General Template
```pseudocode
divide_and_conquer(problem):
  if problem is small enough:
    solve directly
  else:
    divide problem into subproblems
    
    for each subproblem:
      solution = divide_and_conquer(subproblem)
    
    combine solutions
    return combined solution
```

### Maximum Subarray (Kadane's Algorithm)
```pseudocode
max_subarray(array):
  max_so_far = array[0]
  max_ending_here = array[0]
  
  for i from 1 to array.length - 1:
    max_ending_here = max(array[i], max_ending_here + array[i])
    max_so_far = max(max_so_far, max_ending_here)
  
  return max_so_far
```

**Time Complexity:** O(n)

**Space Complexity:** O(1)

---

### Closest Pair of Points
```pseudocode
closest_pair(points):
  points_x = sort points by x-coordinate
  points_y = sort points by y-coordinate
  
  return closest_pair_recursive(points_x, points_y)

closest_pair_recursive(px, py):
  n = px.length
  
  if n <= 3:
    return brute_force(px)
  
  mid = n / 2
  midpoint = px[mid]
  
  pyl = py points where x <= midpoint.x
  pyr = py points where x > midpoint.x
  
  dl = closest_pair_recursive(px[0..mid], pyl)
  dr = closest_pair_recursive(px[mid+1..n], pyr)
  
  d = min(dl, dr)
  
  strip = py points where abs(x - midpoint.x) < d
  
  return min(d, strip_closest(strip, d))

strip_closest(strip, d):
  min_dist = d
  
  for i from 0 to strip.length - 1:
    j = i + 1
    while j < strip.length and (strip[j].y - strip[i].y) < min_dist:
      min_dist = min(min_dist, distance(strip[i], strip[j]))
      j++
  
  return min_dist
```

**Time Complexity:** O(n log n)

**Space Complexity:** O(n)

---

## Dynamic Programming

### General Approach
1. Define subproblems
2. Write recurrence relation
3. Identify base cases
4. Decide bottom-up or top-down
5. Optimize space if possible

### Fibonacci (Bottom-Up)
```pseudocode
fibonacci(n):
  if n <= 1:
    return n
  
  dp = new array[n + 1]
  dp[0] = 0
  dp[1] = 1
  
  for i from 2 to n:
    dp[i] = dp[i - 1] + dp[i - 2]
  
  return dp[n]

// Space optimized
fibonacci_optimized(n):
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

**Time Complexity:** O(n)

**Space Complexity:** O(1) optimized

---

### Longest Common Subsequence
```pseudocode
lcs(str1, str2):
  m = str1.length
  n = str2.length
  dp = new array[m + 1][n + 1]
  
  for i from 0 to m:
    for j from 0 to n:
      if i == 0 or j == 0:
        dp[i][j] = 0
      elif str1[i - 1] == str2[j - 1]:
        dp[i][j] = dp[i - 1][j - 1] + 1
      else:
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
  
  return dp[m][n]

// Reconstruct LCS
reconstruct_lcs(str1, str2, dp):
  i = str1.length
  j = str2.length
  lcs = ""
  
  while i > 0 and j > 0:
    if str1[i - 1] == str2[j - 1]:
      lcs = str1[i - 1] + lcs
      i--
      j--
    elif dp[i - 1][j] > dp[i][j - 1]:
      i--
    else:
      j--
  
  return lcs
```

**Time Complexity:** O(m * n)

**Space Complexity:** O(m * n), can be optimized to O(min(m, n))

---

### 0/1 Knapsack
```pseudocode
knapsack(weights, values, capacity):
  n = weights.length
  dp = new array[n + 1][capacity + 1]
  
  for i from 0 to n:
    for w from 0 to capacity:
      if i == 0 or w == 0:
        dp[i][w] = 0
      elif weights[i - 1] <= w:
        dp[i][w] = max(
          values[i - 1] + dp[i - 1][w - weights[i - 1]],
          dp[i - 1][w]
        )
      else:
        dp[i][w] = dp[i - 1][w]
  
  return dp[n][capacity]
```

**Time Complexity:** O(n * W) where W is capacity

**Space Complexity:** O(n * W), can be optimized to O(W)

---

### Longest Increasing Subsequence
```pseudocode
lis(array):
  n = array.length
  dp = new array[n] initialized to 1
  
  for i from 1 to n - 1:
    for j from 0 to i - 1:
      if array[j] < array[i]:
        dp[i] = max(dp[i], dp[j] + 1)
  
  return max(dp)

// O(n log n) solution with binary search
lis_optimized(array):
  n = array.length
  tails = new array[n]
  length = 0
  
  for num in array:
    pos = binary_search_insert_position(tails, 0, length, num)
    tails[pos] = num
    
    if pos == length:
      length++
  
  return length
```

**Time Complexity:** O(n²) or O(n log n) optimized

**Space Complexity:** O(n)

---

## Greedy Algorithms

### Activity Selection
```pseudocode
activity_selection(start, finish):
  n = start.length
  activities = sort by finish time
  
  selected = [activities[0]]
  last_finish = activities[0].finish
  
  for i from 1 to n - 1:
    if activities[i].start >= last_finish:
      selected.append(activities[i])
      last_finish = activities[i].finish
  
  return selected
```

**Time Complexity:** O(n log n)

**Space Complexity:** O(n)

---

### Huffman Coding
```pseudocode
huffman_coding(frequencies):
  heap = MinHeap()
  
  for char, freq in frequencies:
    heap.insert(Node(char, freq))
  
  while heap.size() > 1:
    left = heap.extract_min()
    right = heap.extract_min()
    
    merged = Node(null, left.freq + right.freq)
    merged.left = left
    merged.right = right
    
    heap.insert(merged)
  
  root = heap.extract_min()
  codes = {}
  generate_codes(root, "", codes)
  
  return codes

generate_codes(node, code, codes):
  if node is leaf:
    codes[node.char] = code
    return
  
  generate_codes(node.left, code + "0", codes)
  generate_codes(node.right, code + "1", codes)
```

**Time Complexity:** O(n log n)

**Space Complexity:** O(n)

---

### Dijkstra's Shortest Path
```pseudocode
dijkstra(graph, source):
  distances = array initialized to infinity
  distances[source] = 0
  visited = set()
  pq = PriorityQueue()
  
  pq.enqueue((0, source))
  
  while not pq.is_empty():
    current_dist, u = pq.dequeue()
    
    if u in visited:
      continue
    
    visited.add(u)
    
    for v, weight in graph.neighbors(u):
      new_dist = distances[u] + weight
      
      if new_dist < distances[v]:
        distances[v] = new_dist
        pq.enqueue((new_dist, v))
  
  return distances
```

**Time Complexity:** O((V + E) log V) with binary heap

**Space Complexity:** O(V)

---

## Backtracking

### General Template
```pseudocode
backtrack(state):
  if is_solution(state):
    process_solution(state)
    return
  
  for choice in get_choices(state):
    if is_valid(choice):
      make_choice(choice)
      backtrack(state)
      unmake_choice(choice)
```

### N-Queens
```pseudocode
solve_n_queens(n):
  board = new array[n][n]
  solutions = []
  
  solve_n_queens_recursive(board, 0, solutions)
  
  return solutions

solve_n_queens_recursive(board, row, solutions):
  if row == board.length:
    solutions.append(copy(board))
    return
  
  for col from 0 to board.length - 1:
    if is_safe(board, row, col):
      board[row][col] = 'Q'
      solve_n_queens_recursive(board, row + 1, solutions)
      board[row][col] = '.'

is_safe(board, row, col):
  // Check column
  for i from 0 to row - 1:
    if board[i][col] == 'Q':
      return false
  
  // Check upper-left diagonal
  i = row - 1
  j = col - 1
  while i >= 0 and j >= 0:
    if board[i][j] == 'Q':
      return false
    i--
    j--
  
  // Check upper-right diagonal
  i = row - 1
  j = col + 1
  while i >= 0 and j < board.length:
    if board[i][j] == 'Q':
      return false
    i--
    j++
  
  return true
```

**Time Complexity:** O(N!)

**Space Complexity:** O(N²)

---

### Subset Sum
```pseudocode
subset_sum(numbers, target):
  solutions = []
  current = []
  
  subset_sum_recursive(numbers, target, 0, current, solutions)
  
  return solutions

subset_sum_recursive(numbers, target, start, current, solutions):
  if target == 0:
    solutions.append(copy(current))
    return
  
  if target < 0:
    return
  
  for i from start to numbers.length - 1:
    current.append(numbers[i])
    subset_sum_recursive(numbers, target - numbers[i], i + 1, current, solutions)
    current.remove_last()
```

**Time Complexity:** O(2ⁿ)

**Space Complexity:** O(n)

---

## Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Radix Sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes |

---

## Choosing the Right Algorithm

**Small data (n < 50)?** → Insertion Sort

**Nearly sorted?** → Insertion Sort, Bubble Sort

**Guaranteed O(n log n)?** → Merge Sort, Heap Sort

**In-place sorting?** → Quick Sort, Heap Sort

**Stable sorting?** → Merge Sort, Counting Sort

**Integer range limited?** → Counting Sort, Radix Sort

**Search in sorted data?** → Binary Search

**Shortest path?** → Dijkstra (non-negative), Bellman-Ford (negative)

**Optimal substructure?** → Dynamic Programming

**Greedy choice property?** → Greedy Algorithm

**Explore all solutions?** → Backtracking
