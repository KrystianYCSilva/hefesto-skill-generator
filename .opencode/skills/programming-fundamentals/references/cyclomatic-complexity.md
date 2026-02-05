# Cyclomatic Complexity

## Overview

Cyclomatic complexity is a software metric used to measure the complexity of a program by quantifying the number of linearly independent paths through the program's source code. Developed by Thomas J. McCabe in 1976, it provides an objective measure of code complexity.

## Definition

Cyclomatic complexity (M) measures the number of independent decision paths in code. Higher values indicate more complex code that is harder to test, understand, and maintain.

## Calculation Formula

The basic formula for cyclomatic complexity is:

```
M = E - N + 2P

Where:
M = Cyclomatic Complexity
E = Number of edges in the control flow graph
N = Number of nodes in the control flow graph
P = Number of connected components (usually 1 for a single method)
```

### Simplified Formula

For a single function or method (P=1):

```
M = E - N + 2
```

### Alternative Formula

A more practical formula for counting:

```
M = Number of decision points + 1

Where decision points include:
- if, else if
- for, while, do-while loops
- case in switch statements
- && and || operators
- ? : ternary operators
- catch blocks
- goto statements
```

## Control Flow Graph Example

### Simple Function

```pseudo
function authenticate(username, password):
    if username is empty:
        return false
    
    if password is empty:
        return false
    
    user = database.find(username)
    
    if user exists:
        if user.password matches password:
            return true
    
    return false
```

**Control Flow Graph:**
```
Start (1)
  ↓
Check username empty (2)
  ↓ (no)        ↓ (yes)
Check password  Return false (3)
empty (4)
  ↓ (no)        ↓ (yes)
Find user      Return false (5)
(6)
  ↓
Check user     
exists (7)
  ↓ (no)        ↓ (yes)
Return false   Check password
(8)            matches (9)
               ↓ (no)    ↓ (yes)
               Return    Return
               false(10) true(11)
```

**Calculation:**
- Nodes (N) = 11
- Edges (E) = 13
- M = 13 - 11 + 2 = 4

**Alternative calculation:**
- Decision points: if username (1), if password (2), if user exists (3), if password matches (4)
- M = 4 + 1 = 5

Note: Minor difference due to graph construction method.

## Practical Calculation Examples

### Example 1: Linear Code (M=1)

```pseudo
function calculateTotal(price, quantity):
    subtotal = price * quantity
    tax = subtotal * 0.08
    total = subtotal + tax
    return total
```

**Complexity:** M = 1 (no branches)

### Example 2: Single If Statement (M=2)

```pseudo
function getDiscount(amount):
    discount = 0
    if amount > 100:
        discount = amount * 0.1
    return discount
```

**Complexity:** M = 2 (1 decision point + 1)

### Example 3: Multiple Conditions (M=4)

```pseudo
function validateAge(age):
    if age < 0:
        return "Invalid"
    else if age < 18:
        return "Minor"
    else if age < 65:
        return "Adult"
    else:
        return "Senior"
```

**Complexity:** M = 4 (3 decision points + 1)

### Example 4: Nested Conditions (M=5)

```pseudo
function processOrder(order):
    if order is null:
        return "Error"
    
    if order.isPaid():
        if order.isShipped():
            return "Complete"
        else:
            return "Processing"
    else:
        if order.isCancelled():
            return "Cancelled"
        else:
            return "Pending"
```

**Complexity:** M = 5
- Decision points: null check (1), isPaid (2), isShipped (3), isCancelled (4)
- M = 4 + 1 = 5

### Example 5: Loops (M=4)

```pseudo
function findMax(numbers):
    if numbers is empty:
        return null
    
    max = numbers[0]
    
    for each num in numbers:
        if num > max:
            max = num
    
    return max
```

**Complexity:** M = 4
- Decision points: empty check (1), for loop (2), if num > max (3)
- M = 3 + 1 = 4

### Example 6: Switch Statement (M=5)

```pseudo
function getPrice(productType):
    switch productType:
        case "book":
            return 10.0
        case "dvd":
            return 15.0
        case "game":
            return 60.0
        case "toy":
            return 20.0
        default:
            return 0.0
```

