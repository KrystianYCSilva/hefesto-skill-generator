# ZK Framework Migration Guide

Comprehensive guide for migrating ZK applications across major versions.

## Table of Contents

1. [ZK 3.x to 6.x Migration](#zk-3x-to-6x-migration)
2. [ZK 6.x to 8.x Migration](#zk-6x-to-8x-migration)
3. [ZK 8.x to 10.x Migration](#zk-8x-to-10x-migration)
4. [Breaking Changes](#breaking-changes)
5. [Best Practices](#best-practices)

## ZK 3.x to 6.x Migration

### Major Changes

1. MVC to MVVM pattern introduction
2. Data binding syntax changes
3. Component API updates
4. Event handling improvements

### Composer Migration

```java
// ZK 3.x - GenericForwardComposer
public class UserComposer extends GenericForwardComposer {
    
    private Listbox userListbox;
    
    public void onCreate$win(Event event) {
        loadUsers();
    }
    
    public void onClick$addButton(Event event) {
        addUser();
    }
    
    private void loadUsers() {
        List<User> users = getUsersFromDB();
        userListbox.setModel(new ListModelList(users));
    }
}
```

```java
// ZK 6.x - SelectorComposer
public class UserComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox userListbox;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        loadUsers();
    }
    
    @Listen("onClick = #addButton")
    public void onAddUser() {
        addUser();
    }
    
    private void loadUsers() {
        List<User> users = getUsersFromDB();
        userListbox.setModel(new ListModelList<User>(users));
    }
}
```

### Data Binding Migration

```xml
<!-- ZK 3.x - Annotated Data Binding -->
<window id="win" apply="com.example.UserComposer">
    <listbox id="userListbox">
        <listitem self="@{each='user'}" value="@{user}">
            <listcell label="@{user.name}" />
            <listcell label="@{user.email}" />
        </listitem>
    </listbox>
</window>
```

```xml
<!-- ZK 6.x - MVVM Data Binding -->
<window viewModel="@id('vm') @init('com.example.UserVM')">
    <listbox model="@load(vm.users)">
        <template name="model">
            <listitem>
                <listcell label="@load(each.name)" />
                <listcell label="@load(each.email)" />
            </listitem>
        </template>
    </listbox>
</window>
```

### Event Handling

```java
// ZK 3.x - Forward events
public class UserComposer extends GenericForwardComposer {
    
    public void onSelect$userListbox(Event event) {
        Listitem selected = userListbox.getSelectedItem();
        showUserDetails(selected.getValue());
    }
}
```

```java
// ZK 6.x - @Listen annotation
public class UserComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox userListbox;
    
    @Listen("onSelect = #userListbox")
    public void onSelectUser() {
        User selected = userListbox.getSelectedItem().getValue();
        showUserDetails(selected);
    }
}
```

### Component Changes

```java
// ZK 3.x
Window win = new Window();
win.setTitle("User Management");
win.setBorder("normal");
win.setWidth("600px");

// ZK 6.x - Same API maintained
Window win = new Window();
win.setTitle("User Management");
win.setBorder("normal");
win.setWidth("600px");
```

## ZK 6.x to 8.x Migration

### Packaging Changes

```xml
<!-- ZK 6.x -->
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zk</artifactId>
    <version>6.5.10</version>
</dependency>
```

```xml
<!-- ZK 8.x -->
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zkbind</artifactId>
    <version>8.6.4</version>
</dependency>
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zul</artifactId>
    <version>8.6.4</version>
</dependency>
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zkplus</artifactId>
    <version>8.6.4</version>
</dependency>
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zhtml</artifactId>
    <version>8.6.4</version>
</dependency>
```

### Lambda Expression Support

```java
// ZK 6.x
@Listen("onClick = #saveButton")
public void onSave() {
    users.forEach(new Consumer<User>() {
        @Override
        public void accept(User user) {
            userService.save(user);
        }
    });
}
```

```java
// ZK 8.x - Lambda support
@Listen("onClick = #saveButton")
public void onSave() {
    users.forEach(user -> userService.save(user));
}
```

### Shadow Elements

```xml
<!-- ZK 6.x - <forEach> creates actual components -->
<listbox>
    <forEach items="@load(vm.users)">
        <listitem>
            <listcell label="@load(each.name)" />
        </listitem>
    </forEach>
</listbox>
```

```xml
<!-- ZK 8.x - Template (shadow elements, better performance) -->
<listbox model="@load(vm.users)">
    <template name="model">
        <listitem>
            <listcell label="@load(each.name)" />
        </listitem>
    </template>
</listbox>
```

### Client Binding

```java
// ZK 6.x - Server-side only
public class UserVM {
    
    private String name;
    
    @Command
    @NotifyChange("name")
    public void updateName() {
        name = "John Doe";
    }
    
    public String getName() {
        return name;
    }
}
```

```java
// ZK 8.x - Client binding support
public class UserVM {
    
    private String name;
    
    @Command
    @NotifyChange("name")
    public void updateName() {
        name = "John Doe";
    }
    
    public String getName() {
        return name;
    }
}
```

```xml
<!-- ZK 8.x - Client binding -->
<textbox value="@bind(vm.name)" instant="true" />
```

### Modern Java Support

```java
// ZK 8.x - Java 8+ features
public class ProductVM {
    
    private List<Product> products;
    
    @Init
    public void init() {
        products = productService.findAll();
    }
    
    public List<Product> getActiveProducts() {
        return products.stream()
            .filter(Product::isActive)
            .sorted(Comparator.comparing(Product::getName))
            .collect(Collectors.toList());
    }
    
    @DependsOn("products")
    public BigDecimal getTotalValue() {
        return products.stream()
            .map(Product::getPrice)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

## ZK 8.x to 10.x Migration

### Java Version Requirements

```xml
<!-- ZK 8.x - Java 6+ -->
<properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```

```xml
<!-- ZK 10.x - Java 11+ -->
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
</properties>
```

### Maven Dependencies Update

```xml
<!-- ZK 8.x -->
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zkbind</artifactId>
    <version>8.6.4</version>
</dependency>
```

```xml
<!-- ZK 10.x -->
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zkbind</artifactId>
    <version>10.0.0</version>
</dependency>
```

### Bootstrap Theme

```xml
<!-- ZK 8.x - Atlantic theme -->
<library-property>
    <name>org.zkoss.theme.preferred</name>
    <value>atlantic</value>
</library-property>
```

```xml
<!-- ZK 10.x - Bootstrap theme available -->
<library-property>
    <name>org.zkoss.theme.preferred</name>
    <value>bootstrap</value>
</library-property>
```

### Responsive Design Support

```xml
<!-- ZK 10.x - Enhanced responsive utilities -->
<div sclass="row">
    <div sclass="col-md-6">
        <textbox hflex="1" />
    </div>
    <div sclass="col-md-6">
        <button label="Submit" />
    </div>
</div>
```

### Modern JavaScript Integration

```javascript
// ZK 10.x - Better ES6+ support
zk.afterMount(function() {
    const element = jq('#myComponent');
    
    element.on('click', (event) => {
        console.log('Clicked:', event.target);
    });
});
```

### Performance Improvements

```java
// ZK 10.x - Optimized rendering
public class OptimizedVM {
    
    @Init
    public void init() {
        products = new ListModelList<>(productService.findAll());
        products.setMultiple(true);
    }
    
    @Command
    @SmartNotifyChange("products")
    public void updateProducts() {
        List<Product> updated = productService.findRecent();
        products.addAll(updated);
    }
}
```

## Breaking Changes

### ZK 6.x Breaking Changes

1. `GenericForwardComposer` deprecated, use `SelectorComposer`
2. Annotated data binding replaced by MVVM
3. Event forwarding mechanism changed
4. Some component methods renamed

### ZK 8.x Breaking Changes

1. `zk.jar` split into multiple JARs
2. Client engine rewritten
3. Some deprecated APIs removed
4. Theme structure changed

### ZK 10.x Breaking Changes

1. Java 11 minimum requirement
2. Dropped IE11 support
3. Some legacy components removed
4. Updated third-party dependencies

### API Deprecations

```java
// Deprecated in ZK 8.x
public class OldStyle extends GenericForwardComposer {
    public void onCreate$win(Event event) { }
}

// Use instead
public class NewStyle extends SelectorComposer<Component> {
    @Listen("onCreate = #win")
    public void onWinCreate() { }
}
```

### Component Changes

```java
// ZK 6.x
Messagebox.show("Message", "Title", Messagebox.OK, Messagebox.INFORMATION);

// ZK 8.x onwards - Same API
Messagebox.show("Message", "Title", Messagebox.OK, Messagebox.INFORMATION);

// ZK 10.x - Additional options
Messagebox.show("Message", "Title", 
    new Messagebox.Button[] {Messagebox.Button.OK, Messagebox.Button.CANCEL},
    Messagebox.QUESTION, 
    event -> {
        if (Messagebox.Button.OK.equals(event.getButton())) {
            // OK clicked
        }
    }
);
```

## Best Practices

### Gradual Migration Strategy

1. Update dependencies incrementally
2. Run tests after each change
3. Migrate one module at a time
4. Keep both old and new code temporarily

### Code Compatibility

```java
// Create abstraction layer
public interface UserController {
    void loadUsers();
    void saveUser(User user);
}

// Old implementation
public class LegacyUserController extends GenericForwardComposer 
        implements UserController {
    // Old code
}

// New implementation
public class ModernUserController extends SelectorComposer<Component> 
        implements UserController {
    // New code
}
```

### Testing Strategy

```java
// Unit tests should work across versions
@Test
public void testUserViewModel() {
    UserVM vm = new UserVM();
    vm.init();
    
    assertNotNull(vm.getUsers());
    assertTrue(vm.getUsers().size() > 0);
}
```

### Configuration Management

```xml
<!-- zk.xml - Version-specific settings -->
<zk>
    <!-- ZK 6.x specific -->
    <device-config>
        <device-type>ajax</device-type>
    </device-config>
    
    <!-- ZK 8.x+ specific -->
    <library-property>
        <name>org.zkoss.zk.ui.versionInfo.enabled</name>
        <value>false</value>
    </library-property>
</zk>
```

### Performance Monitoring

```java
public class MigrationMonitor {
    
    private static final Logger logger = LoggerFactory.getLogger(MigrationMonitor.class);
    
    public static void monitorPerformance(String operation, Runnable task) {
        long start = System.currentTimeMillis();
        
        try {
            task.run();
        } finally {
            long duration = System.currentTimeMillis() - start;
            logger.info("{} took {}ms", operation, duration);
            
            if (duration > 1000) {
                logger.warn("{} is slow, consider optimization", operation);
            }
        }
    }
}
```

### Documentation Updates

```java
/**
 * User management ViewModel
 * 
 * @since ZK 6.5
 * @deprecated Since ZK 8.0, use {@link ModernUserVM} instead
 */
@Deprecated
public class LegacyUserVM {
    // Old implementation
}

/**
 * Modern user management ViewModel with enhanced features
 * 
 * @since ZK 8.0
 */
public class ModernUserVM {
    // New implementation
}
```

### Backward Compatibility

```java
public class CompatibilityHelper {
    
    public static boolean isZK8OrHigher() {
        String version = WebApp.getCurrent().getVersion();
        return version.startsWith("8.") || version.startsWith("9.") || 
               version.startsWith("10.");
    }
    
    public static void showMessage(String message) {
        if (isZK8OrHigher()) {
            Clients.showNotification(message);
        } else {
            Messagebox.show(message);
        }
    }
}
```

### Migration Checklist

1. Review release notes for target version
2. Update Maven dependencies
3. Update Java version if required
4. Run automated tests
5. Check deprecated API usage
6. Update composer implementations
7. Migrate data binding syntax
8. Test event handling
9. Verify theme compatibility
10. Performance testing
11. Browser compatibility testing
12. Update documentation

### Common Migration Issues

```java
// Issue: GenericForwardComposer not working
// Solution: Migrate to SelectorComposer

// Issue: Data binding not updating
// Solution: Use @NotifyChange annotation

// Issue: Events not firing
// Solution: Check @Listen syntax

// Issue: Components not found
// Solution: Use @Wire annotation

// Issue: Performance degradation
// Solution: Use template instead of forEach

// Issue: Client-side errors
// Solution: Clear browser cache and update client libs
```
