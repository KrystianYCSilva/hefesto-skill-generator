---
name: programming-fundamentals
description: |
  Skill para aplicação de fundamentos sólidos de programação, algoritmos, 
  estruturas de dados, paradigmas e boas práticas de código.
  Use quando: projetar algoritmos, escolher estruturas de dados, analisar 
  complexidade, aplicar paradigmas (OO, funcional, estrutural), seguir 
  SOLID/Clean Code, refatorar código, evitar anti-patterns.
license: MIT
metadata: ./metadata.yaml
---

# Programming Fundamentals

Skill para aplicação de fundamentos sólidos de programação, algoritmos, estruturas de dados, paradigmas e boas práticas de código - agnóstico de linguagem.

---

## When to Use

Use esta skill quando precisar:

- **Projetar algoritmos** eficientes para resolver problemas
- **Escolher estruturas de dados** adequadas (lista, pilha, fila, árvore, grafo, hash)
- **Analisar complexidade** de algoritmos (Big O notation)
- **Aplicar paradigmas** (Orientado a Objetos, Funcional, Estruturado)
- **Seguir boas práticas** (SOLID, Clean Code, DRY, KISS, YAGNI)
- **Refatorar código** para melhor legibilidade e manutenibilidade
- **Evitar code smells** e anti-patterns
- **Aplicar design patterns** clássicos (GoF)
- **Reduzir complexidade ciclomática** de código complexo

**Não use para**: Linguagem específica (use java-fundamentals, kotlin-fundamentals, etc.), frameworks, deployment, infraestrutura.

---

## Instructions

### Step 1: Analisar o Problema

Antes de implementar solução:

1. **Entender requisitos**
   - Quais são as entradas e saídas esperadas?
   - Quais restrições existem (tempo, memória, precisão)?
   - Quais casos extremos devem ser tratados?

2. **Definir complexidade alvo**
   - Qual volume de dados esperado? (n < 100, n < 10^6, n < 10^9?)
   - Tempo de resposta aceitável? (ms, segundos, minutos?)
   - Recursos disponíveis? (memória limitada, CPU multi-core?)

3. **Escolher abordagem**
   - Algoritmo: força bruta, dividir-e-conquistar, programação dinâmica, greedy?
   - Estrutura de dados: array, lista, pilha, fila, árvore, grafo, hash?
   - Paradigma: imperativo, funcional, OO?

### Step 2: Escolher Estruturas de Dados

**Guia de seleção baseado em casos de uso:**

| Estrutura | Acesso | Busca | Inserção | Remoção | Uso quando... |
|-----------|--------|-------|----------|---------|---------------|
| **Array** | O(1) | O(n) | O(n) | O(n) | Tamanho fixo, acesso por índice frequente |
| **Lista Ligada** | O(n) | O(n) | O(1)* | O(1)* | Inserções/remoções frequentes, tamanho variável |
| **Pilha (Stack)** | O(1) topo | - | O(1) | O(1) | LIFO: backtracking, recursão, parser |
| **Fila (Queue)** | O(1) início | - | O(1) | O(1) | FIFO: BFS, processamento sequencial |
| **Fila de Prioridade** | O(1) | - | O(log n) | O(log n) | Elemento com maior prioridade sempre acessível |
| **Hash Table** | O(1)* | O(1)* | O(1)* | O(1)* | Busca/inserção rápida por chave |
| **Árvore Binária de Busca** | O(log n)* | O(log n)* | O(log n)* | O(log n)* | Dados ordenados, range queries |
| **Grafo** | - | O(V+E) | O(1) | O(1) | Relações complexas, redes, caminhos |

*Complexidade amortizada ou caso médio

**Consulte:** `references/data-structures-guide.md` para implementações detalhadas

### Step 3: Aplicar Análise de Complexidade

**Big O Notation:**

```
O(1)         - Constante: acesso array por índice
O(log n)     - Logarítmica: busca binária, árvore balanceada
O(n)         - Linear: percorrer lista/array
O(n log n)   - Log-linear: merge sort, heap sort
O(n²)        - Quadrática: bubble sort, nested loops
O(n³)        - Cúbica: multiplicação matriz ingênua
O(2^n)       - Exponencial: subconjuntos, força bruta recursiva
O(n!)        - Fatorial: permutações
```

