# MVC Pattern Guide for ZK Framework

This reference provides comprehensive guidance on using the MVC (Model-View-Controller) pattern in ZK Framework.

## Complete MVC Example

### UserListComposer.java (Controller)
```java
package org.example.composer;

import org.zkoss.zk.ui.Component;
import org.zkoss.zk.ui.select.SelectorComposer;
import org.zkoss.zk.ui.select.annotation.Listen;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zul.*;
import org.example.model.User;
import org.example.service.UserService;
import java.util.List;

public class UserListComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox userListbox;
    
    @Wire
    private Textbox nameTextbox;
    
    @Wire
    private Textbox emailTextbox;
    
    @Wire
    private Button saveBtn;
    
    @Wire
    private Button deleteBtn;
    
    private UserService userService = new UserService();
    private User selectedUser;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        loadUsers();
    }
    
    private void loadUsers() {
        List<User> users = userService.findAll();
        ListModelList<User> model = new ListModelList<>(users);
        model.setMultiple(false);
        userListbox.setModel(model);
    }
    
    @Listen("onSelect = #userListbox")
    public void onSelectUser() {
        selectedUser = userListbox.getSelectedItem().getValue();
        nameTextbox.setValue(selectedUser.getName());
        emailTextbox.setValue(selectedUser.getEmail());
        deleteBtn.setDisabled(false);
    }
    
    @Listen("onClick = #saveBtn")
    public void onSave() {
        if (selectedUser == null) {
            // Create new user
            User user = new User();
            user.setName(nameTextbox.getValue());
            user.setEmail(emailTextbox.getValue());
            userService.save(user);
            Clients.showNotification("User created successfully!");
        } else {
            // Update existing user
            selectedUser.setName(nameTextbox.getValue());
            selectedUser.setEmail(emailTextbox.getValue());
            userService.update(selectedUser);
            Clients.showNotification("User updated successfully!");
        }
        loadUsers();
        clearForm();
    }
    
    @Listen("onClick = #deleteBtn")
    public void onDelete() {
        if (selectedUser != null) {
            userService.delete(selectedUser.getId());
            Clients.showNotification("User deleted!");
            loadUsers();
            clearForm();
        }
    }
    
    @Listen("onClick = #newBtn")
    public void onNew() {
        clearForm();
    }
    
    private void clearForm() {
        selectedUser = null;
        nameTextbox.setValue("");
        emailTextbox.setValue("");
        deleteBtn.setDisabled(true);
    }
}
```

### user-list.zul (View)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<zk>
    <window title="User Management (MVC)" border="normal" 
            apply="org.example.composer.UserListComposer"
            width="600px">
        
        <vlayout>
            <!-- User List -->
            <listbox id="userListbox" height="300px">
                <listhead>
                    <listheader label="ID" width="80px"/>
                    <listheader label="Name"/>
                    <listheader label="Email"/>
                </listhead>
                <template name="model">
                    <listitem>
                        <listcell label="${each.id}"/>
                        <listcell label="${each.name}"/>
                        <listcell label="${each.email}"/>
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
                            <textbox id="nameTextbox" width="300px" 
                                     constraint="no empty: Please enter name"/>
                        </row>
                        <row>
                            <label value="Email:"/>
                            <textbox id="emailTextbox" width="300px"
                                     constraint="/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/: Invalid email"/>
                        </row>
                    </rows>
                </grid>
            </groupbox>
            
            <!-- Action Buttons -->
            <hbox spacing="5px">
                <button id="newBtn" label="New" sclass="btn-primary"/>
                <button id="saveBtn" label="Save" sclass="btn-success"/>
                <button id="deleteBtn" label="Delete" sclass="btn-danger" disabled="true"/>
            </hbox>
        </vlayout>
    </window>
</zk>
```

## Common Issues

### Issue 1: "Component not found" error
**Symptom**: `@Wire` annotation doesn't inject component, NullPointerException when accessing.

**Causes**:
- Component ID in ZUL doesn't match `@Wire` field name
- Accessing component before `doAfterCompose()` completes
- Component is inside a template or macro (not in main tree)

**Solution**:
```java
// Wrong: Accessing in constructor
public UserComposer() {
    userListbox.setModel(...); // NPE! Component not wired yet
}

