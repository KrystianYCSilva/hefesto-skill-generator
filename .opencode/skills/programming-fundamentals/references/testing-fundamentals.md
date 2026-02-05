# Testing Fundamentals

## Overview

Software testing ensures code correctness, prevents regressions, and enables confident refactoring. This guide covers test-driven development (TDD), the test pyramid, types of tests, test doubles, coverage metrics, and best practices.

## Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

```
1. RED:    Write a failing test
2. GREEN:  Write minimal code to make it pass
3. REFACTOR: Improve code while keeping tests passing
4. REPEAT
```

### TDD Example: Calculator

**Step 1: Red (Write failing test)**

```pseudo
test "addition of two numbers":
    calculator = new Calculator()
    result = calculator.add(2, 3)
    assert result equals 5
```

**Step 2: Green (Minimal implementation)**

```pseudo
class Calculator:
    function add(a, b):
        return 5
```

**Step 3: Add more tests (Red)**

```pseudo
test "addition of different numbers":
    calculator = new Calculator()
    result = calculator.add(5, 7)
    assert result equals 12
```

**Step 4: Proper implementation (Green)**

```pseudo
class Calculator:
    function add(a, b):
        return a + b
```

**Step 5: Refactor**

```pseudo
class Calculator:
    function add(a, b):
        validateNumbers(a, b)
        return a + b
    
    function validateNumbers(a, b):
        if not isNumber(a) or not isNumber(b):
            throw Error("Arguments must be numbers")
```

### Benefits of TDD

1. **Better design**: Forces thinking about interfaces first
2. **Built-in tests**: Tests exist before code
3. **Confidence**: Know immediately when something breaks
4. **Documentation**: Tests show how code should be used
5. **Less debugging**: Catches errors early

## Test Pyramid

### Structure

```
        /\
       /  \  E2E (10%)
      /    \
     /------\ Integration (20%)
    /        \
   /----------\ Unit (70%)
  /            \
```

### Layer Breakdown

**Unit Tests (70%)**
- Fast (milliseconds)
- Isolated (single function/class)
- Many tests
- Cheap to maintain

**Integration Tests (20%)**
- Medium speed (seconds)
- Test component interactions
- Moderate quantity
- Medium maintenance cost

**E2E Tests (10%)**
- Slow (minutes)
- Test entire system
- Few tests
- Expensive to maintain

### Example Pyramid

```pseudo
Unit Tests (500 tests):
- test Calculator.add()
- test UserValidator.validateEmail()
- test OrderProcessor.calculateTotal()

Integration Tests (100 tests):
- test UserService with UserRepository
- test PaymentProcessor with PaymentGateway
- test OrderService with InventoryService

E2E Tests (20 tests):
- test complete checkout flow
- test user registration and login
- test order placement and fulfillment
```

## Types of Tests

### 1. Unit Tests

**Definition:** Test individual units (functions, methods, classes) in isolation.

```pseudo
class StringUtilsTests:
    
    test "capitalize should capitalize first letter":
        result = StringUtils.capitalize("hello")
        assert result equals "Hello"
    
    test "capitalize should handle empty string":
        result = StringUtils.capitalize("")
        assert result equals ""
    
    test "capitalize should handle null":
        expect StringUtils.capitalize(null) to throw Error
```

### 2. Integration Tests

**Definition:** Test interactions between multiple units or components.

```pseudo
class UserServiceIntegrationTests:
    database, userService
    
    setup:
        database = new TestDatabase()
        userService = new UserService(database)
    
    test "create user should save to database":
        user = {username: "john", email: "john@example.com"}
        createdUser = userService.createUser(user)
        
        savedUser = database.findById(createdUser.id)
        assert savedUser is not null
        assert savedUser.username equals "john"
    
    teardown:
        database.clear()
```

### 3. Functional Tests

**Definition:** Test specific functionality from user's perspective.

```pseudo
class LoginFunctionalTests:
    
    test "user can login with valid credentials":
        page = navigateTo("/login")
        page.enterUsername("john")
        page.enterPassword("password123")
        page.clickLoginButton()
        
        assert page.isOnDashboard()
        assert page.showsWelcomeMessage("Welcome, john")
    
    test "user cannot login with invalid credentials":
        page = navigateTo("/login")
        page.enterUsername("john")
        page.enterPassword("wrongpassword")
        page.clickLoginButton()
        
        assert page.isOnLoginPage()
        assert page.showsError("Invalid credentials")
```