**Complexity:** M = 5 (4 case statements + 1)

### Example 7: Logical Operators (M=4)

```pseudo
function canVote(age, citizenship, registered):
    if age >= 18 && citizenship == "US" && registered:
        return true
    return false
```

**Complexity:** M = 4
- Decision points: age check (1), && citizenship (2), && registered (3)
- M = 3 + 1 = 4

### Example 8: Complex Function (M=12)

```pseudo
function processPayment(payment, account):
    if payment is null || account is null:
        return "Error: Invalid input"
    
    if payment.amount <= 0:
        return "Error: Invalid amount"
    
    if account.balance < payment.amount:
        if payment.allowOverdraft:
            if account.overdraftLimit >= payment.amount - account.balance:
                account.balance -= payment.amount
                return "Success: Overdraft used"
            else:
                return "Error: Overdraft limit exceeded"
        else:
            return "Error: Insufficient funds"
    
    account.balance -= payment.amount
    
    if payment.amount > 1000:
        if account.requiresApproval():
            sendApprovalRequest(payment)
            return "Pending: Requires approval"
    
    if payment.category == "international":
        applyInternationalFee(payment)
    
    return "Success"
```

**Complexity:** M = 12
- Decision points: null checks with || (2), amount check (1), balance check (1), allowOverdraft (1), overdraft limit (1), amount > 1000 (1), requiresApproval (1), category check (1)
- M = 9 + 1 = 10 (approximate, may vary with exact counting method)

## Complexity Thresholds

### Industry Guidelines

| Complexity (M) | Risk Level | Maintainability | Testing Effort |
|---------------|------------|-----------------|----------------|
| 1-10 | Low | High | Simple |
| 11-20 | Moderate | Medium | Moderate |
| 21-50 | High | Low | Complex |
| 50+ | Very High | Very Low | Very Complex |

### Recommendations

```
M = 1-10:   Simple procedure, low risk
M = 11-20:  More complex, moderate risk, consider refactoring
M = 21-50:  Complex, high risk, refactor recommended
M = 50+:    Untestable, very high risk, refactor required
```

### Testing Requirements

```
M = 1-10:   Minimum of M test cases
M = 11-20:  M + edge cases test coverage
M = 21+:    Comprehensive testing required, difficult to achieve full coverage
```

## Refactoring Techniques

### Technique 1: Extract Method

**Before (M=8):**

```pseudo
function processUser(user):
    if user is null:
        return "Error"
    
    if user.age < 18:
        return "Minor"
    
    if user.email is empty:
        return "No email"
    
    if not isValidEmail(user.email):
        return "Invalid email"
    
    if user.country == "US":
        if user.state is empty:
            return "State required"
    
    if user.subscribed:
        sendWelcomeEmail(user)
    
    return "Success"
```

**After (M=5, M=2, M=2):**

```pseudo
function processUser(user):
    if user is null:
        return "Error"
    
    ageCheck = validateAge(user)
    if ageCheck != "Valid":
        return ageCheck
    
    emailCheck = validateEmail(user)
    if emailCheck != "Valid":
        return emailCheck
    
    if user.subscribed:
        sendWelcomeEmail(user)
    
    return "Success"

function validateAge(user):
    if user.age < 18:
        return "Minor"
    return "Valid"

function validateEmail(user):
    if user.email is empty:
        return "No email"
    if not isValidEmail(user.email):
        return "Invalid email"
    return "Valid"
```

### Technique 2: Guard Clauses

**Before (M=5):**

```pseudo
function withdraw(account, amount):
    if account is not null:
        if amount > 0:
            if account.balance >= amount:
                account.balance -= amount
                return "Success"
            else:
                return "Insufficient funds"
        else:
            return "Invalid amount"
    else:
        return "Invalid account"
```

**After (M=4):**

```pseudo
function withdraw(account, amount):
    if account is null:
        return "Invalid account"
    
    if amount <= 0:
        return "Invalid amount"
    
    if account.balance < amount:
        return "Insufficient funds"
    
    account.balance -= amount
    return "Success"
```

### Technique 3: Replace Conditional with Polymorphism

