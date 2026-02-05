---
name: zk-framework
description: |
  Skill para desenvolvimento de aplicações web Java utilizando ZK Framework 
  (Community Edition), seguindo boas práticas de MVC/MVVM e integração com 
  ecossistema Java.
  Use quando: criar interfaces ZK com componentes ZUML (.zul), implementar 
  padrão MVC ou MVVM, integrar ZK com Spring/JPA/Jersey, migrar entre versões.
license: MIT
metadata: ./metadata.yaml
---

# ZK Framework Development

Skill para desenvolvimento de aplicações web Java utilizando ZK Framework (Community Edition), seguindo boas práticas de MVC/MVVM e integração com ecossistema Java.

---

## When to Use

Use esta skill quando precisar:

- **Criar interfaces ZK** com componentes ZUML (.zul)
- **Implementar padrão MVC** com SelectorComposer e @Wire/@Listen
- **Implementar padrão MVVM** com ViewModel e data binding
- **Integrar ZK com Spring** Framework ou Spring Boot
- **Integrar ZK com JPA/Hibernate** para persistência
- **Integrar ZK com Jersey/JAX-RS** para APIs REST
- **Migrar entre versões** do ZK (3.x até 10.x)
- **Escolher entre MVC e MVVM** para seu caso de uso

**Não use para**: ZK Enterprise Edition (EE), ZK Charts, ZK Spreadsheet, mobile-specific.

---

## Instructions

### Step 1: Analisar Contexto ZK

Antes de gerar código, identifique:

1. **Versão do ZK Framework**
   - Verifique `pom.xml` ou `build.gradle`
   - ZK 3.x-5.x: MVC clássico (GenericForwardComposer)
   - ZK 6.x+: SelectorComposer, @Wire, @Listen
   - ZK 8.x+: MVVM maduro, Shadow Elements
   - ZK 9.x-10.x: Spring Boot integration, Java 17+ support

2. **Padrão arquitetural**
   - **MVC**: Uso de Composer (controller explícito)
   - **MVVM**: Uso de ViewModel (@Command, @NotifyChange, data binding)

3. **Stack de integração**
   - Spring Framework/Boot: DI, transações
   - JPA/Hibernate: Persistência
   - Jersey/JAX-RS: APIs REST

### Step 2: Escolher Padrão MVC vs MVVM

**Use MVC quando:**
- Lógica de UI complexa e acoplada ao componente
- Controle fino sobre eventos e lifecycle
- Migração de código legado ZK 3.x-5.x
- Prototipagem rápida

**Use MVVM quando:**
- Separação clara entre UI e lógica de negócio
- Reuso de ViewModels entre diferentes UIs
- Testabilidade (ViewModels testáveis sem UI)
- Projetos novos com ZK 8.x+

### Step 3: Implementar Padrão MVC

**ZUML (.zul):**
```xml
<window title="User Management" border="normal" 
        apply="com.example.UserController">
    <listbox id="userList" rows="10">
        <listhead>
            <listheader label="Name"/>
            <listheader label="Email"/>
        </listhead>
    </listbox>
    <button id="addBtn" label="Add User"/>
</window>
```

**Controller (ZK 6.x+):**
```java
package com.example;

import org.zkoss.zk.ui.select.SelectorComposer;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zk.ui.select.annotation.Listen;
import org.zkoss.zul.*;

public class UserController extends SelectorComposer<Window> {
    
    @Wire
    private Listbox userList;
    
    @Wire
    private Button addBtn;
    
    @Override
    public void doAfterCompose(Window comp) throws Exception {
        super.doAfterCompose(comp);
        loadUsers();
    }
    
    @Listen("onClick = #addBtn")
    public void onAddUser() {
        Messagebox.show("Add user clicked");
    }
    
    private void loadUsers() {
        ListModelList<String> model = new ListModelList<>();
        model.add("John Doe");
        model.add("Jane Smith");
        userList.setModel(model);
    }
}
```

### Step 4: Implementar Padrão MVVM

**ZUML (.zul):**
```xml
<window title="User Management" border="normal" 
        viewModel="@id('vm') @init('com.example.UserViewModel')">
    <listbox model="@load(vm.users)" rows="10">
        <listhead>
            <listheader label="Name"/>
            <listheader label="Email"/>
        </listhead>
        <template name="model">
            <listitem>
                <listcell label="@load(each.name)"/>
                <listcell label="@load(each.email)"/>
            </listitem>
        </template>
    </listbox>
    <button label="Add User" onClick="@command('addUser')"/>
</window>
```