### 4. End-to-End Tests

**Definition:** Test complete workflows through entire system.

```pseudo
class CheckoutE2ETests:
    
    test "complete purchase flow":
        loginAs("customer@example.com", "password")
        
        navigateTo("/products")
        addToCart("Product A")
        addToCart("Product B")
        
        navigateTo("/cart")
        assert cartContains("Product A", "Product B")
        
        clickCheckout()
        enterShippingAddress("123 Main St")
        enterPaymentInfo("4111111111111111")
        submitOrder()
        
        assert orderConfirmationDisplayed()
        assert emailReceived("Order Confirmation")
```

### 5. Acceptance Tests

**Definition:** Validate that requirements are met from business perspective.

```pseudo
feature "Shopping Cart":
    scenario "User adds items to cart":
        given user is logged in
        when user adds "Laptop" to cart
        and user adds "Mouse" to cart
        then cart should contain 2 items
        and total should be $1050
    
    scenario "User removes item from cart":
        given user has "Laptop" in cart
        when user removes "Laptop" from cart
        then cart should be empty
        and total should be $0
```

## Test Doubles

### 1. Mock

**Definition:** Object that verifies interactions (method calls, arguments).

```pseudo
test "order service should notify customer":
    mockEmailService = createMock(EmailService)
    orderService = new OrderService(mockEmailService)
    
    order = createTestOrder()
    orderService.placeOrder(order)
    
    verify mockEmailService.sendEmail was called once
    verify mockEmailService.sendEmail was called with order.customer.email
```

### 2. Stub

**Definition:** Object that provides predefined responses.

```pseudo
test "payment processing with approved payment":
    stubPaymentGateway = createStub(PaymentGateway)
    stubPaymentGateway.processPayment returns {status: "approved"}
    
    orderService = new OrderService(stubPaymentGateway)
    result = orderService.checkout(order)
    
    assert result.success equals true
```

### 3. Fake

**Definition:** Simplified working implementation for testing.

```pseudo
class FakeDatabase implements Database:
    data = {}
    
    function save(entity):
        this.data[entity.id] = entity
    
    function findById(id):
        return this.data[id]
    
    function clear():
        this.data = {}

test "user service with fake database":
    fakeDb = new FakeDatabase()
    userService = new UserService(fakeDb)
    
    user = userService.create({username: "john"})
    found = userService.findById(user.id)
    
    assert found.username equals "john"
```

### 4. Spy

**Definition:** Real object that records interactions.

```pseudo
test "logger spy records messages":
    logger = spy(new Logger())
    service = new Service(logger)
    
    service.processRequest()
    
    assert logger.log was called 3 times
    assert logger.log.firstCall.args[0] equals "Processing started"
```

### Test Double Comparison

```pseudo
Real Object:
  emailService.send("test@example.com", "Hello")
  → Actually sends email

Mock:
  mockEmailService.send("test@example.com", "Hello")
  → Records call, verifies it happened

Stub:
  stubEmailService.send() returns true
  → Always returns predefined value

Fake:
  fakeEmailService.send() adds to inbox array
  → Simple working implementation

Spy:
  spyEmailService.send() calls real method AND records
  → Real behavior + tracking
```

## Code Coverage

### Types of Coverage

**1. Line Coverage**

```pseudo
function calculate(a, b, operation):
    if operation == "add":
        return a + b        ← covered
    else if operation == "subtract":
        return a - b        ← not covered
    else:
        return 0            ← not covered

test "addition":
    result = calculate(5, 3, "add")
    assert result equals 8

Line coverage: 3/5 = 60%
```

**2. Branch Coverage**

```pseudo
function isValid(user):
    if user is null:         ← branch 1
        return false
    
    if user.age < 18:        ← branch 2
        return false
    
    return true

test "valid user":
    assert isValid({age: 25}) equals true

test "null user":
    assert isValid(null) equals false

Branch coverage: 3/4 = 75% (missing age < 18 branch)
```

**3. Path Coverage**