**Before (M=5):**

```pseudo
function getSpeed(vehicle):
    if vehicle.type == "car":
        return vehicle.speed * 1.0
    else if vehicle.type == "bike":
        return vehicle.speed * 0.5
    else if vehicle.type == "plane":
        return vehicle.speed * 10.0
    else:
        return vehicle.speed
```

**After (M=1 per class):**

```pseudo
interface Vehicle:
    function getSpeed()

class Car implements Vehicle:
    function getSpeed():
        return this.speed * 1.0

class Bike implements Vehicle:
    function getSpeed():
        return this.speed * 0.5

class Plane implements Vehicle:
    function getSpeed():
        return this.speed * 10.0
```

### Technique 4: Strategy Pattern

**Before (M=6):**

```pseudo
function calculateShipping(order):
    if order.priority == "express":
        if order.weight > 10:
            return 50.0
        else:
            return 25.0
    else if order.priority == "standard":
        if order.weight > 10:
            return 20.0
        else:
            return 10.0
    else:
        return 5.0
```

**After (M=1 per strategy):**

```pseudo
interface ShippingStrategy:
    function calculate(order)

class ExpressShipping implements ShippingStrategy:
    function calculate(order):
        return order.weight > 10 ? 50.0 : 25.0

class StandardShipping implements ShippingStrategy:
    function calculate(order):
        return order.weight > 10 ? 20.0 : 10.0

class EconomyShipping implements ShippingStrategy:
    function calculate(order):
        return 5.0

function calculateShipping(order, strategy):
    return strategy.calculate(order)
```

### Technique 5: Lookup Tables

**Before (M=7):**

```pseudo
function getDaysInMonth(month):
    if month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12:
        return 31
    else if month == 4 || month == 6 || month == 9 || month == 11:
        return 30
    else if month == 2:
        return 28
    else:
        return 0
```

**After (M=1):**

```pseudo
DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

function getDaysInMonth(month):
    if month < 1 || month > 12:
        return 0
    return DAYS_IN_MONTH[month]
```

### Technique 6: Decompose Complex Conditionals

**Before (M=6):**

```pseudo
function shouldApprove(loan):
    if (loan.amount < 10000 && loan.credit_score > 700) ||
       (loan.amount < 50000 && loan.credit_score > 750 && loan.income > 50000) ||
       (loan.amount >= 50000 && loan.credit_score > 800 && loan.income > 100000 && loan.debt_ratio < 0.3):
        return true
    return false
```

**After (M=2, M=2, M=2):**

```pseudo
function shouldApprove(loan):
    if isSmallLoanEligible(loan):
        return true
    if isMediumLoanEligible(loan):
        return true
    if isLargeLoanEligible(loan):
        return true
    return false

function isSmallLoanEligible(loan):
    return loan.amount < 10000 && loan.credit_score > 700

function isMediumLoanEligible(loan):
    return loan.amount < 50000 && loan.credit_score > 750 && loan.income > 50000

function isLargeLoanEligible(loan):
    return loan.amount >= 50000 && loan.credit_score > 800 && 
           loan.income > 100000 && loan.debt_ratio < 0.3
```

## Tools and Automation

### Static Analysis Tools

**SonarQube:**
```bash
sonar-scanner -Dsonar.projectKey=myproject
```

**Radon (Python):**
```bash
radon cc myfile.py -a
```

**Complexity-report (JavaScript):**
```bash
cr --format json src/
```

**PMD (Java):**
```bash
pmd -d src/ -R rulesets/java/codesize.xml
```

**Lizard (Multi-language):**
```bash
lizard -l java src/
```

### CI/CD Integration

```yaml
quality_gate:
  script:
    - lizard -l java src/ --CCN 10
  allow_failure: false
```

### IDE Integration

Most modern IDEs provide cyclomatic complexity metrics:

```
Visual Studio Code: CodeMetrics extension
IntelliJ IDEA: MetricsReloaded plugin
Eclipse: Metrics plugin
```

## Real-World Examples

### Example 1: Password Validation (M=8)