**ViewModel:**
```java
package com.example;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import java.util.List;

public class UserViewModel {
    
    @WireVariable
    private UserService userService;
    
    private List<User> users;
    
    @Init
    public void init() {
        loadUsers();
    }
    
    @Command
    @NotifyChange("users")
    public void addUser() {
        User newUser = new User("New User", "new@example.com");
        userService.save(newUser);
        loadUsers();
    }
    
    public List<User> getUsers() {
        return users;
    }
    
    private void loadUsers() {
        users = userService.findAll();
    }
}
```

### Step 5: Componentes ZK Essenciais

**Layout Components:**
```xml
<window>
    <!-- Vertical layout -->
    <vlayout spacing="10px">
        <label value="Item 1"/>
        <label value="Item 2"/>
    </vlayout>
    
    <!-- Horizontal layout -->
    <hlayout spacing="10px">
        <button label="Save"/>
        <button label="Cancel"/>
    </hlayout>
    
    <!-- Grid layout -->
    <grid>
        <rows>
            <row>
                <label value="Name:"/>
                <textbox value="@bind(vm.user.name)"/>
            </row>
            <row>
                <label value="Email:"/>
                <textbox value="@bind(vm.user.email)"/>
            </row>
        </rows>
    </grid>
</window>
```

**Input Components:**
```xml
<textbox value="@bind(vm.name)" placeholder="Enter name"/>
<intbox value="@bind(vm.age)" constraint="min 0 max 120"/>
<decimalbox value="@bind(vm.price)" format="$###,##0.00"/>
<datebox value="@bind(vm.birthDate)" format="dd/MM/yyyy"/>
<timebox value="@bind(vm.meetingTime)" format="HH:mm"/>
<combobox model="@load(vm.countries)" selectedItem="@bind(vm.selectedCountry)"/>
<checkbox checked="@bind(vm.agreed)" label="I agree"/>
<radiogroup selectedItem="@bind(vm.gender)">
    <radio label="Male" value="M"/>
    <radio label="Female" value="F"/>
</radiogroup>
```

**Data Components:**
```xml
<listbox model="@load(vm.users)" selectedItem="@bind(vm.selectedUser)">
    <listhead>
        <listheader label="Name" sort="auto(name)"/>
        <listheader label="Email" sort="auto(email)"/>
    </listhead>
    <template name="model">
        <listitem>
            <listcell label="@load(each.name)"/>
            <listcell label="@load(each.email)"/>
        </listitem>
    </template>
</listbox>

<grid model="@load(vm.users)">
    <columns>
        <column label="Name"/>
        <column label="Email"/>
    </columns>
    <template name="model">
        <row>
            <label value="@load(each.name)"/>
            <label value="@load(each.email)"/>
        </row>
    </template>
</grid>
```

### Step 6: Data Binding

**One-way binding (load):**
```xml
<label value="@load(vm.userName)"/> <!-- UI updates when VM changes -->
```

**Two-way binding (bind):**
```xml
<textbox value="@bind(vm.userName)"/> <!-- Bidirectional sync -->
```

**Command binding:**
```xml
<button label="Save" onClick="@command('save')"/>
<button label="Delete" onClick="@command('delete', user=vm.selectedUser)"/>
```

**Converter:**
```xml
<label value="@load(vm.price) @converter('formattedNumber', format='###,##0.00')"/>
<label value="@load(vm.date) @converter('formattedDate', format='dd/MM/yyyy')"/>
```

**Validator:**
```xml
<textbox value="@bind(vm.email) @validator(vm.emailValidator)"/>
```

**Java Validator:**
```java
public Validator getEmailValidator() {
    return (ValidationContext ctx) -> {
        String email = (String) ctx.getProperty().getValue();
        if (!email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
            ctx.setInvalid();
        }
    };
}
```

### Step 7: Event Handling

**MVC (Composer):**
```java
@Listen("onClick = #saveBtn")
public void onSave() {
    // Handle save
}

@Listen("onSelect = #userList")
public void onUserSelect(SelectEvent<Listitem, String> event) {
    String selected = event.getSelectedObjects().iterator().next();
}

@Listen("onChange = #searchBox")
public void onSearch(InputEvent event) {
    String query = event.getValue();
    filterUsers(query);
}
```

**MVVM (ViewModel):**
```java
@Command
public void save() {
    // Handle save
}

@Command
public void selectUser(@BindingParam("user") User user) {
    this.selectedUser = user;
}

@NotifyChange("filteredUsers")
@Command
public void search(@BindingParam("query") String query) {
    filteredUsers = userService.search(query);
}
```

