# Anti-Patterns and Code Smells

## Overview

Anti-patterns are common solutions to recurring problems that are ineffective and counterproductive. Code smells are surface indicators that usually correspond to deeper problems in the system. This guide covers identification and remediation strategies.

## Code Smells

### 1. Duplicated Code

**Description:** Identical or very similar code exists in multiple locations.

**Example:**

```pseudo
function calculateEmployeeBonus(employee):
    salary = employee.salary
    yearsOfService = employee.yearsOfService
    if yearsOfService > 10:
        bonus = salary * 0.15
    else if yearsOfService > 5:
        bonus = salary * 0.10
    else:
        bonus = salary * 0.05
    return bonus

function calculateContractorBonus(contractor):
    salary = contractor.hourlyRate * 2000
    yearsOfService = contractor.yearsOfService
    if yearsOfService > 10:
        bonus = salary * 0.15
    else if yearsOfService > 5:
        bonus = salary * 0.10
    else:
        bonus = salary * 0.05
    return bonus
```

**Refactored:**

```pseudo
function calculateBonus(yearsOfService, salary):
    if yearsOfService > 10:
        return salary * 0.15
    else if yearsOfService > 5:
        return salary * 0.10
    else:
        return salary * 0.05

function calculateEmployeeBonus(employee):
    return calculateBonus(employee.yearsOfService, employee.salary)

function calculateContractorBonus(contractor):
    salary = contractor.hourlyRate * 2000
    return calculateBonus(contractor.yearsOfService, salary)
```

### 2. Long Method

**Description:** A method that has grown too large and does too many things.

**Threshold:** Generally > 20-30 lines is suspicious, > 50 lines is problematic.

**Example:**

```pseudo
function processOrder(order):
    if order is null:
        throw Error("Order cannot be null")
    
    if order.items.isEmpty():
        throw Error("Order must contain items")
    
    total = 0
    for item in order.items:
        if item.quantity <= 0:
            throw Error("Invalid quantity")
        total += item.price * item.quantity
    
    tax = total * 0.08
    total += tax
    
    if order.customer.membershipLevel == "gold":
        discount = total * 0.1
    else if order.customer.membershipLevel == "silver":
        discount = total * 0.05
    else:
        discount = 0
    
    total -= discount
    
    order.total = total
    order.status = "processed"
    
    database.save(order)
    
    email = "Order #" + order.id + " total: $" + total
    sendEmail(order.customer.email, email)
    
    inventory.reduceStock(order.items)
    
    log("Order processed: " + order.id)
    
    return order
```

**Refactored:**

```pseudo
function processOrder(order):
    validateOrder(order)
    calculateOrderTotal(order)
    saveOrder(order)
    notifyCustomer(order)
    updateInventory(order)
    logOrderProcessed(order)
    return order

function validateOrder(order):
    if order is null:
        throw Error("Order cannot be null")
    if order.items.isEmpty():
        throw Error("Order must contain items")
    for item in order.items:
        if item.quantity <= 0:
            throw Error("Invalid quantity")

function calculateOrderTotal(order):
    subtotal = calculateSubtotal(order.items)
    tax = subtotal * 0.08
    discount = calculateDiscount(subtotal, order.customer)
    order.total = subtotal + tax - discount
    order.status = "processed"
```

### 3. Large Class

**Description:** A class that has grown to do too much, violating Single Responsibility Principle.

**Indicators:**
- Too many instance variables (> 10-15)
- Too many methods (> 20-30)
- Too many lines of code (> 500-1000)

**Example:**

```pseudo
class User:
    username, password, email, firstName, lastName
    address, city, state, zip, country
    phone, mobile, fax
    accountBalance, creditLimit, lastPaymentDate
    preferences, settings, notifications
    
    function login()
    function logout()
    function changePassword()
    function updateEmail()
    function updateProfile()
    function updateAddress()
    function makePayment()
    function checkBalance()
    function getCreditLimit()
    function sendNotification()
    function getPreferences()
    function updateSettings()
    function validateEmail()
    function validatePhone()
    function formatAddress()
```

**Refactored:**

```pseudo
class User:
    username, passwordHash, email
    profile, contactInfo, account, preferences
    
    function login()
    function logout()
    function changePassword()

class UserProfile:
    firstName, lastName, avatarUrl
    
    function update()
    function getDisplayName()

class ContactInfo:
    address, phone, mobile
    
    function update()
    function validate()
    function format()

class UserAccount:
    balance, creditLimit, transactions
    
    function makePayment()
    function checkBalance()
    function getHistory()

class UserPreferences:
    settings, notifications
    
    function update()
    function get()
```

### 4. Long Parameter List

**Description:** Methods with too many parameters (> 3-4) are hard to understand and use.

