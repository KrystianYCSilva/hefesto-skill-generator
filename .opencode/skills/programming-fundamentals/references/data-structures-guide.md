# Data Structures Guide

Comprehensive guide to fundamental data structures with implementations, trade-offs, and use cases.

---

## Arrays

### Characteristics
- Contiguous memory allocation
- Fixed size (in most languages)
- O(1) random access by index
- O(n) insertion/deletion (requires shifting)

### Implementation Concepts
```pseudocode
Array:
  data: contiguous memory block
  size: integer
  
  access(index):
    if index < 0 or index >= size:
      throw IndexOutOfBounds
    return data[index]  // O(1)
  
  insert(index, value):
    if size == capacity:
      resize()  // O(n)
    shift_right(index)  // O(n)
    data[index] = value
  
  delete(index):
    shift_left(index)  // O(n)
    size--
```

### Dynamic Arrays (ArrayList/Vector)
```pseudocode
DynamicArray:
  data: array
  size: integer
  capacity: integer
  
  append(value):
    if size == capacity:
      new_capacity = capacity * 2
      new_data = allocate(new_capacity)
      copy(data, new_data)  // O(n) amortized O(1)
      data = new_data
      capacity = new_capacity
    data[size++] = value
  
  resize():
    // Amortized O(1) due to doubling strategy
    // Cost: n + n/2 + n/4 + ... = 2n → O(n)
```

### Use Cases
- Random access needed
- Size known in advance
- Cache-friendly traversal
- Matrix operations

### Trade-offs
| Operation | Array | Dynamic Array |
|-----------|-------|---------------|
| Access | O(1) | O(1) |
| Append | N/A | O(1) amortized |
| Insert | O(n) | O(n) |
| Delete | O(n) | O(n) |
| Space | O(n) | O(n) with overhead |

---

## Linked Lists

### Singly Linked List
```pseudocode
Node:
  data: value
  next: Node reference
  
LinkedList:
  head: Node
  tail: Node (optional)
  size: integer
  
  insert_head(value):
    new_node = Node(value)
    new_node.next = head
    head = new_node
    if tail == null:
      tail = new_node
    size++
  
  insert_tail(value):
    new_node = Node(value)
    if tail == null:
      head = tail = new_node
    else:
      tail.next = new_node
      tail = new_node
    size++
  
  delete(value):
    if head == null:
      return false
    
    if head.data == value:
      head = head.next
      size--
      return true
    
    current = head
    while current.next != null:
      if current.next.data == value:
        current.next = current.next.next
        if current.next == null:
          tail = current
        size--
        return true
      current = current.next
    return false
  
  search(value):
    current = head
    while current != null:
      if current.data == value:
        return current
      current = current.next
    return null  // O(n)
```

### Doubly Linked List
```pseudocode
DoublyNode:
  data: value
  next: DoublyNode reference
  prev: DoublyNode reference
  
DoublyLinkedList:
  head: DoublyNode
  tail: DoublyNode
  size: integer
  
  insert_after(node, value):
    new_node = DoublyNode(value)
    new_node.next = node.next
    new_node.prev = node
    
    if node.next != null:
      node.next.prev = new_node
    else:
      tail = new_node
    
    node.next = new_node
    size++
  
  delete_node(node):
    if node.prev != null:
      node.prev.next = node.next
    else:
      head = node.next
    
    if node.next != null:
      node.next.prev = node.prev
    else:
      tail = node.prev
    
    size--
```

### Circular Linked List
```pseudocode
CircularLinkedList:
  head: Node
  
  is_circular():
    if head == null:
      return false
    
    slow = fast = head
    while fast != null and fast.next != null:
      slow = slow.next
      fast = fast.next.next
      if slow == fast:
        return true
    return false
```

### Use Cases
- Frequent insertions/deletions at beginning
- Unknown size, dynamic growth
- Implementing queues, stacks
- Undo functionality

### Trade-offs
| Operation | Singly Linked | Doubly Linked |
|-----------|---------------|---------------|
| Access | O(n) | O(n) |
| Insert Head | O(1) | O(1) |
| Insert Tail | O(1)* | O(1) |
| Delete Head | O(1) | O(1) |
| Delete Tail | O(n) | O(1) |
| Delete Node | O(n) | O(1) if have reference |
| Space | O(n) | O(n) + extra pointers |

*With tail pointer

---

## Stacks

