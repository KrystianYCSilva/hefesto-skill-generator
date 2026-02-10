---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
@Path("/v1/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class OrderResource {
  @POST
  public Response create(CreateOrderRequest req) {
    URI location = URI.create("/v1/orders/" + req.externalId());
    return Response.created(location).entity(service.create(req)).build();
  }
}
```

```kotlin
@Path("/v1/users")
class UserResource(private val service: UserService) {
  @GET
  @Path("/{id}")
  fun get(@PathParam("id") id: String): Response =
    service.find(id)?.let { Response.ok(it).build() } ?: Response.status(404).build()
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