**Example:**

```pseudo
function createUser(username, password, email, firstName, lastName, 
                   address, city, state, zip, phone, role, department):
    user = new User()
    user.username = username
    user.password = hashPassword(password)
    user.email = email
    user.firstName = firstName
    user.lastName = lastName
    user.address = address
    user.city = city
    user.state = state
    user.zip = zip
    user.phone = phone
    user.role = role
    user.department = department
    return user
```

**Refactored:**

```pseudo
class UserBuilder:
    username, password, email
    profile, contact, employment
    
    function withCredentials(username, password, email):
        this.username = username
        this.password = password
        this.email = email
        return this
    
    function withProfile(profile):
        this.profile = profile
        return this
    
    function withContact(contact):
        this.contact = contact
        return this
    
    function withEmployment(role, department):
        this.employment = new Employment(role, department)
        return this
    
    function build():
        return new User(this)

usage:
user = new UserBuilder()
    .withCredentials("john", "pass123", "john@example.com")
    .withProfile(new Profile("John", "Doe"))
    .withContact(new Contact("123 Main St", "555-1234"))
    .withEmployment("Developer", "Engineering")
    .build()
```

### 5. Divergent Change

**Description:** One class is commonly changed in different ways for different reasons.

**Example:**

```pseudo
class Order:
    function calculateTotal()
    function applyDiscount()
    function calculateTax()
    function validatePayment()
    function processPayment()
    function generateInvoice()
    function formatInvoiceHTML()
    function formatInvoicePDF()
    function sendInvoiceEmail()
    function updateInventory()
    function trackShipment()
```

**Refactored:**

```pseudo
class Order:
    function calculateTotal()
    function applyDiscount()

class PaymentProcessor:
    function validatePayment()
    function processPayment()

class InvoiceGenerator:
    function generate()
    function formatHTML()
    function formatPDF()
    function send()

class InventoryManager:
    function updateStock()

class ShipmentTracker:
    function track()
```

### 6. Shotgun Surgery

**Description:** Making a change requires many small changes across many classes.

**Example:**

```pseudo
Adding a new payment method requires changes in:
- PaymentProcessor.processPayment()
- OrderController.checkout()
- PaymentValidator.validate()
- PaymentFormatter.format()
- InvoiceGenerator.generate()
- ReportGenerator.generateSalesReport()
- Database.savePayment()
```

**Refactored:**

```pseudo
interface PaymentMethod:
    function process(amount)
    function validate()
    function format()
    function getType()

class CreditCardPayment implements PaymentMethod:
    function process(amount):
        ...
    function validate():
        ...
    function format():
        ...
    function getType():
        return "credit_card"

class PaymentProcessor:
    function process(paymentMethod, amount):
        if not paymentMethod.validate():
            return error
        return paymentMethod.process(amount)

Adding a new payment method now only requires:
1. Create new class implementing PaymentMethod
2. Register in payment method factory
```

### 7. Feature Envy

**Description:** A method accesses data of another object more than its own data.

**Example:**

```pseudo
class Order:
    customer, items, date
    
    function getCustomerDiscount():
        if this.customer.membershipLevel == "gold":
            if this.customer.yearsActive > 5:
                return 0.20
            else:
                return 0.15
        else if this.customer.membershipLevel == "silver":
            return 0.10
        else:
            return 0
```

**Refactored:**

```pseudo
class Customer:
    membershipLevel, yearsActive
    
    function getDiscount():
        if this.membershipLevel == "gold":
            if this.yearsActive > 5:
                return 0.20
            else:
                return 0.15
        else if this.membershipLevel == "silver":
            return 0.10
        else:
            return 0

class Order:
    customer, items, date
    
    function getCustomerDiscount():
        return this.customer.getDiscount()
```

### 8. Data Clumps

**Description:** Same group of data items appear together in multiple places.

**Example:**

```pseudo
function createAddress(street, city, state, zip):
    ...

function validateAddress(street, city, state, zip):
    ...

function formatAddress(street, city, state, zip):
    ...

class Customer:
    street, city, state, zip
    billingStreet, billingCity, billingState, billingZip
```

**Refactored:**

```pseudo
class Address:
    street, city, state, zip
    
    function validate():
        ...
    
    function format():
        ...

class Customer:
    shippingAddress, billingAddress
```

### 9. Primitive Obsession

**Description:** Using primitive types instead of small objects for simple tasks.

**Example:**

```pseudo
function sendEmail(to, subject, body):
    if not to.contains("@"):
        throw Error("Invalid email")
    ...

function validateEmail(email):
    if not email.contains("@"):
        return false
    return true

class User:
    email
    
    function changeEmail(newEmail):
        if not newEmail.contains("@"):
            throw Error("Invalid email")
        this.email = newEmail
```