```pseudo
function process(a, b):
    if a > 0:              ← decision 1
        if b > 0:          ← decision 2
            return "both positive"
        else:
            return "a positive, b negative"
    else:
        if b > 0:
            return "a negative, b positive"
        else:
            return "both negative"

Possible paths: 4
Tests needed for 100% path coverage: 4

test paths:
1. a > 0, b > 0
2. a > 0, b <= 0
3. a <= 0, b > 0
4. a <= 0, b <= 0
```

### Coverage Guidelines

```
< 60%: Poor coverage
60-75%: Acceptable
75-85%: Good
85-95%: Very good
> 95%: Excellent (but beware of diminishing returns)
```

### Coverage Limitations

```pseudo
function divide(a, b):
    return a / b

test "division":
    result = divide(10, 2)
    assert result equals 5

Coverage: 100%
But missing: divide by zero test!
```

## Testing Best Practices

### AAA Pattern (Arrange-Act-Assert)

```pseudo
test "user creation":
    ARRANGE:
        database = new TestDatabase()
        userService = new UserService(database)
        userData = {username: "john", email: "john@example.com"}
    
    ACT:
        user = userService.createUser(userData)
    
    ASSERT:
        assert user.id is not null
        assert user.username equals "john"
        assert user.email equals "john@example.com"
```

### Test Isolation

**Bad (Tests depend on each other):**

```pseudo
sharedUser = null

test "create user":
    sharedUser = createUser("john")
    assert sharedUser is not null

test "update user":
    sharedUser.email = "new@example.com"
    updateUser(sharedUser)
    assert sharedUser.email equals "new@example.com"
```

**Good (Tests are independent):**

```pseudo
test "create user":
    user = createUser("john")
    assert user is not null

test "update user":
    user = createUser("jane")
    user.email = "new@example.com"
    updateUser(user)
    
    updated = findUser(user.id)
    assert updated.email equals "new@example.com"
```

### FIRST Properties

**F - Fast**

```pseudo
Good: Unit test runs in < 10ms
Bad: Test queries production database (500ms)
```

**I - Independent**

```pseudo
Good: Each test can run in any order
Bad: Test 2 depends on state from Test 1
```

**R - Repeatable**

```pseudo
Good: Test produces same result every time
Bad: Test depends on current time/date
```

**S - Self-validating**

```pseudo
Good: Test clearly passes or fails
Bad: Test requires manual inspection
```

**T - Timely**

```pseudo
Good: Write tests with (or before) code
Bad: Write tests months after implementation
```

### One Assertion Per Test

**Bad:**

```pseudo
test "user validation":
    user = createUser("john", "john@example.com", 25)
    assert user.username equals "john"
    assert user.email equals "john@example.com"
    assert user.age equals 25
```

**Good:**

```pseudo
test "user should have correct username":
    user = createUser("john", "john@example.com", 25)
    assert user.username equals "john"

test "user should have correct email":
    user = createUser("john", "john@example.com", 25)
    assert user.email equals "john@example.com"

test "user should have correct age":
    user = createUser("john", "john@example.com", 25)
    assert user.age equals 25
```

### Test Naming Conventions

```pseudo
Pattern: test_[method]_[scenario]_[expectedResult]

Good names:
- test_add_positiveNumbers_returnsSum
- test_divide_byZero_throwsException
- test_createUser_duplicateUsername_returnsFalse
- test_authenticate_invalidPassword_returnsNull

Bad names:
- test1
- testAddition
- testUserStuff
```

### Setup and Teardown

```pseudo
class DatabaseTests:
    database, connection
    
    setup:
        connection = createConnection()
        database = new Database(connection)
        database.migrate()
    
    test "insert record":
        database.insert({name: "John"})
        count = database.count()
        assert count equals 1
    
    test "delete record":
        database.insert({name: "Jane"})
        database.delete({name: "Jane"})
        count = database.count()
        assert count equals 0
    
    teardown:
        database.clear()
        connection.close()
```

### Test Data Builders

```pseudo
class UserBuilder:
    username = "default_user"
    email = "default@example.com"
    age = 18
    
    function withUsername(username):
        this.username = username
        return this
    
    function withEmail(email):
        this.email = email
        return this
    
    function withAge(age):
        this.age = age
        return this
    
    function build():
        return new User(this.username, this.email, this.age)

test "user with custom username":
    user = new UserBuilder()
        .withUsername("john")
        .build()
    assert user.username equals "john"
```