**Exemplo de análise:**

```pseudocode
// O(n²) - Quadrático
for i = 1 to n:
    for j = 1 to n:
        print(i, j)

// O(n log n) - Log-linear
mergeSort(array):
    if len(array) <= 1: return array
    mid = len(array) / 2
    left = mergeSort(array[0:mid])    # O(log n) divisões
    right = mergeSort(array[mid:])
    return merge(left, right)          # O(n) merge

// O(n) - Linear otimizado
sum = 0
for i = 1 to n:
    sum += i
// Otimizado para O(1): sum = n * (n + 1) / 2
```

**Consulte:** `references/complexity-analysis.md` para técnicas avançadas

### Step 4: Aplicar Paradigmas de Programação

**Orientado a Objetos (OO):**
- **Encapsulamento**: Esconder detalhes de implementação
- **Herança**: Reutilizar código via hierarquia
- **Polimorfismo**: Comportamento diferente para mesma interface
- **Abstração**: Modelar conceitos do domínio

**Funcional:**
- **Funções puras**: Sem efeitos colaterais
- **Imutabilidade**: Dados não modificáveis
- **Higher-order functions**: Funções como argumentos
- **Composição**: Combinar funções simples

**Estruturado:**
- **Sequência**: Instruções em ordem
- **Seleção**: if/else, switch
- **Iteração**: loops (for, while)
- **Modularização**: funções/procedimentos

**Consulte:** `references/programming-paradigms.md` para comparação detalhada

### Step 5: Seguir Princípios SOLID (OO)

**S - Single Responsibility Principle:**
```
❌ ERRADO:
class User:
    save_to_database()
    send_email()
    generate_report()

✅ CORRETO:
class User: ...
class UserRepository: save()
class EmailService: send()
class ReportGenerator: generate()
```

**O - Open/Closed Principle:**
```
❌ ERRADO (modificar classe existente):
class PaymentProcessor:
    process(type):
        if type == "credit": ...
        elif type == "paypal": ...
        elif type == "crypto": ...  # Modifica classe

✅ CORRETO (extensão):
interface Payment: process()
class CreditCardPayment implements Payment
class PayPalPayment implements Payment
class CryptoPayment implements Payment  # Não modifica existentes
```

**L - Liskov Substitution Principle:**
```
❌ ERRADO:
class Bird: fly()
class Penguin extends Bird:
    fly(): throw Exception("Can't fly")  # Quebra contrato

✅ CORRETO:
interface Animal
interface Flyable extends Animal: fly()
class Penguin implements Animal
class Eagle implements Flyable
```

**I - Interface Segregation Principle:**
```
❌ ERRADO (interface grande):
interface Worker: work(), eat(), sleep()
class Robot implements Worker:
    eat(): pass  # Robô não come

✅ CORRETO (interfaces pequenas):
interface Workable: work()
interface Eatable: eat()
class Robot implements Workable
```

**D - Dependency Inversion Principle:**
```
❌ ERRADO (dependência concreta):
class UserController:
    service = new EmailService()  # Acoplamento forte

✅ CORRETO (abstração):
interface NotificationService: notify()
class UserController:
    __init__(service: NotificationService):
        self.service = service  # Injeção de dependência
```

### Step 6: Aplicar Clean Code

**Nomenclatura descritiva:**
```
❌ EVITAR:
d = 86400  # segundos
arr = [1, 2, 3]
def calc(x, y): return x + y

✅ PREFERIR:
SECONDS_PER_DAY = 86400
user_ids = [1, 2, 3]
def calculate_total_price(item_price, quantity): 
    return item_price * quantity
```

**Funções pequenas e coesas:**
```
❌ EVITAR (função faz muitas coisas - 75 linhas):
def process_order(order):
    # Validar (20 linhas)
    # Calcular preço (15 linhas)
    # Salvar no banco (10 linhas)
    # Enviar email (12 linhas)
    # Gerar fatura (18 linhas)

✅ PREFERIR (funções pequenas):
def process_order(order):
    validate_order(order)
    price = calculate_total_price(order)
    save_order(order, price)
    send_confirmation_email(order)
    generate_invoice(order)
```