### LIFO (Last In, First Out)
```pseudocode
Stack:
  data: Array or LinkedList
  top: integer (for array) or Node (for list)
  
  push(value):
    if using_array:
      if top == capacity - 1:
        throw StackOverflow
      data[++top] = value
    else:
      new_node = Node(value)
      new_node.next = top
      top = new_node
  
  pop():
    if is_empty():
      throw StackUnderflow
    
    if using_array:
      return data[top--]
    else:
      value = top.data
      top = top.next
      return value
  
  peek():
    if is_empty():
      throw EmptyStack
    return top_element
  
  is_empty():
    return (top == -1) or (top == null)
```

### Use Cases
- Function call stack
- Expression evaluation (postfix, infix)
- Backtracking algorithms
- Undo mechanisms
- Browser history

### Example: Balanced Parentheses
```pseudocode
is_balanced(expression):
  stack = Stack()
  pairs = {')': '(', ']': '[', '}': '{'}
  
  for char in expression:
    if char in ['(', '[', '{']:
      stack.push(char)
    elif char in [')', ']', '}']:
      if stack.is_empty():
        return false
      if stack.pop() != pairs[char]:
        return false
  
  return stack.is_empty()
```

---

## Queues

### FIFO (First In, First Out)
```pseudocode
Queue:
  data: Array or LinkedList
  front: integer or Node
  rear: integer or Node
  size: integer
  
  enqueue(value):
    if using_array:
      if size == capacity:
        throw QueueOverflow
      rear = (rear + 1) % capacity  // Circular
      data[rear] = value
    else:
      new_node = Node(value)
      if rear == null:
        front = rear = new_node
      else:
        rear.next = new_node
        rear = new_node
    size++
  
  dequeue():
    if is_empty():
      throw QueueUnderflow
    
    value = data[front]
    if using_array:
      front = (front + 1) % capacity
    else:
      front = front.next
      if front == null:
        rear = null
    size--
    return value
  
  peek():
    if is_empty():
      throw EmptyQueue
    return data[front]
```

### Priority Queue
```pseudocode
PriorityQueue:
  heap: BinaryHeap
  
  enqueue(value, priority):
    heap.insert((priority, value))
  
  dequeue():
    return heap.extract_max()  // or extract_min
  
  peek():
    return heap.peek()
```

### Deque (Double-Ended Queue)
```pseudocode
Deque:
  data: DoublyLinkedList
  
  add_front(value):
    data.insert_head(value)
  
  add_rear(value):
    data.insert_tail(value)
  
  remove_front():
    return data.delete_head()
  
  remove_rear():
    return data.delete_tail()
```

### Use Cases
- BFS algorithms
- Task scheduling
- Event handling
- Request buffering
- Printer queue

---

## Trees

### Binary Tree
```pseudocode
TreeNode:
  data: value
  left: TreeNode
  right: TreeNode
  
BinaryTree:
  root: TreeNode
  
  insert(value):
    root = insert_recursive(root, value)
  
  insert_recursive(node, value):
    if node == null:
      return TreeNode(value)
    
    // BST insertion logic
    if value < node.data:
      node.left = insert_recursive(node.left, value)
    else:
      node.right = insert_recursive(node.right, value)
    
    return node
  
  search(value):
    return search_recursive(root, value)
  
  search_recursive(node, value):
    if node == null or node.data == value:
      return node
    
    if value < node.data:
      return search_recursive(node.left, value)
    else:
      return search_recursive(node.right, value)
```

### Tree Traversals
```pseudocode
preorder(node):
  if node == null:
    return
  visit(node)
  preorder(node.left)
  preorder(node.right)

inorder(node):
  if node == null:
    return
  inorder(node.left)
  visit(node)
  inorder(node.right)

postorder(node):
  if node == null:
    return
  postorder(node.left)
  postorder(node.right)
  visit(node)

level_order(root):
  if root == null:
    return
  
  queue = Queue()
  queue.enqueue(root)
  
  while not queue.is_empty():
    node = queue.dequeue()
    visit(node)
    
    if node.left != null:
      queue.enqueue(node.left)
    if node.right != null:
      queue.enqueue(node.right)
```