## Practical Testing Examples

### Example 1: Testing with Mocks

```pseudo
class OrderServiceTests:
    
    test "placing order sends confirmation email":
        mockEmailService = mock(EmailService)
        mockInventory = mock(InventoryService)
        orderService = new OrderService(mockEmailService, mockInventory)
        
        order = createTestOrder({
            customer: {email: "customer@example.com"},
            items: [{id: 1, quantity: 2}]
        })
        
        orderService.placeOrder(order)
        
        verify mockEmailService.sendEmail(
            "customer@example.com",
            contains("Order Confirmation")
        )
```

### Example 2: Parameterized Tests

```pseudo
testCases = [
    {input: 0, expected: 0},
    {input: 1, expected: 1},
    {input: 2, expected: 2},
    {input: 3, expected: 6},
    {input: 4, expected: 24},
    {input: 5, expected: 120}
]

for testCase in testCases:
    test "factorial of " + testCase.input:
        result = factorial(testCase.input)
        assert result equals testCase.expected
```

### Example 3: Testing Async Code

```pseudo
test "async data fetching":
    mockApi = mock(ApiClient)
    mockApi.fetchUser(123) returns Promise.resolve({id: 123, name: "John"})
    
    service = new UserService(mockApi)
    user = await service.getUser(123)
    
    assert user.id equals 123
    assert user.name equals "John"
```

### Example 4: Testing Exceptions

```pseudo
test "division by zero throws exception":
    calculator = new Calculator()
    
    expect calculator.divide(10, 0) to throw DivisionByZeroError
    expect calculator.divide(10, 0) to throw error with message "Cannot divide by zero"
```

### Example 5: Integration Test with Database

```pseudo
class UserRepositoryIntegrationTests:
    database, repository
    
    setup:
        database = createTestDatabase()
        repository = new UserRepository(database)
    
    test "save and retrieve user":
        user = new User("john", "john@example.com")
        savedUser = repository.save(user)
        
        assert savedUser.id is not null
        
        retrievedUser = repository.findById(savedUser.id)
        assert retrievedUser.username equals "john"
        assert retrievedUser.email equals "john@example.com"
    
    test "update user":
        user = repository.save(new User("jane", "jane@example.com"))
        user.email = "newemail@example.com"
        
        repository.update(user)
        
        updated = repository.findById(user.id)
        assert updated.email equals "newemail@example.com"
    
    teardown:
        database.clear()
        database.close()
```

## Testing Anti-Patterns

### 1. Testing Implementation Details

```pseudo
Bad:
test "user service uses cache":
    userService = new UserService()
    userService.getUser(123)
    assert userService.cache.contains(123)

Good:
test "user service returns user":
    userService = new UserService()
    user = userService.getUser(123)
    assert user.id equals 123
```

### 2. Flaky Tests

```pseudo
Bad:
test "async operation":
    startAsyncOperation()
    wait(100)
    assert operation is complete

Good:
test "async operation":
    promise = startAsyncOperation()
    await promise
    assert operation is complete
```

### 3. Testing Too Much

```pseudo
Bad:
test "calculator add":
    calculator = new Calculator()
    assert calculator.add(1, 1) equals 2
    assert calculator.add(2, 2) equals 4
    assert calculator.add(5, 5) equals 10
    assert calculator.subtract(5, 3) equals 2
    assert calculator.multiply(3, 4) equals 12

Good:
test "calculator add":
    calculator = new Calculator()
    assert calculator.add(2, 3) equals 5

test "calculator subtract":
    calculator = new Calculator()
    assert calculator.subtract(5, 3) equals 2
```

## Summary

Effective testing requires:

1. **TDD Cycle**: Red-Green-Refactor
2. **Test Pyramid**: 70% unit, 20% integration, 10% E2E
3. **Test Types**: Unit, integration, functional, E2E, acceptance
4. **Test Doubles**: Mocks, stubs, fakes, spies
5. **Coverage**: Line, branch, path (aim for 75-85%)
6. **FIRST Principles**: Fast, Independent, Repeatable, Self-validating, Timely
7. **AAA Pattern**: Arrange-Act-Assert

Write tests that are clear, isolated, and maintainable. Tests are documentation and safety net.