**DRY - Don't Repeat Yourself:**
```
❌ REPETIÇÃO:
def calculate_circle_area(radius):
    return 3.14159 * radius * radius

def calculate_cylinder_volume(radius, height):
    return 3.14159 * radius * radius * height

✅ DRY:
PI = 3.14159

def calculate_circle_area(radius):
    return PI * radius ** 2

def calculate_cylinder_volume(radius, height):
    return calculate_circle_area(radius) * height
```

**Consulte:** `references/clean-code-guide.md` para mais padrões

### Step 7: Reduzir Complexidade Ciclomática

**Complexidade Ciclomática (M):** Medida de caminhos independentes através do código.

**Cálculo simplificado:** M = 1 + número de pontos de decisão (if, while, for, case, &&, ||)

**Exemplo:**

```
❌ ALTA COMPLEXIDADE (M = 11):
def calculate_discount(customer_type, amount, is_holiday, has_coupon):
    if customer_type == "premium":
        if amount > 1000:
            if is_holiday:
                discount = 0.3
            else:
                discount = 0.25
        elif amount > 500:
            discount = 0.2
        else:
            discount = 0.1
    elif customer_type == "regular":
        if has_coupon:
            discount = 0.15
        else:
            discount = 0.05
    else:
        discount = 0.0
    return amount * (1 - discount)

✅ BAIXA COMPLEXIDADE (M = 2-3 por função):
def calculate_discount(customer, order):
    discount_rate = get_discount_rate(customer, order)
    return apply_discount(order.amount, discount_rate)

def get_discount_rate(customer, order):
    if customer.type == "premium":
        return get_premium_discount(order.amount, order.is_holiday)
    elif customer.type == "regular":
        return get_regular_discount(order.has_coupon)
    return 0.0

def get_premium_discount(amount, is_holiday):
    if amount > 1000:
        return 0.3 if is_holiday else 0.25
    elif amount > 500:
        return 0.2
    return 0.1
```

**Diretrizes:**
- M ≤ 10: Baixa complexidade (bom)
- 11 ≤ M ≤ 20: Moderada (refatorar se possível)
- M > 20: Alta (refatorar obrigatório)

**Consulte:** `references/cyclomatic-complexity.md` para técnicas de redução

### Step 8: Aplicar Design Patterns

**Quando usar patterns:**
- **Problema recorrente**: Solução já testada e documentada
- **Comunicação**: Vocabulário comum entre desenvolvedores
- **Manutenibilidade**: Estrutura conhecida facilita manutenção

**Patterns mais comuns:**

**Creational:**
- **Singleton**: Instância única global
- **Factory**: Criar objetos sem expor lógica de criação
- **Builder**: Construir objetos complexos passo a passo

**Structural:**
- **Adapter**: Compatibilizar interfaces incompatíveis
- **Decorator**: Adicionar comportamento dinamicamente
- **Facade**: Interface simplificada para sistema complexo

**Behavioral:**
- **Strategy**: Trocar algoritmos em runtime
- **Observer**: Notificar mudanças para múltiplos objetos
- **Command**: Encapsular requisição como objeto

**Consulte:** `references/design-patterns-catalog.md` para implementações

### Step 9: Evitar Anti-Patterns

**Code Smells comuns:**

**Duplicação de código:**
- Mesma lógica repetida em múltiplos lugares
- Solução: Extrair método/classe, aplicar DRY

**Funções/classes grandes:**
- Classe com mais de 500 linhas
- Função com mais de 50 linhas
- Solução: Dividir responsabilidades (SRP)

**Nomenclatura ruim:**
- Variáveis de 1 letra (exceto loops simples)
- Nomes genéricos (data, info, manager)
- Solução: Nomes descritivos e contextuais

**Acoplamento alto:**
- Classe depende de muitas outras classes concretas
- Solução: Inversão de dependência, interfaces

**Coesão baixa:**
- Classe com responsabilidades não relacionadas
- Solução: Separar em classes coesas (SRP)

**Consulte:** `references/anti-patterns.md` para catálogo completo

### Step 10: Técnicas Avançadas

