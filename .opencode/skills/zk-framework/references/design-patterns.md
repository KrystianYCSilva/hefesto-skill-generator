# ZK Framework Design Patterns

Essential design patterns for building maintainable ZK applications.

## Table of Contents

1. [Composer Pattern](#composer-pattern)
2. [ViewModel Pattern](#viewmodel-pattern)
3. [Template Method Pattern](#template-method-pattern)
4. [Macro Component Pattern](#macro-component-pattern)
5. [Repository Pattern](#repository-pattern)
6. [Service Layer Pattern](#service-layer-pattern)

## Composer Pattern

### Basic Composer

```java
package com.example.composer;

import org.zkoss.zk.ui.Component;
import org.zkoss.zk.ui.select.SelectorComposer;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zk.ui.select.annotation.Listen;
import org.zkoss.zul.*;

public class UserListComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox userListbox;
    
    @Wire
    private Textbox nameTextbox;
    
    @Wire
    private Textbox emailTextbox;
    
    private ListModelList<User> userModel;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        loadUsers();
    }
    
    private void loadUsers() {
        List<User> users = getUsersFromDatabase();
        userModel = new ListModelList<>(users);
        userListbox.setModel(userModel);
    }
    
    @Listen("onClick = #addButton")
    public void onAddUser() {
        User user = new User();
        user.setName(nameTextbox.getValue());
        user.setEmail(emailTextbox.getValue());
        
        userModel.add(user);
        clearForm();
    }
    
    @Listen("onClick = #deleteButton")
    public void onDeleteUser() {
        Set<User> selection = userModel.getSelection();
        
        if (!selection.isEmpty()) {
            userModel.removeAll(selection);
        }
    }
    
    private void clearForm() {
        nameTextbox.setValue("");
        emailTextbox.setValue("");
    }
    
    private List<User> getUsersFromDatabase() {
        return new ArrayList<>();
    }
}
```

### Generic Composer

```java
package com.example.composer;

import org.zkoss.zk.ui.Component;
import org.zkoss.zk.ui.select.SelectorComposer;
import org.zkoss.zul.ListModelList;

public abstract class GenericListComposer<T> extends SelectorComposer<Component> {
    
    protected ListModelList<T> model;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        initModel();
        loadData();
    }
    
    protected void initModel() {
        model = new ListModelList<>();
    }
    
    protected void loadData() {
        List<T> items = fetchItems();
        model.clear();
        model.addAll(items);
    }
    
    protected abstract List<T> fetchItems();
    
    protected void addItem(T item) {
        model.add(item);
    }
    
    protected void updateItem(T item) {
        int index = model.indexOf(item);
        if (index >= 0) {
            model.set(index, item);
        }
    }
    
    protected void deleteItem(T item) {
        model.remove(item);
    }
    
    protected void deleteSelected() {
        Set<T> selection = model.getSelection();
        model.removeAll(selection);
    }
}
```

```java
package com.example.composer;

public class ProductListComposer extends GenericListComposer<Product> {
    
    @Wire
    private Listbox productListbox;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        productListbox.setModel(model);
    }
    
    @Override
    protected List<Product> fetchItems() {
        return productService.findAll();
    }
    
    @Listen("onClick = #addButton")
    public void onAdd() {
        Product product = createProductFromForm();
        addItem(product);
    }
}
```

## ViewModel Pattern

### MVVM ViewModel

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import com.example.service.ProductService;
import com.example.model.Product;
import java.util.List;

public class ProductVM {
    
    @WireVariable
    private ProductService productService;
    
    private List<Product> products;
    private Product selectedProduct;
    private String searchKeyword = "";
    
    @Init
    public void init() {
        loadProducts();
    }
    
    @Command
    @NotifyChange("products")
    public void loadProducts() {
        if (searchKeyword.isEmpty()) {
            products = productService.findAll();
        } else {
            products = productService.search(searchKeyword);
        }
    }
    
    @Command
    @NotifyChange({"products", "selectedProduct"})
    public void saveProduct() {
        if (selectedProduct != null) {
            productService.save(selectedProduct);
            selectedProduct = null;
            loadProducts();
        }
    }
    
    @Command
    @NotifyChange({"products", "selectedProduct"})
    public void deleteProduct(@BindingParam("product") Product product) {
        productService.delete(product);
        selectedProduct = null;
        loadProducts();
    }
    
    @Command
    @NotifyChange("selectedProduct")
    public void newProduct() {
        selectedProduct = new Product();
    }
    
    @Command
    @NotifyChange("products")
    public void search() {
        loadProducts();
    }
    
    public List<Product> getProducts() {
        return products;
    }
    
    public Product getSelectedProduct() {
        return selectedProduct;
    }
    
    public void setSelectedProduct(Product selectedProduct) {
        this.selectedProduct = selectedProduct;
    }
    
    public String getSearchKeyword() {
        return searchKeyword;
    }
    
    public void setSearchKeyword(String searchKeyword) {
        this.searchKeyword = searchKeyword;
    }
}
```

### Form Validation ViewModel

```java
package com.example.viewmodel;

import org.zkoss.bind.ValidationContext;
import org.zkoss.bind.Validator;
import org.zkoss.bind.annotation.Command;
import org.zkoss.bind.annotation.Init;
import org.zkoss.bind.annotation.NotifyChange;
import org.zkoss.bind.validator.AbstractValidator;

public class UserFormVM {
    
    private User user;
    
    @Init
    public void init() {
        user = new User();
    }
    
    @Command
    @NotifyChange("user")
    public void save(@BindingParam("fx") ValidationContext vctx) {
        if (vctx.isValid()) {
            userService.save(user);
            Clients.showNotification("User saved successfully");
        }
    }
    
    public Validator getEmailValidator() {
        return new AbstractValidator() {
            @Override
            public void validate(ValidationContext ctx) {
                String email = (String) ctx.getProperty().getValue();
                
                if (email == null || email.isEmpty()) {
                    addInvalidMessage(ctx, "Email is required");
                } else if (!email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
                    addInvalidMessage(ctx, "Invalid email format");
                }
            }
        };
    }
    
    public Validator getPasswordValidator() {
        return new AbstractValidator() {
            @Override
            public void validate(ValidationContext ctx) {
                String password = (String) ctx.getProperty().getValue();
                
                if (password == null || password.length() < 8) {
                    addInvalidMessage(ctx, "Password must be at least 8 characters");
                }
            }
        };
    }
    
    public User getUser() {
        return user;
    }
}
```

## Template Method Pattern

### Abstract CRUD ViewModel

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import java.util.List;

public abstract class AbstractCrudVM<T> {
    
    protected List<T> items;
    protected T selectedItem;
    
    @Init
    public void init() {
        loadItems();
        initializeNewItem();
    }
    
    @Command
    @NotifyChange("items")
    public void load() {
        loadItems();
    }
    
    @Command
    @NotifyChange({"items", "selectedItem"})
    public void save() {
        if (validate(selectedItem)) {
            beforeSave(selectedItem);
            
            if (isNewItem(selectedItem)) {
                create(selectedItem);
            } else {
                update(selectedItem);
            }
            
            afterSave(selectedItem);
            loadItems();
            initializeNewItem();
        }
    }
    
    @Command
    @NotifyChange({"items", "selectedItem"})
    public void delete(@BindingParam("item") T item) {
        if (confirmDelete(item)) {
            beforeDelete(item);
            performDelete(item);
            afterDelete(item);
            loadItems();
            initializeNewItem();
        }
    }
    
    @Command
    @NotifyChange("selectedItem")
    public void newItem() {
        initializeNewItem();
    }
    
    protected void loadItems() {
        items = fetchItems();
    }
    
    protected void initializeNewItem() {
        selectedItem = createNewItem();
    }
    
    protected abstract List<T> fetchItems();
    protected abstract T createNewItem();
    protected abstract boolean isNewItem(T item);
    protected abstract void create(T item);
    protected abstract void update(T item);
    protected abstract void performDelete(T item);
    
    protected boolean validate(T item) {
        return true;
    }
    
    protected void beforeSave(T item) {}
    protected void afterSave(T item) {}
    protected void beforeDelete(T item) {}
    protected void afterDelete(T item) {}
    
    protected boolean confirmDelete(T item) {
        return true;
    }
    
    public List<T> getItems() {
        return items;
    }
    
    public T getSelectedItem() {
        return selectedItem;
    }
    
    public void setSelectedItem(T item) {
        this.selectedItem = item;
    }
}
```

### Concrete Implementation

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.WireVariable;
import org.zkoss.zul.Messagebox;
import com.example.service.ProductService;
import com.example.model.Product;

public class ProductCrudVM extends AbstractCrudVM<Product> {
    
    @WireVariable
    private ProductService productService;
    
    @Override
    protected List<Product> fetchItems() {
        return productService.findAll();
    }
    
    @Override
    protected Product createNewItem() {
        return new Product();
    }
    
    @Override
    protected boolean isNewItem(Product item) {
        return item.getId() == null;
    }
    
    @Override
    protected void create(Product item) {
        productService.save(item);
    }
    
    @Override
    protected void update(Product item) {
        productService.update(item);
    }
    
    @Override
    protected void performDelete(Product item) {
        productService.delete(item);
    }
    
    @Override
    protected boolean validate(Product item) {
        if (item.getName() == null || item.getName().isEmpty()) {
            Messagebox.show("Product name is required", "Validation Error",
                          Messagebox.OK, Messagebox.ERROR);
            return false;
        }
        
        if (item.getPrice() == null || item.getPrice().compareTo(BigDecimal.ZERO) <= 0) {
            Messagebox.show("Product price must be greater than zero", 
                          "Validation Error", Messagebox.OK, Messagebox.ERROR);
            return false;
        }
        
        return true;
    }
    
    @Override
    protected void afterSave(Product item) {
        Messagebox.show("Product saved successfully", "Success",
                      Messagebox.OK, Messagebox.INFORMATION);
    }
}
```

## Macro Component Pattern

### Reusable Macro Component

```xml
<!-- userCard.zul -->
<vlayout xmlns:w="client">
    <div style="border: 1px solid #ccc; padding: 10px; margin: 5px;">
        <hbox>
            <image src="${arg.avatarUrl}" width="50px" height="50px" />
            <vbox>
                <label value="${arg.name}" style="font-weight: bold;" />
                <label value="${arg.email}" />
                <label value="Member since: ${arg.memberSince}" />
            </vbox>
        </hbox>
        <hbox>
            <button label="Edit" onClick='@command("editUser", user=arg)' />
            <button label="Delete" onClick='@command("deleteUser", user=arg)' />
        </hbox>
    </div>
</vlayout>
```

### Using Macro Components

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.UserListVM')">
    <vlayout>
        <forEach items="@load(vm.users)">
            <apply templateURI="/components/userCard.zul">
                <custom-attributes 
                    arg="${each}"
                    avatarUrl="${each.avatarUrl}"
                    name="${each.name}"
                    email="${each.email}"
                    memberSince="${each.createdDate}" />
            </apply>
        </forEach>
    </vlayout>
</window>
```

### Custom Component

```java
package com.example.component;

import org.zkoss.zk.ui.HtmlMacroComponent;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zul.Label;
import org.zkoss.zul.Image;

public class UserCard extends HtmlMacroComponent {
    
    @Wire
    private Label nameLabel;
    
    @Wire
    private Label emailLabel;
    
    @Wire
    private Image avatarImage;
    
    private User user;
    
    public UserCard() {
        setMacroURI("/components/userCard.zul");
    }
    
    @Override
    public void afterCompose() {
        super.afterCompose();
        updateUI();
    }
    
    private void updateUI() {
        if (user != null) {
            nameLabel.setValue(user.getName());
            emailLabel.setValue(user.getEmail());
            avatarImage.setSrc(user.getAvatarUrl());
        }
    }
    
    public User getUser() {
        return user;
    }
    
    public void setUser(User user) {
        this.user = user;
        updateUI();
    }
}
```

## Repository Pattern

### Generic Repository Interface

```java
package com.example.repository;

import java.util.List;
import java.util.Optional;

public interface Repository<T, ID> {
    
    T save(T entity);
    
    Optional<T> findById(ID id);
    
    List<T> findAll();
    
    void delete(T entity);
    
    void deleteById(ID id);
    
    boolean existsById(ID id);
    
    long count();
}
```

### JPA Repository Implementation

```java
package com.example.repository;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;
import java.util.Optional;

public abstract class JpaRepository<T, ID> implements Repository<T, ID> {
    
    protected final Class<T> entityClass;
    
    public JpaRepository(Class<T> entityClass) {
        this.entityClass = entityClass;
    }
    
    protected abstract EntityManager getEntityManager();
    protected abstract ID getId(T entity);
    
    @Override
    public T save(T entity) {
        EntityManager em = getEntityManager();
        EntityTransaction tx = em.getTransaction();
        
        try {
            tx.begin();
            
            if (getId(entity) == null) {
                em.persist(entity);
            } else {
                entity = em.merge(entity);
            }
            
            tx.commit();
            return entity;
        } catch (Exception e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw new RuntimeException(e);
        } finally {
            em.close();
        }
    }
    
    @Override
    public Optional<T> findById(ID id) {
        EntityManager em = getEntityManager();
        try {
            T entity = em.find(entityClass, id);
            return Optional.ofNullable(entity);
        } finally {
            em.close();
        }
    }
    
    @Override
    public List<T> findAll() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("FROM " + entityClass.getSimpleName(), entityClass)
                     .getResultList();
        } finally {
            em.close();
        }
    }
    
    @Override
    public void delete(T entity) {
        EntityManager em = getEntityManager();
        EntityTransaction tx = em.getTransaction();
        
        try {
            tx.begin();
            em.remove(em.contains(entity) ? entity : em.merge(entity));
            tx.commit();
        } catch (Exception e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw new RuntimeException(e);
        } finally {
            em.close();
        }
    }
    
    @Override
    public void deleteById(ID id) {
        findById(id).ifPresent(this::delete);
    }
    
    @Override
    public boolean existsById(ID id) {
        return findById(id).isPresent();
    }
    
    @Override
    public long count() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT COUNT(e) FROM " + entityClass.getSimpleName() + " e", 
                Long.class
            ).getSingleResult();
        } finally {
            em.close();
        }
    }
}
```

### Concrete Repository

```java
package com.example.repository;

import com.example.model.User;
import javax.persistence.EntityManager;
import java.util.List;

public class UserRepository extends JpaRepository<User, Long> {
    
    public UserRepository() {
        super(User.class);
    }
    
    @Override
    protected EntityManager getEntityManager() {
        return JPAUtil.getEntityManagerFactory().createEntityManager();
    }
    
    @Override
    protected Long getId(User entity) {
        return entity.getId();
    }
    
    public Optional<User> findByEmail(String email) {
        EntityManager em = getEntityManager();
        try {
            User user = em.createQuery(
                "SELECT u FROM User u WHERE u.email = :email", User.class)
                .setParameter("email", email)
                .getSingleResult();
            return Optional.ofNullable(user);
        } catch (NoResultException e) {
            return Optional.empty();
        } finally {
            em.close();
        }
    }
    
    public List<User> findByNameContaining(String name) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT u FROM User u WHERE u.name LIKE :name", User.class)
                .setParameter("name", "%" + name + "%")
                .getResultList();
        } finally {
            em.close();
        }
    }
}
```

## Service Layer Pattern

### Service Interface

```java
package com.example.service;

import com.example.model.User;
import java.util.List;

public interface UserService {
    
    User save(User user);
    
    User findById(Long id);
    
    List<User> findAll();
    
    void delete(Long id);
    
    User authenticate(String email, String password);
    
    boolean emailExists(String email);
}
```

### Service Implementation

```java
package com.example.service;

import com.example.repository.UserRepository;
import com.example.model.User;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@Transactional
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    public UserServiceImpl(UserRepository userRepository, 
                          PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }
    
    @Override
    public User save(User user) {
        if (user.getId() == null) {
            user.setPassword(passwordEncoder.encode(user.getPassword()));
        }
        return userRepository.save(user);
    }
    
    @Override
    @Transactional(readOnly = true)
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }
    
    @Override
    @Transactional(readOnly = true)
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    @Override
    public void delete(Long id) {
        userRepository.deleteById(id);
    }
    
    @Override
    @Transactional(readOnly = true)
    public User authenticate(String email, String password) {
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new AuthenticationException("Invalid credentials"));
        
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new AuthenticationException("Invalid credentials");
        }
        
        return user;
    }
    
    @Override
    @Transactional(readOnly = true)
    public boolean emailExists(String email) {
        return userRepository.findByEmail(email).isPresent();
    }
}
```