**Refactored:**

```pseudo
class Email:
    value
    
    function constructor(emailString):
        if not this.isValid(emailString):
            throw Error("Invalid email")
        this.value = emailString
    
    function isValid(emailString):
        return emailString.contains("@") and emailString.length > 3
    
    function toString():
        return this.value

function sendEmail(to, subject, body):
    ...

class User:
    email
    
    function changeEmail(newEmail):
        this.email = newEmail
```

### 10. Switch Statements

**Description:** Same switch statement appears in multiple places.

**Example:**

```pseudo
function getEmployeeSalary(employee):
    switch employee.type:
        case "engineer":
            return employee.baseSalary * 1.5
        case "manager":
            return employee.baseSalary * 2.0
        case "intern":
            return employee.baseSalary * 0.5

function getEmployeeBonus(employee):
    switch employee.type:
        case "engineer":
            return employee.baseSalary * 0.15
        case "manager":
            return employee.baseSalary * 0.25
        case "intern":
            return employee.baseSalary * 0.05

function getEmployeeVacationDays(employee):
    switch employee.type:
        case "engineer":
            return 20
        case "manager":
            return 25
        case "intern":
            return 10
```

**Refactored:**

```pseudo
class Employee:
    baseSalary
    
    function getSalary()
    function getBonus()
    function getVacationDays()

class Engineer extends Employee:
    function getSalary():
        return this.baseSalary * 1.5
    function getBonus():
        return this.baseSalary * 0.15
    function getVacationDays():
        return 20

class Manager extends Employee:
    function getSalary():
        return this.baseSalary * 2.0
    function getBonus():
        return this.baseSalary * 0.25
    function getVacationDays():
        return 25

class Intern extends Employee:
    function getSalary():
        return this.baseSalary * 0.5
    function getBonus():
        return this.baseSalary * 0.05
    function getVacationDays():
        return 10
```

## Anti-Patterns

### 1. God Object

**Description:** An object that knows too much or does too much.

**Characteristics:**
- Controls too many other objects
- Has too many dependencies
- Has too many responsibilities
- Too many lines of code (thousands)

**Example:**

```pseudo
class ApplicationManager:
    database, config, logger, cache, emailService
    userManager, orderManager, inventoryManager
    paymentProcessor, reportGenerator
    
    function initializeApplication()
    function shutdownApplication()
    function handleRequest()
    function authenticateUser()
    function processOrder()
    function updateInventory()
    function sendEmail()
    function generateReport()
    function cacheData()
    function validateInput()
    function handleError()
```

**Refactored:**

```pseudo
class Application:
    config, serviceContainer
    
    function initialize():
        this.serviceContainer.register("database", new Database())
        this.serviceContainer.register("auth", new AuthService())
        this.serviceContainer.register("order", new OrderService())
    
    function handleRequest(request):
        controller = this.routeRequest(request)
        return controller.handle(request)

class AuthService:
    function authenticate(credentials)

class OrderService:
    function process(order)

class InventoryService:
    function update(items)
```

### 2. Lava Flow

**Description:** Dead code and forgotten design information is frozen in an ever-changing design.

**Indicators:**
- Commented-out code
- Unused variables/functions
- Unclear purpose of code
- "Don't touch" regions

**Example:**

```pseudo
function processData(data):
    result = []
    
    for item in data:
        result.append(item)
    
    return result

function processDataOld(data):
    result = []
    for item in data:
        if item.valid:
            result.append(item)
    return result

function processDataBackup(data):
    ...
```

**Solution:**

```pseudo
function processData(data):
    return data.filter(item => item.valid)
```

### 3. Spaghetti Code

**Description:** Code with complex and tangled control structure.

**Characteristics:**
- Excessive use of GOTO
- Deeply nested conditionals
- No clear flow
- Hard to follow logic

**Example:**

```pseudo
function process(data):
    if data is not null:
        if data.length > 0:
            for i = 0 to data.length:
                if data[i].valid:
                    if data[i].processed:
                        continue
                    else:
                        if data[i].type == "A":
                            if data[i].value > 100:
                                processTypeA(data[i])
                            else:
                                skipItem(data[i])
                        else if data[i].type == "B":
                            processTypeB(data[i])
                        else:
                            handleUnknown(data[i])
                    data[i].processed = true
```

**Refactored:**

```pseudo
function process(data):
    if data is null or data.isEmpty():
        return
    
    for item in data:
        processItem(item)

function processItem(item):
    if not item.valid or item.processed:
        return
    
    processItemByType(item)
    item.processed = true

function processItemByType(item):
    handlers = {
        "A": processTypeAIfEligible,
        "B": processTypeB,
        default: handleUnknown
    }
    
    handler = handlers[item.type] or handlers.default
    handler(item)

function processTypeAIfEligible(item):
    if item.value > 100:
        processTypeA(item)
    else:
        skipItem(item)
```