**Memoization (caching de resultados):**
```pseudocode
cache = {}

def fibonacci(n):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    result = fibonacci(n-1) + fibonacci(n-2)
    cache[n] = result
    return result
```

**Lazy Evaluation:**
```pseudocode
def generate_numbers(n):
    for i in range(n):
        yield i  # Gera sob demanda, não pré-computa tudo
```

**Tail Recursion:**
```pseudocode
// Não tail-recursive (usa stack)
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

// Tail-recursive (otimizável para loop)
def factorial_tail(n, acc=1):
    if n <= 1: return acc
    return factorial_tail(n - 1, n * acc)
```

**Consulte:** `references/advanced-techniques.md` para mais padrões

---

## Best Practices

### 1. Progressive Disclosure
- Use `references/` para tópicos avançados
- Consulte referências específicas conforme necessidade

### 2. Análise antes de Implementação
- Entenda o problema completamente
- Escolha estrutura de dados adequada
- Calcule complexidade esperada

### 3. Refatoração Contínua
- Melhore código existente regularmente
- Aplique Clean Code e SOLID
- Reduza complexidade ciclomática

### 4. Testes
- Escreva testes para validar algoritmos
- Teste casos extremos (edge cases)
- Consulte `references/testing-fundamentals.md`

### 5. Documentação
- Documente complexidade de algoritmos
- Explique escolhas de estruturas de dados
- Justifique uso de patterns

---

## Common Patterns

**Algoritmo de busca binária:**
```pseudocode
def binary_search(sorted_array, target):
    left, right = 0, len(sorted_array) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if sorted_array[mid] == target:
            return mid
        elif sorted_array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Não encontrado
```

**Algoritmo de ordenação merge sort:**
```pseudocode
def merge_sort(array):
    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
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

**Padrão Strategy:**
```pseudocode
interface SortStrategy:
    sort(array)

class QuickSort implements SortStrategy:
    sort(array): ...

class MergeSort implements SortStrategy:
    sort(array): ...

class Sorter:
    __init__(strategy: SortStrategy):
        self.strategy = strategy
    
    sort_data(array):
        return self.strategy.sort(array)
```

---

## References

Para tópicos avançados e implementações detalhadas:

- **[Data Structures Guide](./references/data-structures-guide.md)** - Arrays, listas, pilhas, filas, árvores, grafos
- **[Algorithms Fundamentals](./references/algorithms-fundamentals.md)** - Ordenação, busca, dividir-conquistar, DP, greedy
- **[Complexity Analysis](./references/complexity-analysis.md)** - Big O, análise amortizada, trade-offs
- **[Programming Paradigms](./references/programming-paradigms.md)** - OO, funcional, estrutural, comparações
- **[Design Patterns Catalog](./references/design-patterns-catalog.md)** - GoF patterns detalhados
- **[Clean Code Guide](./references/clean-code-guide.md)** - Nomenclatura, funções, formatação
- **[Cyclomatic Complexity](./references/cyclomatic-complexity.md)** - Cálculo, redução, refatorações
- **[Anti-Patterns](./references/anti-patterns.md)** - Code smells e como evitar
- **[Advanced Techniques](./references/advanced-techniques.md)** - Memoization, lazy eval, tail recursion
- **[Testing Fundamentals](./references/testing-fundamentals.md)** - TDD, cobertura, mocks

---

## Sources

1. **Introduction to Algorithms (CLRS)** - Cormen, Leiserson, Rivest, Stein - MIT Press
2. **Design Patterns: Elements of Reusable Object-Oriented Software** - Gang of Four - Addison-Wesley
3. **Clean Code: A Handbook of Agile Software Craftsmanship** - Robert C. Martin - Prentice Hall
4. **Refactoring: Improving the Design of Existing Code** - Martin Fowler - Addison-Wesley
5. **Structure and Interpretation of Computer Programs (SICP)** - Abelson, Sussman - MIT Press
6. **Code Complete, 2nd Edition** - Steve McConnell - Microsoft Press
7. **A Complexity Measure (IEEE)** - Thomas J. McCabe - 1976
8. **The Pragmatic Programmer** - Hunt, Thomas - Addison-Wesley
