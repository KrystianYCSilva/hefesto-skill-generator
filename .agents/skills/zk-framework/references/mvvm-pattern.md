---
name: mvvm-pattern
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# MVVM Pattern Guide for ZK Framework

This reference provides comprehensive guidance on using the MVVM (Model-View-ViewModel) pattern in ZK Framework.

## Complete MVVM Example

### UserListViewModel.java (ViewModel)
```java
package org.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zk.ui.util.Clients;
import org.zkoss.zul.ListModelList;
import org.example.model.User;
import org.example.service.UserService;
import java.util.List;

public class UserListViewModel {
    
    // Services
    private UserService userService = new UserService();
    
    // Data properties
    private List<User> users;
    private User selectedUser;
    private User editingUser = new User();
    
    // UI state
    private boolean deleteDisabled = true;
    
    // Initialization
    @Init
    public void init() {
        loadUsers();
    }
    
    // Data loading
    @Command
    @NotifyChange({"users", "selectedUser", "editingUser", "deleteDisabled"})
    public void loadUsers() {
        users = userService.findAll();
        selectedUser = null;
        editingUser = new User();
        deleteDisabled = true;
    }
    
    // User selection
    @Command
    @NotifyChange({"selectedUser", "editingUser", "deleteDisabled"})
    public void selectUser(@BindingParam("user") User user) {
        selectedUser = user;
        // Clone for editing
        editingUser = new User();
        editingUser.setId(user.getId());
        editingUser.setName(user.getName());
        editingUser.setEmail(user.getEmail());
        deleteDisabled = false;
    }
    
    // Save user
    @Command
    @NotifyChange({"users", "selectedUser", "editingUser", "deleteDisabled"})
    public void save() {
        if (editingUser.getId() == null) {
            // Create new
            userService.save(editingUser);
            Clients.showNotification("User created successfully!", "info", null, null, 2000);
        } else {
            // Update existing
            userService.update(editingUser);
            Clients.showNotification("User updated successfully!", "info", null, null, 2000);
        }
        loadUsers();
    }
    
    // Delete user
    @Command
    @NotifyChange({"users", "selectedUser", "editingUser", "deleteDisabled"})
    public void delete() {
        if (selectedUser != null) {
            userService.delete(selectedUser.getId());
            Clients.showNotification("User deleted!", "info", null, null, 2000);
            loadUsers();
        }
    }
    
    // New user
    @Command
    @NotifyChange({"selectedUser", "editingUser", "deleteDisabled"})
    public void newUser() {
        selectedUser = null;
        editingUser = new User();
        deleteDisabled = true;
    }
    
    // Getters (bound to View)
    public List<User> getUsers() {
        return users;
    }
    
    public User getSelectedUser() {
        return selectedUser;
    }
    
    public User getEditingUser() {
        return editingUser;
    }
    
    public boolean isDeleteDisabled() {
        return deleteDisabled;
    }
    
    // Setters (for two-way binding)
    public void setSelectedUser(User user) {
        this.selectedUser = user;
    }
}
```

### user-list.zul (View)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<zk>
    <window title="User Management (MVVM)" border="normal" 
            viewModel="@id('vm') @init('org.example.viewmodel.UserListViewModel')"
            width="600px">
        
        <vlayout>
            <!-- User List -->
            <listbox model="@load(vm.users)" selectedItem="@bind(vm.selectedUser)"
                     height="300px" onSelect="@command('selectUser', user=self.selectedItem.value)">
                <listhead>
                    <listheader label="ID" width="80px"/>
                    <listheader label="Name"/>
                    <listheader label="Email"/>
                </listhead>
                <template name="model" var="user">
                    <listitem>
                        <listcell label="@load(user.id)"/>
                        <listcell label="@load(user.name)"/>
                        <listcell label="@load(user.email)"/>
                    </listitem>
                </template>
            </listbox>
            
            <!-- Edit Form -->
            <groupbox>
                <caption label="User Details"/>
                <grid>
                    <rows>
                        <row>
                            <label value="Name:"/>
                            <textbox value="@bind(vm.editingUser.name)" width="300px" 
                                     constraint="no empty: Please enter name"/>
                        </row>
                        <row>
                            <label value="Email:"/>
                            <textbox value="@bind(vm.editingUser.email)" width="300px"
                                     constraint="/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/: Invalid email"/>
                        </row>
                    </rows>
                </grid>
            </groupbox>
            
            <!-- Action Buttons -->
            <hbox spacing="5px">
                <button label="New" onClick="@command('newUser')" sclass="btn-primary"/>
                <button label="Save" onClick="@command('save')" sclass="btn-success"/>
                <button label="Delete" onClick="@command('delete')" 
                        disabled="@load(vm.deleteDisabled)" sclass="btn-danger"/>
            </hbox>
        </vlayout>
    </window>
