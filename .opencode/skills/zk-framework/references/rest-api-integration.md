# ZK Framework + REST API Integration

Guide to consuming and exposing REST APIs with ZK Framework applications.

## Table of Contents

1. [Client-Side REST Consumption](#client-side-rest-consumption)
2. [Jersey JAX-RS Integration](#jersey-jax-rs-integration)
3. [Async REST Calls](#async-rest-calls)
4. [Error Handling](#error-handling)
5. [Authentication](#authentication)
6. [Best Practices](#best-practices)

## Client-Side REST Consumption

### Maven Dependencies

```xml
<!-- JAX-RS API -->
<dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>2.1.1</version>
</dependency>

<!-- Jersey Client -->
<dependency>
    <groupId>org.glassfish.jersey.core</groupId>
    <artifactId>jersey-client</artifactId>
    <version>2.39.1</version>
</dependency>

<dependency>
    <groupId>org.glassfish.jersey.inject</groupId>
    <artifactId>jersey-hk2</artifactId>
    <version>2.39.1</version>
</dependency>

<!-- JSON Support -->
<dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
    <version>2.39.1</version>
</dependency>
```

### REST Client Service

```java
package com.example.service;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

public class RestClientService {
    
    private final Client client;
    private final String baseUrl;
    
    public RestClientService(String baseUrl) {
        this.client = ClientBuilder.newClient();
        this.baseUrl = baseUrl;
    }
    
    public <T> T get(String path, Class<T> responseType) {
        WebTarget target = client.target(baseUrl).path(path);
        
        Response response = target.request(MediaType.APPLICATION_JSON).get();
        
        if (response.getStatus() == 200) {
            return response.readEntity(responseType);
        } else {
            throw new RuntimeException("Failed: HTTP " + response.getStatus());
        }
    }
    
    public <T> T post(String path, Object entity, Class<T> responseType) {
        WebTarget target = client.target(baseUrl).path(path);
        
        Response response = target.request(MediaType.APPLICATION_JSON)
                                  .post(Entity.json(entity));
        
        if (response.getStatus() == 200 || response.getStatus() == 201) {
            return response.readEntity(responseType);
        } else {
            throw new RuntimeException("Failed: HTTP " + response.getStatus());
        }
    }
    
    public <T> T put(String path, Object entity, Class<T> responseType) {
        WebTarget target = client.target(baseUrl).path(path);
        
        Response response = target.request(MediaType.APPLICATION_JSON)
                                  .put(Entity.json(entity));
        
        if (response.getStatus() == 200) {
            return response.readEntity(responseType);
        } else {
            throw new RuntimeException("Failed: HTTP " + response.getStatus());
        }
    }
    
    public void delete(String path) {
        WebTarget target = client.target(baseUrl).path(path);
        
        Response response = target.request().delete();
        
        if (response.getStatus() != 204 && response.getStatus() != 200) {
            throw new RuntimeException("Failed: HTTP " + response.getStatus());
        }
    }
    
    public void close() {
        client.close();
    }
}
```

### ViewModel with REST Calls

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import org.zkoss.zul.Messagebox;
import com.example.service.RestClientService;
import com.example.dto.UserDTO;
import java.util.List;
import java.util.Arrays;

public class UserRestVM {
    
    private RestClientService restClient;
    private List<UserDTO> users;
    private UserDTO selectedUser = new UserDTO();
    
    @Init
    public void init() {
        restClient = new RestClientService("http://localhost:8080/api");
        loadUsers();
    }
    
    @Command
    @NotifyChange("users")
    public void loadUsers() {
        try {
            UserDTO[] usersArray = restClient.get("/users", UserDTO[].class);
            users = Arrays.asList(usersArray);
        } catch (Exception e) {
            Messagebox.show("Error loading users: " + e.getMessage(), 
                          "Error", Messagebox.OK, Messagebox.ERROR);
        }
    }
    
    @Command
    @NotifyChange({"users", "selectedUser"})
    public void saveUser() {
        try {
            if (selectedUser.getId() == null) {
                restClient.post("/users", selectedUser, UserDTO.class);
            } else {
                restClient.put("/users/" + selectedUser.getId(), 
                             selectedUser, UserDTO.class);
            }
            
            selectedUser = new UserDTO();
            loadUsers();
            Messagebox.show("User saved successfully", "Success", 
                          Messagebox.OK, Messagebox.INFORMATION);
        } catch (Exception e) {
            Messagebox.show("Error saving user: " + e.getMessage(), 
                          "Error", Messagebox.OK, Messagebox.ERROR);
        }
    }
    
    @Command
    @NotifyChange({"users", "selectedUser"})
    public void deleteUser(@BindingParam("user") UserDTO user) {
        try {
            restClient.delete("/users/" + user.getId());
            selectedUser = new UserDTO();
            loadUsers();
            Messagebox.show("User deleted successfully", "Success", 
                          Messagebox.OK, Messagebox.INFORMATION);
        } catch (Exception e) {
            Messagebox.show("Error deleting user: " + e.getMessage(), 
                          "Error", Messagebox.OK, Messagebox.ERROR);
        }
    }
    
    public List<UserDTO> getUsers() {
        return users;
    }
    
    public UserDTO getSelectedUser() {
        return selectedUser;
    }
    
    public void setSelectedUser(UserDTO selectedUser) {
        this.selectedUser = selectedUser;
    }
    
    @Destroy
    public void cleanup() {
        if (restClient != null) {
            restClient.close();
        }
    }
}
```

### DTO Classes

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UserDTO {
    
    @JsonProperty("id")
    private Long id;
    
    @JsonProperty("name")
    private String name;
    
    @JsonProperty("email")
    private String email;
    
    @JsonProperty("active")
    private boolean active;
    
    public UserDTO() {}
    
    public UserDTO(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.active = true;
    }
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
}
```

## Jersey JAX-RS Integration

### JAX-RS Resource

```java
package com.example.rest;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.example.service.UserService;
import com.example.dto.UserDTO;
import java.util.List;

@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {
    
    private final UserService userService;
    
    public UserResource() {
        this.userService = new UserService();
    }
    
    @GET
    public Response getAllUsers() {
        List<UserDTO> users = userService.findAll();
        return Response.ok(users).build();
    }
    
    @GET
    @Path("/{id}")
    public Response getUserById(@PathParam("id") Long id) {
        UserDTO user = userService.findById(id);
        
        if (user == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.ok(user).build();
    }
    
    @POST
    public Response createUser(UserDTO user) {
        UserDTO created = userService.create(user);
        return Response.status(Response.Status.CREATED).entity(created).build();
    }
    
    @PUT
    @Path("/{id}")
    public Response updateUser(@PathParam("id") Long id, UserDTO user) {
        user.setId(id);
        UserDTO updated = userService.update(user);
        
        if (updated == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.ok(updated).build();
    }
    
    @DELETE
    @Path("/{id}")
    public Response deleteUser(@PathParam("id") Long id) {
        boolean deleted = userService.delete(id);
        
        if (!deleted) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.noContent().build();
    }
    
    @GET
    @Path("/search")
    public Response searchUsers(@QueryParam("name") String name) {
        List<UserDTO> users = userService.findByName(name);
        return Response.ok(users).build();
    }
}
```

### Jersey Servlet Configuration

```xml
<!-- web.xml -->
<servlet>
    <servlet-name>Jersey REST Service</servlet-name>
    <servlet-class>org.glassfish.jersey.servlet.ServletContainer</servlet-class>
    <init-param>
        <param-name>jersey.config.server.provider.packages</param-name>
        <param-value>com.example.rest</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>Jersey REST Service</servlet-name>
    <url-pattern>/api/*</url-pattern>
</servlet-mapping>
```

### Application Configuration

```java
package com.example.rest;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;
import java.util.Set;
import java.util.HashSet;

@ApplicationPath("/api")
public class RestApplication extends Application {
    
    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> classes = new HashSet<>();
        classes.add(UserResource.class);
        classes.add(ProductResource.class);
        return classes;
    }
}
```

## Async REST Calls

### Async Client with CompletableFuture

```java
package com.example.service;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.InvocationCallback;
import java.util.concurrent.CompletableFuture;

public class AsyncRestClientService {
    
    private final Client client;
    private final String baseUrl;
    
    public AsyncRestClientService(String baseUrl) {
        this.client = ClientBuilder.newClient();
        this.baseUrl = baseUrl;
    }
    
    public <T> CompletableFuture<T> getAsync(String path, Class<T> responseType) {
        CompletableFuture<T> future = new CompletableFuture<>();
        
        client.target(baseUrl)
              .path(path)
              .request()
              .async()
              .get(new InvocationCallback<T>() {
                  @Override
                  public void completed(T response) {
                      future.complete(response);
                  }
                  
                  @Override
                  public void failed(Throwable throwable) {
                      future.completeExceptionally(throwable);
                  }
              });
        
        return future;
    }
}
```

### Async ViewModel

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.event.Event;
import org.zkoss.zk.ui.event.EventListener;
import org.zkoss.zk.ui.util.Clients;
import com.example.service.AsyncRestClientService;
import com.example.dto.UserDTO;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class AsyncUserVM {
    
    private AsyncRestClientService restClient;
    private List<UserDTO> users;
    private boolean loading = false;
    
    @Init
    public void init() {
        restClient = new AsyncRestClientService("http://localhost:8080/api");
        loadUsersAsync();
    }
    
    @Command
    @NotifyChange({"loading", "users"})
    public void loadUsersAsync() {
        loading = true;
        
        CompletableFuture<UserDTO[]> future = 
            restClient.getAsync("/users", UserDTO[].class);
        
        future.thenAccept(usersArray -> {
            users = Arrays.asList(usersArray);
            loading = false;
            notifyChange();
        }).exceptionally(throwable -> {
            loading = false;
            Clients.showNotification("Error: " + throwable.getMessage(), 
                                   "error", null, null, 0);
            notifyChange();
            return null;
        });
    }
    
    private void notifyChange() {
        BindUtils.postNotifyChange(null, null, this, "users");
        BindUtils.postNotifyChange(null, null, this, "loading");
    }
    
    public List<UserDTO> getUsers() {
        return users;
    }
    
    public boolean isLoading() {
        return loading;
    }
}
```

## Error Handling

### Custom Exception Mapper

```java
package com.example.rest.exception;

import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

@Provider
public class GenericExceptionMapper implements ExceptionMapper<Exception> {
    
    @Override
    public Response toResponse(Exception exception) {
        ErrorMessage errorMessage = new ErrorMessage(
            exception.getMessage(),
            Response.Status.INTERNAL_SERVER_ERROR.getStatusCode()
        );
        
        return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                       .entity(errorMessage)
                       .build();
    }
}

class ErrorMessage {
    private String message;
    private int status;
    
    public ErrorMessage(String message, int status) {
        this.message = message;
        this.status = status;
    }
    
    public String getMessage() { return message; }
    public int getStatus() { return status; }
}
```

### Enhanced REST Client with Error Handling

```java
package com.example.service;

import javax.ws.rs.client.Client;
import javax.ws.rs.core.Response;

public class EnhancedRestClientService {
    
    private final Client client;
    private final String baseUrl;
    
    public <T> T get(String path, Class<T> responseType) {
        Response response = null;
        
        try {
            response = client.target(baseUrl)
                           .path(path)
                           .request(MediaType.APPLICATION_JSON)
                           .get();
            
            return handleResponse(response, responseType);
        } finally {
            if (response != null) {
                response.close();
            }
        }
    }
    
    private <T> T handleResponse(Response response, Class<T> responseType) {
        int status = response.getStatus();
        
        if (status >= 200 && status < 300) {
            return response.readEntity(responseType);
        } else if (status == 404) {
            throw new NotFoundException("Resource not found");
        } else if (status == 401) {
            throw new UnauthorizedException("Unauthorized");
        } else if (status == 403) {
            throw new ForbiddenException("Forbidden");
        } else if (status >= 400 && status < 500) {
            String errorMsg = response.readEntity(String.class);
            throw new ClientErrorException("Client error: " + errorMsg, status);
        } else {
            throw new ServerErrorException("Server error", status);
        }
    }
}
```

## Authentication

### Bearer Token Authentication

```java
package com.example.service;

import javax.ws.rs.client.ClientRequestContext;
import javax.ws.rs.client.ClientRequestFilter;
import javax.ws.rs.core.HttpHeaders;

public class BearerAuthFilter implements ClientRequestFilter {
    
    private final String token;
    
    public BearerAuthFilter(String token) {
        this.token = token;
    }
    
    @Override
    public void filter(ClientRequestContext requestContext) {
        requestContext.getHeaders().add(
            HttpHeaders.AUTHORIZATION, 
            "Bearer " + token
        );
    }
}
```

```java
public class AuthenticatedRestClient {
    
    private final Client client;
    private final String baseUrl;
    
    public AuthenticatedRestClient(String baseUrl, String token) {
        this.client = ClientBuilder.newClient();
        this.client.register(new BearerAuthFilter(token));
        this.baseUrl = baseUrl;
    }
    
    public <T> T get(String path, Class<T> responseType) {
        return client.target(baseUrl)
                    .path(path)
                    .request(MediaType.APPLICATION_JSON)
                    .get(responseType);
    }
}
```

### Basic Authentication

```java
import javax.ws.rs.core.HttpHeaders;
import java.util.Base64;

public class BasicAuthFilter implements ClientRequestFilter {
    
    private final String username;
    private final String password;
    
    public BasicAuthFilter(String username, String password) {
        this.username = username;
        this.password = password;
    }
    
    @Override
    public void filter(ClientRequestContext requestContext) {
        String credentials = username + ":" + password;
        String encoded = Base64.getEncoder().encodeToString(
            credentials.getBytes()
        );
        
        requestContext.getHeaders().add(
            HttpHeaders.AUTHORIZATION,
            "Basic " + encoded
        );
    }
}
```

## Best Practices

### Practice 1: Connection Pooling

```java
public class RestClientFactory {
    
    private static Client client;
    
    public static synchronized Client getClient() {
        if (client == null) {
            ClientConfig config = new ClientConfig();
            config.property(ClientProperties.CONNECT_TIMEOUT, 5000);
            config.property(ClientProperties.READ_TIMEOUT, 30000);
            
            client = ClientBuilder.newClient(config);
            client.register(JacksonJsonProvider.class);
        }
        return client;
    }
}
```

### Practice 2: Request Timeouts

```java
WebTarget target = client.target(baseUrl).path(path);

Response response = target.request()
    .property(ClientProperties.CONNECT_TIMEOUT, 5000)
    .property(ClientProperties.READ_TIMEOUT, 10000)
    .get();
```

### Practice 3: Response Caching

```java
public class CachedRestClient {
    
    private final RestClientService restClient;
    private final Map<String, CacheEntry> cache = new ConcurrentHashMap<>();
    private final long cacheTimeoutMs;
    
    public CachedRestClient(String baseUrl, long cacheTimeoutMs) {
        this.restClient = new RestClientService(baseUrl);
        this.cacheTimeoutMs = cacheTimeoutMs;
    }
    
    public <T> T get(String path, Class<T> responseType) {
        CacheEntry entry = cache.get(path);
        
        if (entry != null && !entry.isExpired()) {
            return (T) entry.getData();
        }
        
        T data = restClient.get(path, responseType);
        cache.put(path, new CacheEntry(data, cacheTimeoutMs));
        
        return data;
    }
    
    static class CacheEntry {
        private final Object data;
        private final long expiryTime;
        
        CacheEntry(Object data, long timeoutMs) {
            this.data = data;
            this.expiryTime = System.currentTimeMillis() + timeoutMs;
        }
        
        boolean isExpired() {
            return System.currentTimeMillis() > expiryTime;
        }
        
        Object getData() {
            return data;
        }
    }
}
```