### Binary Search Tree (BST)
```pseudocode
BST:
  root: TreeNode
  
  delete(value):
    root = delete_recursive(root, value)
  
  delete_recursive(node, value):
    if node == null:
      return null
    
    if value < node.data:
      node.left = delete_recursive(node.left, value)
    elif value > node.data:
      node.right = delete_recursive(node.right, value)
    else:
      // Node to delete found
      
      // Case 1: No children
      if node.left == null and node.right == null:
        return null
      
      // Case 2: One child
      if node.left == null:
        return node.right
      if node.right == null:
        return node.left
      
      // Case 3: Two children
      successor = find_min(node.right)
      node.data = successor.data
      node.right = delete_recursive(node.right, successor.data)
    
    return node
  
  find_min(node):
    while node.left != null:
      node = node.left
    return node
```

### AVL Tree (Self-Balancing BST)
```pseudocode
AVLNode:
  data: value
  left: AVLNode
  right: AVLNode
  height: integer
  
AVLTree:
  root: AVLNode
  
  height(node):
    return node.height if node != null else -1
  
  balance_factor(node):
    return height(node.left) - height(node.right)
  
  update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))
  
  rotate_right(y):
    x = y.left
    T2 = x.right
    
    x.right = y
    y.left = T2
    
    update_height(y)
    update_height(x)
    
    return x
  
  rotate_left(x):
    y = x.right
    T2 = y.left
    
    y.left = x
    x.right = T2
    
    update_height(x)
    update_height(y)
    
    return y
  
  insert(node, value):
    if node == null:
      return AVLNode(value)
    
    if value < node.data:
      node.left = insert(node.left, value)
    else:
      node.right = insert(node.right, value)
    
    update_height(node)
    
    balance = balance_factor(node)
    
    // Left-Left case
    if balance > 1 and value < node.left.data:
      return rotate_right(node)
    
    // Right-Right case
    if balance < -1 and value > node.right.data:
      return rotate_left(node)
    
    // Left-Right case
    if balance > 1 and value > node.left.data:
      node.left = rotate_left(node.left)
      return rotate_right(node)
    
    // Right-Left case
    if balance < -1 and value < node.right.data:
      node.right = rotate_right(node.right)
      return rotate_left(node)
    
    return node
```

### Use Cases
- BST: Ordered data with O(log n) operations (when balanced)
- AVL: Frequent searches, less frequent insertions
- Hierarchical data (file systems, org charts)
- Expression parsing

---

## Heaps

### Binary Heap (Min-Heap)
```pseudocode
MinHeap:
  data: array
  size: integer
  
  parent(i):
    return (i - 1) / 2
  
  left_child(i):
    return 2 * i + 1
  
  right_child(i):
    return 2 * i + 2
  
  insert(value):
    data[size] = value
    size++
    heapify_up(size - 1)
  
  heapify_up(i):
    while i > 0 and data[i] < data[parent(i)]:
      swap(data[i], data[parent(i)])
      i = parent(i)
  
  extract_min():
    if size == 0:
      throw EmptyHeap
    
    min_value = data[0]
    data[0] = data[size - 1]
    size--
    heapify_down(0)
    
    return min_value
  
  heapify_down(i):
    while true:
      left = left_child(i)
      right = right_child(i)
      smallest = i
      
      if left < size and data[left] < data[smallest]:
        smallest = left
      
      if right < size and data[right] < data[smallest]:
        smallest = right
      
      if smallest == i:
        break
      
      swap(data[i], data[smallest])
      i = smallest
  
  peek():
    if size == 0:
      throw EmptyHeap
    return data[0]
  
  build_heap(array):
    data = array
    size = array.length
    
    // Start from last non-leaf node
    for i from (size / 2 - 1) down to 0:
      heapify_down(i)
```

### Use Cases
- Priority queues
- Heap sort
- Finding k largest/smallest elements
- Dijkstra's algorithm
- Huffman coding

---

## Hash Tables

### Hash Table with Chaining
```pseudocode
HashTable:
  buckets: array of LinkedLists
  capacity: integer
  size: integer
  load_factor: float = 0.75
  
  hash(key):
    // Simple hash function
    hash_value = 0
    for char in key:
      hash_value = (hash_value * 31 + char) % capacity
    return hash_value
  
  put(key, value):
    index = hash(key)
    bucket = buckets[index]
    
    // Update if key exists
    for node in bucket:
      if node.key == key:
        node.value = value
        return
    
    // Insert new key-value
    bucket.insert((key, value))
    size++
    
    if size / capacity > load_factor:
      resize()
  
  get(key):
    index = hash(key)
    bucket = buckets[index]
    
    for node in bucket:
      if node.key == key:
        return node.value
    
    return null
  
  remove(key):
    index = hash(key)
    bucket = buckets[index]
    
    for node in bucket:
      if node.key == key:
        bucket.remove(node)
        size--
        return true
    
    return false
  
  resize():
    old_buckets = buckets
    capacity = capacity * 2
    buckets = array of LinkedLists[capacity]
    size = 0
    
    for bucket in old_buckets:
      for node in bucket:
        put(node.key, node.value)
```