</zk>
```

## Common Issues

### Issue 1: @NotifyChange not updating UI
**Symptom**: Property changes in ViewModel, but UI doesn't refresh.

**Causes**:
- Forgot `@NotifyChange` annotation on command method
- Property name in `@NotifyChange` doesn't match getter
- Getter method missing or named incorrectly

**Solution**:
```java
// Wrong: No @NotifyChange
@Command
public void updateName() {
    user.setName("New Name"); // UI won't update
}

// Correct: Notify binder
@Command
@NotifyChange("user")  // Must match getUser() method
public void updateName() {
    user.setName("New Name"); // UI updates
}

// Alternative: Notify multiple properties
@Command
@NotifyChange({"user", "userCount", "isModified"})
public void updateUser() { ... }
```

### Issue 2: Binding expression not working
**Symptom**: `@bind`, `@load`, or `@save` doesn't bind property correctly.

**Causes**:
- ViewModel not initialized with `viewModel=` attribute
- Property name typo (case-sensitive)
- Getter/setter missing
- Complex expression syntax error

**Solution**:
```xml
<!-- Wrong: No viewModel attribute -->
<window>
    <textbox value="@bind(vm.username)"/> <!-- vm is undefined -->
</window>

<!-- Correct: Declare viewModel -->
<window viewModel="@id('vm') @init('com.example.MyViewModel')">
    <textbox value="@bind(vm.username)"/> <!-- Now works -->
</window>

<!-- Wrong: Property name typo -->
<textbox value="@bind(vm.userName)"/>  <!-- Getter is getUserName() -->

<!-- Correct: Match getter exactly -->
<textbox value="@bind(vm.userName)"/>  <!-- public String getUserName() -->
```

### Issue 3: @Command method not executing
**Symptom**: Button click does nothing, command method never called.

**Causes**:
- Command name typo in ZUL
- Method not annotated with `@Command`
- ViewModel not properly initialized
- Event syntax error

**Solution**:
```java
// Wrong: Missing @Command
public void save() {  // Won't be callable from ZUL
    ...
}

// Correct: Add @Command
@Command
public void save() {
    ...
}
```

```xml
<!-- Wrong: Command name typo -->
<button onClick="@command('saveUser')"/>  <!-- Method is save() -->

<!-- Correct: Match method name -->
<button onClick="@command('save')"/>  <!-- Matches @Command save() -->
```

### Issue 4: Passing parameters to commands
**Symptom**: Need to pass data to command, but it arrives as null.

**Solution**:
```xml
<!-- Pass parameter from ZUL -->
<listbox model="@load(vm.users)">
    <template name="model" var="user">
        <listitem>
            <listcell label="@load(user.name)"/>
            <listcell>
                <button label="Edit" 
                        onClick="@command('editUser', user=user)"/>
            </listcell>
        </listitem>
    </template>
</listbox>
```

```java
// Receive parameter in ViewModel
@Command
@NotifyChange("editingUser")
public void editUser(@BindingParam("user") User user) {
    this.editingUser = user;  // Now user is not null
}
```

## Warnings & Anti-Patterns

### ⚠️ Warning 1: Stateful ViewModel (Session data)
**Problem**: Storing session/user state in ViewModel fields leads to memory leaks.

```java
// BAD: Storing session-wide data
public class MyViewModel {
    private User currentUser;  // Stored across requests
    private List<Order> userOrders;  // Grows indefinitely
}
```

**Fix**: Keep ViewModels stateless, fetch data in `@Init` or `@Command`.

### ⚠️ Warning 2: Business logic in ViewModel
**Problem**: ViewModel contains complex business rules instead of delegating.

```java
// BAD
@Command
public void processOrder() {
    // 100 lines of business logic
    if (order.getTotal() > 1000) { applyDiscount(); }
    calculateTax();
    validateInventory();
    // More logic...
}
```

**Fix**: Delegate to service layer.

```java
// GOOD
@Command
@NotifyChange("orders")
public void processOrder() {
    orderService.process(order);  // Service handles logic
    loadOrders();  // ViewModel only handles UI state
}
```

### ⚠️ Warning 3: Overusing @NotifyChange("*")
**Problem**: Notifying all properties causes unnecessary UI updates.

```java
// BAD: Updates entire UI
@Command
@NotifyChange("*")
public void updateName() {
    user.setName(newName);  // Only name changed, but entire VM reloads
}
```

**Fix**: Specify exact properties.

```java
// GOOD: Surgical update
@Command
@NotifyChange("user")  // Only user property updates
public void updateName() {
    user.setName(newName);
}
```

### ⚠️ Warning 4: Missing @DependsOn for computed properties
**Problem**: Computed properties don't update when dependencies change.

```java
// BAD: fullName won't update when firstName changes
public String getFullName() {
    return firstName + " " + lastName;
}