### 4. Golden Hammer

**Description:** "If all you have is a hammer, everything looks like a nail."

**Example:**

```pseudo
Using inheritance for everything:

class List extends Database:
    ...

class Configuration extends Database:
    ...

Using patterns inappropriately:

class SimpleAdder:
    factory, builder, strategy, observer, mediator
    
    function add(a, b):
        return a + b
```

**Solution:**

Use the right tool for the job. Not every problem needs the same solution.

### 5. Cargo Cult Programming

**Description:** Using patterns and practices without understanding why.

**Example:**

```pseudo
function addNumbers(a, b):
    try:
        result = a + b
        return result
    catch error:
        throw error
    finally:
        doNothing()

class SimpleValue:
    value
    
    function getValue():
        return this.value
    
    function setValue(value):
        this.value = value

interface ISimpleValue:
    function getValue()
    function setValue(value)

class SimpleValueFactory:
    function create(value):
        return new SimpleValue(value)

class SimpleValueBuilder:
    value
    
    function withValue(value):
        this.value = value
        return this
    
    function build():
        factory = new SimpleValueFactory()
        return factory.create(this.value)
```

**Refactored:**

```pseudo
class SimpleValue:
    value
```

### 6. Copy-Paste Programming

**Description:** Copying code and making minor modifications instead of abstracting.

**Example:**

```pseudo
function validateUsername(username):
    if username is null:
        return false
    if username.length < 3:
        return false
    if username.length > 20:
        return false
    if not username.matches("[a-zA-Z0-9]+"):
        return false
    return true

function validatePassword(password):
    if password is null:
        return false
    if password.length < 8:
        return false
    if password.length > 50:
        return false
    if not password.matches("[a-zA-Z0-9!@#$%]+"):
        return false
    return true

function validateEmail(email):
    if email is null:
        return false
    if email.length < 5:
        return false
    if email.length > 100:
        return false
    if not email.matches(".+@.+\\..+"):
        return false
    return true
```

**Refactored:**

```pseudo
function validateField(value, minLength, maxLength, pattern):
    if value is null:
        return false
    if value.length < minLength or value.length > maxLength:
        return false
    if not value.matches(pattern):
        return false
    return true

function validateUsername(username):
    return validateField(username, 3, 20, "[a-zA-Z0-9]+")

function validatePassword(password):
    return validateField(password, 8, 50, "[a-zA-Z0-9!@#$%]+")

function validateEmail(email):
    return validateField(email, 5, 100, ".+@.+\\..+")
```

## Detection Techniques

### Static Analysis

```pseudo
Tools to detect code smells:
- SonarQube: Comprehensive analysis
- PMD: Rule-based detection
- Checkstyle: Style and structure
- ESLint: JavaScript linting
- RuboCop: Ruby style guide
- Pylint: Python code analysis
```

### Code Metrics

```pseudo
Metrics that indicate problems:

Cyclomatic Complexity > 10
Lines of Code > 500 per class
Number of Methods > 30 per class
Method Length > 50 lines
Parameter Count > 4
Coupling > 10
Lack of Cohesion > 0.8
Depth of Inheritance > 5
```

### Code Review Checklist

```
[ ] Functions < 30 lines
[ ] Classes < 500 lines
[ ] Parameters < 4
[ ] No duplicated code blocks
[ ] No deeply nested conditionals (> 3 levels)
[ ] Clear single responsibility
[ ] No primitive obsession
[ ] Meaningful names
[ ] No dead code
[ ] No magic numbers
```

## Refactoring Strategies

### Extract Method

When: Long method, duplicated code, complex logic

```pseudo
Before:
function complex():
    step 1
    step 2
    step 3

After:
function complex():
    doStep1()
    doStep2()
    doStep3()
```

### Extract Class

When: Large class, divergent change

```pseudo
Before:
class User:
    many fields
    many methods

After:
class User:
    profile, account, preferences
```

### Replace Type Code with Polymorphism

When: Switch statements, type codes

```pseudo
Before:
switch type:
    case A: ...
    case B: ...

After:
class A:
    method()
class B:
    method()
```

### Introduce Parameter Object

When: Long parameter list, data clumps

```pseudo
Before:
function create(a, b, c, d, e):
    ...

After:
function create(params):
    ...
```

## Summary

Anti-patterns and code smells indicate design problems that make code harder to maintain. Regular refactoring, code reviews, and static analysis help prevent and remediate these issues. Focus on simplicity, clarity, and single responsibility.