// Correct: Access in doAfterCompose or event handlers
@Override
public void doAfterCompose(Component comp) throws Exception {
    super.doAfterCompose(comp); // Wire components first
    userListbox.setModel(...);  // Now safe
}
```

### Issue 2: Event listener not firing
**Symptom**: `@Listen` method never executes when component is clicked.

**Causes**:
- Wrong event name (e.g., `onClick` vs `onSelect`)
- Component selector doesn't match ID
- Composer not applied to correct window

**Solution**:
```java
// Wrong
@Listen("onClick = #myBtn")  // ID mismatch
public void onSave() { ... }

// Correct
@Listen("onClick = #saveBtn")  // Matches <button id="saveBtn">
public void onSave() { ... }

// Alternative: Use CSS selector
@Listen("onClick = button[label='Save']")
public void onSave() { ... }
```

### Issue 3: Memory leak from event listeners
**Symptom**: Memory usage grows over time, sessions don't release.

**Cause**: Adding event listeners dynamically without cleanup.

**Solution**:
```java
// Store listener references for cleanup
private EventListener<Event> myListener;

@Override
public void doAfterCompose(Component comp) throws Exception {
    super.doAfterCompose(comp);
    
    myListener = evt -> { /* logic */ };
    myButton.addEventListener(Events.ON_CLICK, myListener);
}

// Clean up in detach
@Override
public void doBeforeComposeChildren(Component comp) throws Exception {
    super.doBeforeComposeChildren(comp);
    if (myListener != null) {
        myButton.removeEventListener(Events.ON_CLICK, myListener);
    }
}
```

## Warnings & Anti-Patterns

### ⚠️ Warning 1: God Composer
**Problem**: Single composer handles too many responsibilities.

```java
// BAD: 2000-line composer handling users, orders, reports
public class MegaComposer extends SelectorComposer<Component> {
    @Wire Listbox users, orders, products, invoices;
    // 50+ @Wire annotations
    // 30+ @Listen methods
}
```

**Fix**: Split into multiple composers, one per logical module.

### ⚠️ Warning 2: Business logic in composer
**Problem**: Composer contains complex business rules instead of delegating to services.

```java
// BAD
@Listen("onClick = #saveBtn")
public void onSave() {
    if (user.getAge() < 18) { /* validation */ }
    if (user.getEmail().contains("@")) { /* validation */ }
    // 50 lines of business logic
    saveToDatabase(user);
}
```

**Fix**: Move logic to service layer, composer only handles UI.

### ⚠️ Warning 3: Tight coupling via IDs
**Problem**: Composer hardcodes component IDs, making refactoring difficult.

```java
// Brittle
Button btn = (Button) Path.getComponent("//window/hbox/button[@label='Save']");
```

**Fix**: Use `@Wire` or inject dependencies.

## Important Tips

### Tip 1: Use SelectorComposer, not GenericForwardComposer
**GenericForwardComposer** is deprecated since ZK 9.x. Use **SelectorComposer**.

```java
// Old (deprecated)
public class MyComposer extends GenericForwardComposer { ... }

// Modern
public class MyComposer extends SelectorComposer<Component> { ... }
```

### Tip 2: Leverage auto-wiring naming convention
If field name matches component ID, `@Wire` can be omitted (but explicit is better).

```java
// Auto-wired if field name = component ID
private Textbox username;  // Matches <textbox id="username"/>
```

### Tip 3: Use @Listen for concise event handling
`@Listen` is cleaner than manual `addEventListener`.

```java
// Instead of this:
public void doAfterCompose(Component comp) {
    super.doAfterCompose(comp);
    saveBtn.addEventListener(Events.ON_CLICK, evt -> onSave());
}

// Use this:
@Listen("onClick = #saveBtn")
public void onSave() { ... }
```

### Tip 4: Forward events for better separation
Forward events from sub-components to parent composer for centralized handling.

```java
// In child component
Events.postEvent("onUserSelected", parentWindow, selectedUser);

// In parent composer
@Listen("onUserSelected = #userPanel")
public void handleUserSelected(ForwardEvent evt) {
    User user = (User) evt.getData();
    // Handle event
}
```

### Tip 5: Use Executions.getCurrent() for context
Access request parameters, session, and other context from anywhere.

```java
String param = Executions.getCurrent().getParameter("userId");
Session session = Sessions.getCurrent();
Desktop desktop = Executions.getCurrent().getDesktop();
```

## Community Edition Limitations

The **MVC pattern is fully available in Community Edition** with no restrictions. All composer-related features are free:

- ✅ `SelectorComposer`, `GenericForwardComposer`
- ✅ `@Wire`, `@Listen` annotations
- ✅ Event handling, component manipulation
- ✅ All ZUL components (Grid, Listbox, Tree, etc.)

**No Enterprise Edition required for MVC development.**