@Command
@NotifyChange("firstName")  // fullName not notified!
public void updateFirstName(String name) {
    this.firstName = name;
}
```

**Fix**: Use `@DependsOn`.

```java
// GOOD
@DependsOn({"firstName", "lastName"})
public String getFullName() {
    return firstName + " " + lastName;
}

@Command
@NotifyChange("firstName")  // fullName auto-updates via @DependsOn
public void updateFirstName(String name) {
    this.firstName = name;
}
```

## Important Tips

### Tip 1: Use @Init for initialization
**@Init** runs once after ViewModel instantiation, perfect for loading data.

```java
@Init
public void init(@ContextParam(ContextType.VIEW) Component view) {
    loadUsers();
    initializeDefaults();
}
```

### Tip 2: Use @AfterCompose for post-render logic
**@AfterCompose** runs after all components are rendered.

```java
@AfterCompose
public void afterCompose(@ContextParam(ContextType.VIEW) Component view) {
    // Components now exist, safe to manipulate
    Clients.scrollIntoView(view);
}
```

### Tip 3: Use Form binding for validation
**Form** component provides automatic validation and dirty checking.

```xml
<window viewModel="@id('vm') @init('com.example.UserViewModel')">
    <vlayout form="@id('fx') @load(vm.user) @save(vm.user, before='save')">
        <textbox value="@bind(fx.name)" constraint="no empty"/>
        <textbox value="@bind(fx.email)" constraint="/.+@.+\.[a-z]+/"/>
        <button label="Save" onClick="@command('save')"/>
    </vlayout>
</window>
```

### Tip 4: Use @GlobalCommand for cross-ViewModel communication
Trigger commands in other ViewModels without direct references.

```java
// Sender ViewModel
@Command
public void createUser() {
    userService.save(user);
    BindUtils.postGlobalCommand(null, null, "refreshUserList", null);
}

// Receiver ViewModel
@GlobalCommand
@NotifyChange("users")
public void refreshUserList() {
    users = userService.findAll();
}
```

### Tip 5: Use converter for display formatting
Convert model values for display without changing the model.

```xml
<label value="@load(vm.user.birthDate) @converter('formatedDate', format='yyyy-MM-dd')"/>
<label value="@load(vm.price) @converter('formatedNumber', format='###,##0.00')"/>
```

### Tip 6: Optimize with @SmartNotifyChange
**@SmartNotifyChange** only notifies if value actually changed.

```java
@Command
@SmartNotifyChange("user")  // Checks if user reference changed
public void updateUser(User newUser) {
    this.user = newUser;  // Only notifies if newUser != user
}
```

## Community Edition Limitations

**MVVM pattern is fully available in Community Edition** with no major restrictions:

### ✅ Available in CE (FREE):
- `@Init`, `@Command`, `@NotifyChange`, `@GlobalCommand`
- `@bind`, `@load`, `@save` binding expressions
- Form binding and validation
- `@BindingParam`, `@ContextParam`
- `@DependsOn`, `@SmartNotifyChange`
- All standard converters and validators
- All ZUL components (Grid, Listbox, Tree, etc.)

### ⚠️ Enterprise Edition Only:
- **ZK Charts** (`<charts>` component) - requires ZK PE/EE
- **Spreadsheet** component - requires ZK EE
- **Pivottable** component - requires ZK EE
- **Advanced themes** (Iceblue, Silvertail) - some themes are PE/EE only

**For 95% of MVVM development, Community Edition is sufficient.**

## Official ZK MVVM Resources

- **MVVM Reference**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM
- **Data Binding**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM/Data_Binding
- **ViewModel**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM/ViewModel
- **Advanced MVVM**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM/Advanced