### Open Addressing (Linear Probing)
```pseudocode
OpenAddressingHashTable:
  keys: array
  values: array
  capacity: integer
  size: integer
  
  hash(key, i):
    return (hash(key) + i) % capacity
  
  put(key, value):
    for i from 0 to capacity - 1:
      index = hash(key, i)
      
      if keys[index] == null or keys[index] == DELETED:
        keys[index] = key
        values[index] = value
        size++
        return
      
      if keys[index] == key:
        values[index] = value
        return
    
    throw HashTableFull
  
  get(key):
    for i from 0 to capacity - 1:
      index = hash(key, i)
      
      if keys[index] == null:
        return null
      
      if keys[index] == key:
        return values[index]
    
    return null
  
  remove(key):
    for i from 0 to capacity - 1:
      index = hash(key, i)
      
      if keys[index] == null:
        return false
      
      if keys[index] == key:
        keys[index] = DELETED
        values[index] = null
        size--
        return true
    
    return false
```

### Use Cases
- Fast lookups O(1) average
- Caching
- Indexing
- Counting frequencies
- Detecting duplicates

---

## Graphs

### Graph Representations
```pseudocode
// Adjacency List
GraphAdjList:
  vertices: integer
  adj_list: array of LinkedLists
  
  add_edge(u, v):
    adj_list[u].append(v)
    // If undirected:
    adj_list[v].append(u)
  
  get_neighbors(u):
    return adj_list[u]

// Adjacency Matrix
GraphAdjMatrix:
  vertices: integer
  matrix: 2D array[vertices][vertices]
  
  add_edge(u, v, weight=1):
    matrix[u][v] = weight
    // If undirected:
    matrix[v][u] = weight
  
  has_edge(u, v):
    return matrix[u][v] != 0
```

### Depth-First Search (DFS)
```pseudocode
dfs(graph, start):
  visited = set()
  stack = Stack()
  stack.push(start)
  
  while not stack.is_empty():
    vertex = stack.pop()
    
    if vertex not in visited:
      visit(vertex)
      visited.add(vertex)
      
      for neighbor in graph.get_neighbors(vertex):
        if neighbor not in visited:
          stack.push(neighbor)

dfs_recursive(graph, vertex, visited):
  visited.add(vertex)
  visit(vertex)
  
  for neighbor in graph.get_neighbors(vertex):
    if neighbor not in visited:
      dfs_recursive(graph, neighbor, visited)
```

### Breadth-First Search (BFS)
```pseudocode
bfs(graph, start):
  visited = set()
  queue = Queue()
  queue.enqueue(start)
  visited.add(start)
  
  while not queue.is_empty():
    vertex = queue.dequeue()
    visit(vertex)
    
    for neighbor in graph.get_neighbors(vertex):
      if neighbor not in visited:
        visited.add(neighbor)
        queue.enqueue(neighbor)
```

### Use Cases
- Social networks
- Route finding
- Dependency resolution
- Network topology
- State machines

---

## Comparison Summary

| Data Structure | Access | Search | Insert | Delete | Space |
|----------------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1)* | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table | N/A | O(1)† | O(1)† | O(1)† | O(n) |
| BST | O(log n)‡ | O(log n)‡ | O(log n)‡ | O(log n)‡ | O(n) |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Binary Heap | O(log n) | O(n) | O(log n) | O(log n) | O(n) |

*With reference to node
†Average case; O(n) worst case
‡Balanced tree; O(n) worst case

---

## Choosing the Right Data Structure

**Need fast random access?** → Array

**Frequent insertions/deletions at ends?** → Linked List, Deque

**LIFO operations?** → Stack

**FIFO operations?** → Queue

**Fast lookup by key?** → Hash Table

**Sorted data with fast operations?** → BST, AVL Tree

**Priority-based access?** → Heap

**Relationships between entities?** → Graph

**Hierarchical data?** → Tree