```pseudo
function isValidPassword(password):
    if password is null || password.length < 8:
        return false
    
    hasUpper = false
    hasLower = false
    hasDigit = false
    hasSpecial = false
    
    for each char in password:
        if char is uppercase:
            hasUpper = true
        else if char is lowercase:
            hasLower = true
        else if char is digit:
            hasDigit = true
        else if char is special:
            hasSpecial = true
    
    return hasUpper && hasLower && hasDigit && hasSpecial
```

**Refactored (M=3):**

```pseudo
function isValidPassword(password):
    if not meetsLengthRequirement(password):
        return false
    
    return hasRequiredCharacterTypes(password)

function meetsLengthRequirement(password):
    return password is not null && password.length >= 8

function hasRequiredCharacterTypes(password):
    return containsUppercase(password) &&
           containsLowercase(password) &&
           containsDigit(password) &&
           containsSpecial(password)
```

### Example 2: Shopping Cart Discount (M=11)

```pseudo
function calculateDiscount(cart):
    discount = 0
    
    if cart.total > 100:
        discount += cart.total * 0.1
    
    if cart.membershipLevel == "gold":
        discount += cart.total * 0.05
    else if cart.membershipLevel == "silver":
        discount += cart.total * 0.03
    
    if cart.items.count > 5:
        discount += 10
    
    if cart.hasPromoCode:
        if cart.promoCode == "SAVE20":
            discount += cart.total * 0.2
        else if cart.promoCode == "SAVE10":
            discount += cart.total * 0.1
    
    if discount > cart.total * 0.5:
        discount = cart.total * 0.5
    
    return discount
```

**Refactored (M=2, M=3, M=2, M=3, M=2):**

```pseudo
function calculateDiscount(cart):
    discount = 0
    discount += getVolumeDiscount(cart)
    discount += getMembershipDiscount(cart)
    discount += getItemCountBonus(cart)
    discount += getPromoCodeDiscount(cart)
    return capDiscount(discount, cart.total)

function getVolumeDiscount(cart):
    if cart.total > 100:
        return cart.total * 0.1
    return 0

function getMembershipDiscount(cart):
    if cart.membershipLevel == "gold":
        return cart.total * 0.05
    else if cart.membershipLevel == "silver":
        return cart.total * 0.03
    return 0

function getItemCountBonus(cart):
    if cart.items.count > 5:
        return 10
    return 0

function getPromoCodeDiscount(cart):
    if not cart.hasPromoCode:
        return 0
    
    if cart.promoCode == "SAVE20":
        return cart.total * 0.2
    else if cart.promoCode == "SAVE10":
        return cart.total * 0.1
    
    return 0

function capDiscount(discount, total):
    maxDiscount = total * 0.5
    if discount > maxDiscount:
        return maxDiscount
    return discount
```

## Benefits of Low Complexity

1. **Testability**: Fewer paths = fewer test cases needed
2. **Readability**: Simpler logic = easier to understand
3. **Maintainability**: Lower complexity = easier to modify
4. **Reliability**: Fewer paths = fewer potential bugs
5. **Code Review**: Simpler code = faster reviews

## Common Pitfalls

### Pitfall 1: Ignoring Logical Operators

```pseudo
if condition1 && condition2 && condition3:
```

This counts as M=4, not M=2.

### Pitfall 2: Hidden Complexity

```pseudo
list.filter(x => x > 0).map(x => x * 2).reduce((a, b) => a + b)
```

Callbacks add complexity not immediately visible.

### Pitfall 3: Over-Refactoring

Breaking M=11 into 10 M=1 functions might be excessive. Balance is key.

## Best Practices

1. **Target M≤10** for most functions
2. **Use guard clauses** to reduce nesting
3. **Extract complex conditions** into named functions
4. **Apply polymorphism** for type-based branching
5. **Monitor in CI/CD** to prevent complexity creep
6. **Review high-complexity** code during code reviews
7. **Document complex logic** when complexity is unavoidable
8. **Refactor incrementally** rather than all at once

## Summary

Cyclomatic complexity is a quantitative measure of code complexity. By keeping M≤10, you ensure code remains testable, maintainable, and reliable. Use the provided refactoring techniques to reduce complexity systematically.
