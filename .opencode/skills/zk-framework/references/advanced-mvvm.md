# ZK Framework Advanced MVVM

Advanced MVVM techniques and patterns for complex ZK applications.

## Table of Contents

1. [Global Commands](#global-commands)
2. [Form Binding](#form-binding)
3. [Nested Beans](#nested-beans)
4. [Conditional Binding](#conditional-binding)
5. [Collection Binding](#collection-binding)
6. [Validation](#validation)

## Global Commands

### Broadcasting Global Commands

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import org.zkoss.bind.BindUtils;
import com.example.service.NotificationService;

public class NotificationVM {
    
    @WireVariable
    private NotificationService notificationService;
    
    private List<Notification> notifications;
    private int unreadCount;
    
    @Init
    public void init() {
        loadNotifications();
    }
    
    @Command
    @NotifyChange({"notifications", "unreadCount"})
    public void loadNotifications() {
        notifications = notificationService.getRecentNotifications();
        unreadCount = notificationService.getUnreadCount();
    }
    
    @Command
    @NotifyChange({"notifications", "unreadCount"})
    public void markAsRead(@BindingParam("notification") Notification notification) {
        notificationService.markAsRead(notification);
        loadNotifications();
        
        BindUtils.postGlobalCommand(null, null, "refreshNotifications", null);
    }
    
    @GlobalCommand
    @NotifyChange({"notifications", "unreadCount"})
    public void refreshNotifications() {
        loadNotifications();
    }
    
    public List<Notification> getNotifications() {
        return notifications;
    }
    
    public int getUnreadCount() {
        return unreadCount;
    }
}
```

### Listening to Global Commands

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;

public class HeaderVM {
    
    private int notificationBadge = 0;
    
    @Init
    public void init() {
        updateBadge();
    }
    
    @GlobalCommand("refreshNotifications")
    @NotifyChange("notificationBadge")
    public void onNotificationRefresh() {
        updateBadge();
    }
    
    private void updateBadge() {
        notificationBadge = notificationService.getUnreadCount();
    }
    
    public int getNotificationBadge() {
        return notificationBadge;
    }
}
```

### Passing Parameters with Global Commands

```java
@Command
public void deleteUser(@BindingParam("userId") Long userId) {
    userService.delete(userId);
    
    Map<String, Object> args = new HashMap<>();
    args.put("userId", userId);
    args.put("action", "delete");
    
    BindUtils.postGlobalCommand(null, null, "userChanged", args);
}

@GlobalCommand("userChanged")
@NotifyChange("users")
public void onUserChanged(@BindingParam("userId") Long userId,
                          @BindingParam("action") String action) {
    if ("delete".equals(action)) {
        loadUsers();
    }
}
```

## Form Binding

### Form Binding with Validation

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.bind.ValidationContext;
import org.zkoss.bind.validator.AbstractValidator;

public class UserFormVM {
    
    private User user;
    private User originalUser;
    
    @Init
    public void init(@ExecutionArgParam("userId") Long userId) {
        if (userId != null) {
            user = userService.findById(userId);
            originalUser = cloneUser(user);
        } else {
            user = new User();
            originalUser = new User();
        }
    }
    
    @Command
    public void save(@BindingParam("fx") ValidationContext vctx) {
        if (!vctx.isValid()) {
            return;
        }
        
        try {
            userService.save(user);
            Clients.showNotification("User saved successfully", 
                                   "info", null, "middle_center", 3000);
            originalUser = cloneUser(user);
        } catch (Exception e) {
            Clients.showNotification("Error: " + e.getMessage(), 
                                   "error", null, "middle_center", 3000);
        }
    }
    
    @Command
    @NotifyChange("user")
    public void reset() {
        user = cloneUser(originalUser);
    }
    
    @Command
    public void cancel() {
        Executions.sendRedirect("userList.zul");
    }
    
    public Validator getEmailValidator() {
        return new AbstractValidator() {
            @Override
            public void validate(ValidationContext ctx) {
                String email = (String) ctx.getProperty().getValue();
                
                if (email == null || email.trim().isEmpty()) {
                    addInvalidMessage(ctx, "Email is required");
                    return;
                }
                
                if (!email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$")) {
                    addInvalidMessage(ctx, "Invalid email format");
                    return;
                }
                
                if (emailExists(email) && !email.equals(originalUser.getEmail())) {
                    addInvalidMessage(ctx, "Email already exists");
                }
            }
        };
    }
    
    public Validator getPasswordValidator() {
        return new AbstractValidator() {
            @Override
            public void validate(ValidationContext ctx) {
                String password = (String) ctx.getProperty().getValue();
                
                if (originalUser.getId() == null && 
                    (password == null || password.length() < 8)) {
                    addInvalidMessage(ctx, "Password must be at least 8 characters");
                }
            }
        };
    }
    
    public User getUser() {
        return user;
    }
    
    private User cloneUser(User source) {
        User clone = new User();
        clone.setId(source.getId());
        clone.setName(source.getName());
        clone.setEmail(source.getEmail());
        return clone;
    }
}
```

### ZUML Form with Validation

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.UserFormVM')"
        validationMessages="@id('vmsgs')">
    
    <grid>
        <columns>
            <column width="120px" />
            <column />
        </columns>
        <rows>
            <row>
                <label value="Name:" />
                <textbox value="@bind(vm.user.name) 
                               @validator(vm.nameValidator)" 
                         width="200px" />
                <label value="@load(vmsgs['user.name'])" 
                       sclass="error" />
            </row>
            
            <row>
                <label value="Email:" />
                <textbox value="@bind(vm.user.email) 
                               @validator(vm.emailValidator)" 
                         width="200px" />
                <label value="@load(vmsgs['user.email'])" 
                       sclass="error" />
            </row>
            
            <row>
                <label value="Password:" />
                <textbox type="password" 
                         value="@bind(vm.user.password) 
                               @validator(vm.passwordValidator)" 
                         width="200px" />
                <label value="@load(vmsgs['user.password'])" 
                       sclass="error" />
            </row>
            
            <row>
                <cell colspan="2">
                    <button label="Save" onClick="@command('save', fx=vmsgs)" />
                    <button label="Reset" onClick="@command('reset')" />
                    <button label="Cancel" onClick="@command('cancel')" />
                </cell>
            </row>
        </rows>
    </grid>
</window>
```

## Nested Beans

### Working with Nested Objects

```java
package com.example.model;

public class Order {
    private Long id;
    private Customer customer;
    private Address shippingAddress;
    private List<OrderItem> items;
    private Payment payment;
    
    // Getters and setters
}

public class Customer {
    private Long id;
    private String name;
    private String email;
}

public class Address {
    private String street;
    private String city;
    private String state;
    private String zipCode;
}

public class OrderItem {
    private Product product;
    private int quantity;
    private BigDecimal price;
}
```

### ViewModel with Nested Beans

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;

public class OrderFormVM {
    
    private Order order;
    
    @Init
    public void init(@ExecutionArgParam("orderId") Long orderId) {
        if (orderId != null) {
            order = orderService.findById(orderId);
        } else {
            order = new Order();
            order.setCustomer(new Customer());
            order.setShippingAddress(new Address());
            order.setItems(new ArrayList<>());
            order.setPayment(new Payment());
        }
    }
    
    @Command
    @NotifyChange("order")
    public void addItem() {
        OrderItem item = new OrderItem();
        item.setQuantity(1);
        order.getItems().add(item);
    }
    
    @Command
    @NotifyChange("order")
    public void removeItem(@BindingParam("item") OrderItem item) {
        order.getItems().remove(item);
    }
    
    @Command
    @NotifyChange("order.customer")
    public void loadCustomer(@BindingParam("customerId") Long customerId) {
        Customer customer = customerService.findById(customerId);
        order.setCustomer(customer);
        
        if (customer.getDefaultAddress() != null) {
            order.setShippingAddress(customer.getDefaultAddress());
        }
    }
    
    @Command
    public void save() {
        if (validateOrder()) {
            orderService.save(order);
            Clients.showNotification("Order saved successfully");
        }
    }
    
    @DependsOn({"order.items"})
    public BigDecimal getTotalAmount() {
        return order.getItems().stream()
            .map(item -> item.getPrice().multiply(
                BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    public Order getOrder() {
        return order;
    }
}
```

### Binding Nested Properties

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.OrderFormVM')">
    <groupbox>
        <caption label="Customer Information" />
        <grid>
            <rows>
                <row>
                    <label value="Name:" />
                    <textbox value="@bind(vm.order.customer.name)" />
                </row>
                <row>
                    <label value="Email:" />
                    <textbox value="@bind(vm.order.customer.email)" />
                </row>
            </rows>
        </grid>
    </groupbox>
    
    <groupbox>
        <caption label="Shipping Address" />
        <grid>
            <rows>
                <row>
                    <label value="Street:" />
                    <textbox value="@bind(vm.order.shippingAddress.street)" />
                </row>
                <row>
                    <label value="City:" />
                    <textbox value="@bind(vm.order.shippingAddress.city)" />
                </row>
                <row>
                    <label value="State:" />
                    <textbox value="@bind(vm.order.shippingAddress.state)" />
                </row>
            </rows>
        </grid>
    </groupbox>
    
    <groupbox>
        <caption label="Order Items" />
        <listbox model="@bind(vm.order.items)">
            <listhead>
                <listheader label="Product" />
                <listheader label="Quantity" />
                <listheader label="Price" />
                <listheader label="Actions" />
            </listhead>
            <template name="model">
                <listitem>
                    <listcell>
                        <textbox value="@bind(each.product.name)" />
                    </listcell>
                    <listcell>
                        <intbox value="@bind(each.quantity)" />
                    </listcell>
                    <listcell>
                        <doublebox value="@bind(each.price)" 
                                   format="$###,##0.00" />
                    </listcell>
                    <listcell>
                        <button label="Remove" 
                                onClick="@command('removeItem', item=each)" />
                    </listcell>
                </listitem>
            </template>
        </listbox>
        <button label="Add Item" onClick="@command('addItem')" />
    </groupbox>
    
    <div>
        <label value="Total: " />
        <label value="@load(vm.totalAmount) @converter('formattedNumber', format='$###,##0.00')" 
               style="font-weight: bold; font-size: 18px;" />
    </div>
    
    <button label="Save Order" onClick="@command('save')" />
</window>
```

## Conditional Binding

### Conditional Visibility

```java
public class ProductVM {
    
    private Product product;
    private String userRole;
    
    @Init
    public void init() {
        product = new Product();
        userRole = SecurityUtil.getCurrentUserRole();
    }
    
    public boolean isAdmin() {
        return "ADMIN".equals(userRole);
    }
    
    public boolean isProductDiscounted() {
        return product.getDiscountPercent() != null && 
               product.getDiscountPercent() > 0;
    }
    
    @DependsOn({"product.price", "product.discountPercent"})
    public BigDecimal getFinalPrice() {
        if (isProductDiscounted()) {
            BigDecimal discount = product.getPrice()
                .multiply(BigDecimal.valueOf(product.getDiscountPercent()))
                .divide(BigDecimal.valueOf(100));
            return product.getPrice().subtract(discount);
        }
        return product.getPrice();
    }
    
    public Product getProduct() {
        return product;
    }
}
```

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.ProductVM')">
    <textbox value="@bind(vm.product.name)" />
    
    <doublebox value="@bind(vm.product.price)" />
    
    <intbox value="@bind(vm.product.discountPercent)" 
            visible="@load(vm.admin)" />
    
    <label value="@load(vm.finalPrice) @converter('formattedNumber', format='$###,##0.00')"
           style="@load(vm.productDiscounted ? 'color: red; font-weight: bold;' : '')" />
    
    <label value="SALE!" 
           visible="@load(vm.productDiscounted)"
           style="background: red; color: white; padding: 5px;" />
    
    <button label="Delete Product" 
            onClick="@command('delete')"
            visible="@load(vm.admin)" />
</window>
```

## Collection Binding

### Dynamic List Management

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zul.ListModelList;

public class TagManagerVM {
    
    private ListModelList<String> tags;
    private String newTag = "";
    
    @Init
    public void init() {
        tags = new ListModelList<>();
        tags.addAll(Arrays.asList("Java", "ZK", "Spring"));
        tags.setMultiple(true);
    }
    
    @Command
    @NotifyChange({"tags", "newTag"})
    public void addTag() {
        if (newTag != null && !newTag.trim().isEmpty() && !tags.contains(newTag)) {
            tags.add(newTag);
            newTag = "";
        }
    }
    
    @Command
    @NotifyChange("tags")
    public void removeTag(@BindingParam("tag") String tag) {
        tags.remove(tag);
    }
    
    @Command
    @NotifyChange("tags")
    public void removeSelected() {
        Set<String> selection = tags.getSelection();
        tags.removeAll(selection);
    }
    
    @Command
    @NotifyChange("tags")
    public void clearAll() {
        tags.clear();
    }
    
    public ListModelList<String> getTags() {
        return tags;
    }
    
    public String getNewTag() {
        return newTag;
    }
    
    public void setNewTag(String newTag) {
        this.newTag = newTag;
    }
}
```

### Set and Map Binding

```java
public class PreferencesVM {
    
    private Map<String, String> preferences;
    private Set<String> enabledFeatures;
    
    @Init
    public void init() {
        preferences = new HashMap<>();
        preferences.put("theme", "dark");
        preferences.put("language", "en");
        
        enabledFeatures = new HashSet<>();
        enabledFeatures.add("notifications");
        enabledFeatures.add("autoSave");
    }
    
    @Command
    @NotifyChange("preferences")
    public void updatePreference(@BindingParam("key") String key,
                                 @BindingParam("value") String value) {
        preferences.put(key, value);
    }
    
    @Command
    @NotifyChange("enabledFeatures")
    public void toggleFeature(@BindingParam("feature") String feature) {
        if (enabledFeatures.contains(feature)) {
            enabledFeatures.remove(feature);
        } else {
            enabledFeatures.add(feature);
        }
    }
    
    public boolean isFeatureEnabled(String feature) {
        return enabledFeatures.contains(feature);
    }
    
    public Map<String, String> getPreferences() {
        return preferences;
    }
    
    public Set<String> getEnabledFeatures() {
        return enabledFeatures;
    }
}
```

## Validation

### Custom Validators

```java
package com.example.validator;

import org.zkoss.bind.ValidationContext;
import org.zkoss.bind.validator.AbstractValidator;

public class CreditCardValidator extends AbstractValidator {
    
    @Override
    public void validate(ValidationContext ctx) {
        String cardNumber = (String) ctx.getProperty().getValue();
        
        if (cardNumber == null || cardNumber.trim().isEmpty()) {
            addInvalidMessage(ctx, "Credit card number is required");
            return;
        }
        
        cardNumber = cardNumber.replaceAll("\\s+", "");
        
        if (!cardNumber.matches("\\d{13,19}")) {
            addInvalidMessage(ctx, "Invalid credit card number format");
            return;
        }
        
        if (!luhnCheck(cardNumber)) {
            addInvalidMessage(ctx, "Invalid credit card number");
        }
    }
    
    private boolean luhnCheck(String cardNumber) {
        int sum = 0;
        boolean alternate = false;
        
        for (int i = cardNumber.length() - 1; i >= 0; i--) {
            int digit = Character.getNumericValue(cardNumber.charAt(i));
            
            if (alternate) {
                digit *= 2;
                if (digit > 9) {
                    digit = (digit % 10) + 1;
                }
            }
            
            sum += digit;
            alternate = !alternate;
        }
        
        return (sum % 10 == 0);
    }
}
```

### Cross-Field Validation

```java
public class RegistrationFormValidator extends AbstractValidator {
    
    @Override
    public void validate(ValidationContext ctx) {
        Map<String, Property> properties = ctx.getProperties(Property.class);
        
        String password = (String) properties.get("password").getValue();
        String confirmPassword = (String) properties.get("confirmPassword").getValue();
        
        if (password != null && !password.equals(confirmPassword)) {
            addInvalidMessage(ctx, "confirmPassword", "Passwords do not match");
        }
        
        Date birthDate = (Date) properties.get("birthDate").getValue();
        if (birthDate != null) {
            LocalDate birth = birthDate.toInstant()
                .atZone(ZoneId.systemDefault()).toLocalDate();
            LocalDate now = LocalDate.now();
            int age = Period.between(birth, now).getYears();
            
            if (age < 18) {
                addInvalidMessage(ctx, "birthDate", "Must be at least 18 years old");
            }
        }
    }
}
```
