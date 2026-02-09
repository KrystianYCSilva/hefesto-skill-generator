# Java and Kotlin Usage Examples

```java
@RestController
@RequestMapping("/v1/orders")
class OrderController {
  @PostMapping
  ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
    return ResponseEntity.status(HttpStatus.CREATED).body(service.create(req));
  }
}
```

```kotlin
@RestController
@RequestMapping("/v1/customers")
class CustomerController(private val service: CustomerService) {
  @GetMapping("/{id}")
  fun get(@PathVariable id: UUID): ResponseEntity<CustomerDto> =
    service.find(id)?.let { ResponseEntity.ok(it) } ?: ResponseEntity.notFound().build()
}
```

## Additional Java and Kotlin Tips

- Java: centralize `@ControllerAdvice` with stable error contracts and correlation identifiers.
- Kotlin: use explicit DTO types and avoid platform type leakage from Java libraries.
- Kotlin coroutines: align dispatcher/thread model with the chosen web stack.