### Step 8: Navigation

**Forward (same app):**
```java
Executions.sendRedirect("/users.zul");
```

**With parameters:**
```java
// Send
Map<String, Object> params = new HashMap<>();
params.put("userId", 123);
Executions.createComponents("/userDetail.zul", null, params);

// Receive
Long userId = (Long) Executions.getCurrent().getArg().get("userId");
```

**Session attributes:**
```java
// Set
Sessions.getCurrent().setAttribute("user", user);

// Get
User user = (User) Sessions.getCurrent().getAttribute("user");
```

### Step 9: Validation & Error Handling

**Client-side validation:**
```xml
<textbox constraint="no empty: Please enter a value"/>
<intbox constraint="min 0 max 100: Value must be between 0 and 100"/>
<textbox constraint="/^[A-Za-z0-9+_.-]+@(.+)$/: Invalid email"/>
```

**Server-side validation:**
```java
@Command
public void save() {
    if (user.getName() == null || user.getName().isEmpty()) {
        Clients.showNotification("Name is required", "error", null, "top_center", 3000);
        return;
    }
    
    try {
        userService.save(user);
        Clients.showNotification("User saved successfully", "info", null, "top_center", 3000);
    } catch (Exception e) {
        Clients.showNotification("Error: " + e.getMessage(), "error", null, "top_center", 5000);
    }
}
```

---

## Best Practices

### 1. Progressive Disclosure
- Use `references/` para integrações específicas (Spring, JPA, REST)
- Consulte `references/design-patterns.md` para padrões avançados
- Veja `references/customization.md` para temas e componentes customizados

### 2. MVC vs MVVM
- **MVC**: Prototipagem rápida, lógica UI-bound
- **MVVM**: Projetos complexos, testabilidade, reuso

### 3. Performance
- Use `ListModelList` com `setMultiple()` para batch updates
- Evite re-renderização desnecessária com `@NotifyChange`
- Lazy loading para datasets grandes
- Detalhes em `references/performance-optimization.md`

### 4. Security
- Sempre validar input no servidor
- Usar Spring Security para autenticação/autorização
- Sanitizar outputs para prevenir XSS

### 5. Testing
- ViewModels são POJOs: teste com JUnit diretamente
- Composers: mock componentes ZK para testes unitários
- Integração: use ZK Test Engine (ZTL)

---

## Common Patterns

**CRUD Pattern (MVVM):**
```java
public class CrudViewModel<T> {
    private List<T> entities;
    private T selected;
    
    @Init
    public void init() { load(); }
    
    @Command @NotifyChange("entities")
    public void load() { entities = service.findAll(); }
    
    @Command @NotifyChange({"entities", "selected"})
    public void save() { service.save(selected); load(); }
    
    @Command @NotifyChange({"entities", "selected"})
    public void delete() { service.delete(selected); load(); }
}
```

**Master-Detail Pattern:**
```xml
<hlayout>
    <listbox model="@load(vm.users)" selectedItem="@bind(vm.selected)" width="300px"/>
    <vlayout visible="@load(not empty vm.selected)">
        <label value="@load(vm.selected.name)"/>
        <label value="@load(vm.selected.email)"/>
    </vlayout>
</hlayout>
```

---

## References

Para integrações específicas e tópicos avançados, consulte:

- **[Spring Integration](./references/spring-integration.md)** - Spring Framework e Spring Boot
- **[JPA/Hibernate Integration](./references/jpa-hibernate-integration.md)** - Persistência e ORM
- **[REST API Integration](./references/rest-api-integration.md)** - Jersey/JAX-RS
- **[Design Patterns](./references/design-patterns.md)** - Padrões ZK-specific
- **[Customization](./references/customization.md)** - Temas, macros, client-side
- **[Advanced MVVM](./references/advanced-mvvm.md)** - Técnicas avançadas MVVM
- **[Performance Optimization](./references/performance-optimization.md)** - Best practices
- **[Migration Guide](./references/migration-guide.md)** - Migração entre versões

---

## Sources

1. **ZK Framework Official Documentation** - https://www.zkoss.org/documentation - Acessado 2026-02-05
2. **ZK MVVM Reference** - https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM - Acessado 2026-02-05
3. **ZK Spring Boot Starter** - https://github.com/zkoss/zkspringboot - Acessado 2026-02-05
4. **ZK Component Reference** - https://www.zkoss.org/zkdemo/ - Acessado 2026-02-05
5. **Baeldung ZK Framework Tutorial** - https://www.baeldung.com/zk-framework - Acessado 2026-02-05
