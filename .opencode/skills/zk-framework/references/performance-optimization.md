# ZK Framework Performance Optimization

Techniques for optimizing ZK application performance and scalability.

## Table of Contents

1. [ListModelList Optimization](#listmodellist-optimization)
2. [Lazy Loading](#lazy-loading)
3. [Paging](#paging)
4. [Caching Strategies](#caching-strategies)
5. [Component Lifecycle](#component-lifecycle)
6. [Memory Management](#memory-management)

## ListModelList Optimization

### Batch Updates

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zul.ListModelList;

public class OptimizedListVM {
    
    private ListModelList<Product> products;
    
    @Init
    public void init() {
        products = new ListModelList<>();
        loadProducts();
    }
    
    @Command
    @NotifyChange("products")
    public void loadProducts() {
        List<Product> data = productService.findAll();
        
        products.clear();
        products.addAll(data);
    }
    
    @Command
    public void addMultipleProducts(@BindingParam("newProducts") List<Product> newProducts) {
        products.addAll(newProducts);
    }
    
    @Command
    public void removeMultipleProducts(@BindingParam("ids") List<Long> ids) {
        List<Product> toRemove = products.stream()
            .filter(p -> ids.contains(p.getId()))
            .collect(Collectors.toList());
        
        products.removeAll(toRemove);
    }
    
    public ListModelList<Product> getProducts() {
        return products;
    }
}
```

### Efficient List Updates

```java
// WRONG: Multiple individual updates
@Command
@NotifyChange("products")
public void updatePrices(Map<Long, BigDecimal> priceUpdates) {
    for (Map.Entry<Long, BigDecimal> entry : priceUpdates.entrySet()) {
        Product product = findProductById(entry.getKey());
        if (product != null) {
            product.setPrice(entry.getValue());
            int index = products.indexOf(product);
            products.set(index, product); // Triggers update each time
        }
    }
}

// CORRECT: Batch update
@Command
@NotifyChange("products")
public void updatePrices(Map<Long, BigDecimal> priceUpdates) {
    List<Product> updated = new ArrayList<>();
    
    for (Product product : products) {
        if (priceUpdates.containsKey(product.getId())) {
            product.setPrice(priceUpdates.get(product.getId()));
            updated.add(product);
        }
    }
    
    products.removeAll(updated);
    products.addAll(updated);
}
```

### Custom List Model for Large Datasets

```java
package com.example.model;

import org.zkoss.zul.AbstractListModel;
import org.zkoss.zul.ext.Sortable;
import java.util.Comparator;

public class PagedListModel<E> extends AbstractListModel<E> implements Sortable<E> {
    
    private List<E> cache;
    private int totalSize;
    private int pageSize;
    private int currentPage;
    private DataProvider<E> dataProvider;
    
    public interface DataProvider<E> {
        List<E> getPage(int page, int pageSize);
        int getTotalSize();
    }
    
    public PagedListModel(DataProvider<E> dataProvider, int pageSize) {
        this.dataProvider = dataProvider;
        this.pageSize = pageSize;
        this.currentPage = 0;
        this.totalSize = dataProvider.getTotalSize();
        loadPage(0);
    }
    
    @Override
    public E getElementAt(int index) {
        int page = index / pageSize;
        
        if (page != currentPage) {
            loadPage(page);
        }
        
        int localIndex = index % pageSize;
        return cache.get(localIndex);
    }
    
    @Override
    public int getSize() {
        return totalSize;
    }
    
    private void loadPage(int page) {
        cache = dataProvider.getPage(page, pageSize);
        currentPage = page;
    }
    
    @Override
    public void sort(Comparator<E> cmpr, boolean ascending) {
        cache.sort(ascending ? cmpr : cmpr.reversed());
        fireEvent(ListDataEvent.CONTENTS_CHANGED, -1, -1);
    }
    
    public void refresh() {
        totalSize = dataProvider.getTotalSize();
        loadPage(currentPage);
        fireEvent(ListDataEvent.CONTENTS_CHANGED, -1, -1);
    }
}
```

## Lazy Loading

### Lazy List Loading

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;

public class LazyProductVM {
    
    private List<Product> products;
    private boolean loaded = false;
    
    @Command
    @NotifyChange({"products", "loaded"})
    public void loadData() {
        if (!loaded) {
            products = productService.findAll();
            loaded = true;
        }
    }
    
    public List<Product> getProducts() {
        return products;
    }
    
    public boolean isLoaded() {
        return loaded;
    }
}
```

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.LazyProductVM')">
    <button label="Load Products" 
            onClick="@command('loadData')" 
            visible="@load(!vm.loaded)" />
    
    <listbox model="@load(vm.products)" 
             visible="@load(vm.loaded)">
        <template name="model">
            <listitem>
                <listcell label="@load(each.name)" />
                <listcell label="@load(each.price)" />
            </listitem>
        </template>
    </listbox>
</window>
```

### Infinite Scroll Pattern

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zul.ListModelList;

public class InfiniteScrollVM {
    
    private ListModelList<Product> products;
    private int currentPage = 0;
    private int pageSize = 20;
    private boolean hasMore = true;
    
    @Init
    public void init() {
        products = new ListModelList<>();
        loadMore();
    }
    
    @Command
    @NotifyChange({"products", "hasMore"})
    public void loadMore() {
        if (!hasMore) {
            return;
        }
        
        List<Product> newProducts = productService.findPage(currentPage, pageSize);
        
        if (newProducts.isEmpty() || newProducts.size() < pageSize) {
            hasMore = false;
        }
        
        products.addAll(newProducts);
        currentPage++;
    }
    
    public ListModelList<Product> getProducts() {
        return products;
    }
    
    public boolean isHasMore() {
        return hasMore;
    }
}
```

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.InfiniteScrollVM')">
    <listbox model="@load(vm.products)" height="400px" 
             onScrollEnd="@command('loadMore')">
        <template name="model">
            <listitem>
                <listcell label="@load(each.name)" />
                <listcell label="@load(each.price)" />
            </listitem>
        </template>
    </listbox>
    
    <button label="Load More" 
            onClick="@command('loadMore')"
            visible="@load(vm.hasMore)" />
</window>
```

## Paging

### Basic Paging with Listbox

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zul.ListModelList;

public class PagedProductVM {
    
    private ListModelList<Product> products;
    private int activePage = 0;
    private int pageSize = 20;
    private int totalSize = 0;
    
    @Init
    public void init() {
        loadPage();
    }
    
    @Command
    @NotifyChange({"products", "totalSize", "activePage"})
    public void loadPage() {
        List<Product> data = productService.findPage(activePage, pageSize);
        products = new ListModelList<>(data);
        totalSize = productService.count();
    }
    
    @Command
    @NotifyChange("*")
    public void changePage(@BindingParam("page") int page) {
        activePage = page;
        loadPage();
    }
    
    @Command
    @NotifyChange("*")
    public void nextPage() {
        if ((activePage + 1) * pageSize < totalSize) {
            activePage++;
            loadPage();
        }
    }
    
    @Command
    @NotifyChange("*")
    public void previousPage() {
        if (activePage > 0) {
            activePage--;
            loadPage();
        }
    }
    
    public int getTotalPages() {
        return (int) Math.ceil((double) totalSize / pageSize);
    }
    
    public ListModelList<Product> getProducts() {
        return products;
    }
    
    public int getActivePage() {
        return activePage;
    }
    
    public int getTotalSize() {
        return totalSize;
    }
}
```

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.PagedProductVM')">
    <listbox model="@load(vm.products)">
        <listhead>
            <listheader label="Name" />
            <listheader label="Price" />
        </listhead>
        <template name="model">
            <listitem>
                <listcell label="@load(each.name)" />
                <listcell label="@load(each.price)" />
            </listitem>
        </template>
    </listbox>
    
    <paging totalSize="@load(vm.totalSize)" 
            pageSize="20"
            activePage="@bind(vm.activePage)"
            onPaging="@command('loadPage')" />
</window>
```

### Server-Side Paging

```java
package com.example.dao;

public class ProductDAO {
    
    public List<Product> findPage(int page, int pageSize) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("SELECT p FROM Product p ORDER BY p.name", Product.class)
                     .setFirstResult(page * pageSize)
                     .setMaxResults(pageSize)
                     .getResultList();
        } finally {
            em.close();
        }
    }
    
    public long count() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("SELECT COUNT(p) FROM Product p", Long.class)
                     .getSingleResult();
        } finally {
            em.close();
        }
    }
    
    public List<Product> findPageWithFilters(String nameFilter, int page, int pageSize) {
        EntityManager em = getEntityManager();
        try {
            CriteriaBuilder cb = em.getCriteriaBuilder();
            CriteriaQuery<Product> cq = cb.createQuery(Product.class);
            Root<Product> root = cq.from(Product.class);
            
            if (nameFilter != null && !nameFilter.isEmpty()) {
                cq.where(cb.like(root.get("name"), "%" + nameFilter + "%"));
            }
            
            return em.createQuery(cq)
                     .setFirstResult(page * pageSize)
                     .setMaxResults(pageSize)
                     .getResultList();
        } finally {
            em.close();
        }
    }
}
```

## Caching Strategies

### Session-Level Caching

```java
package com.example.cache;

import org.zkoss.zk.ui.Session;
import org.zkoss.zk.ui.Sessions;

public class SessionCache {
    
    private static final String CACHE_PREFIX = "cache_";
    
    public static <T> void put(String key, T value, int ttlSeconds) {
        Session session = Sessions.getCurrent();
        CacheEntry<T> entry = new CacheEntry<>(value, ttlSeconds);
        session.setAttribute(CACHE_PREFIX + key, entry);
    }
    
    public static <T> T get(String key) {
        Session session = Sessions.getCurrent();
        CacheEntry<T> entry = (CacheEntry<T>) session.getAttribute(CACHE_PREFIX + key);
        
        if (entry != null && !entry.isExpired()) {
            return entry.getValue();
        }
        
        return null;
    }
    
    public static void remove(String key) {
        Session session = Sessions.getCurrent();
        session.removeAttribute(CACHE_PREFIX + key);
    }
    
    public static void clear() {
        Session session = Sessions.getCurrent();
        session.getAttributes().keySet().stream()
            .filter(key -> key.toString().startsWith(CACHE_PREFIX))
            .forEach(session::removeAttribute);
    }
    
    static class CacheEntry<T> {
        private final T value;
        private final long expiryTime;
        
        CacheEntry(T value, int ttlSeconds) {
            this.value = value;
            this.expiryTime = System.currentTimeMillis() + (ttlSeconds * 1000L);
        }
        
        T getValue() {
            return value;
        }
        
        boolean isExpired() {
            return System.currentTimeMillis() > expiryTime;
        }
    }
}
```

### Using Cache in ViewModel

```java
public class CachedProductVM {
    
    private static final String PRODUCTS_CACHE_KEY = "products_list";
    private List<Product> products;
    
    @Init
    public void init() {
        loadProducts();
    }
    
    @Command
    @NotifyChange("products")
    public void loadProducts() {
        products = SessionCache.get(PRODUCTS_CACHE_KEY);
        
        if (products == null) {
            products = productService.findAll();
            SessionCache.put(PRODUCTS_CACHE_KEY, products, 300);
        }
    }
    
    @Command
    @NotifyChange("products")
    public void refreshProducts() {
        SessionCache.remove(PRODUCTS_CACHE_KEY);
        products = productService.findAll();
        SessionCache.put(PRODUCTS_CACHE_KEY, products, 300);
    }
    
    public List<Product> getProducts() {
        return products;
    }
}
```

### Application-Level Cache with Caffeine

```xml
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
    <version>3.1.8</version>
</dependency>
```

```java
package com.example.cache;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.util.concurrent.TimeUnit;

public class AppCache {
    
    private static final Cache<String, Object> cache = Caffeine.newBuilder()
        .maximumSize(1000)
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .build();
    
    public static <T> void put(String key, T value) {
        cache.put(key, value);
    }
    
    public static <T> T get(String key) {
        return (T) cache.getIfPresent(key);
    }
    
    public static void remove(String key) {
        cache.invalidate(key);
    }
    
    public static void clear() {
        cache.invalidateAll();
    }
}
```

## Component Lifecycle

### Efficient Component Initialization

```java
// WRONG: Heavy processing in constructor
public class ProductComposer extends SelectorComposer<Component> {
    
    public ProductComposer() {
        loadAllProducts(); // Don't do this!
    }
}

// CORRECT: Lazy initialization
public class ProductComposer extends SelectorComposer<Component> {
    
    private List<Product> products;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        
        Events.echoEvent("onLazyLoad", comp, null);
    }
    
    @Listen("onLazyLoad = #win")
    public void onLazyLoad() {
        if (products == null) {
            products = loadProducts();
            updateUI();
        }
    }
}
```

### Component Detachment

```java
public class ResourceAwareComposer extends SelectorComposer<Component> {
    
    private Timer timer;
    private Connection dbConnection;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        
        timer = new Timer();
        dbConnection = getConnection();
    }
    
    @Listen("onDetach = #win")
    public void cleanup() {
        if (timer != null) {
            timer.cancel();
            timer = null;
        }
        
        if (dbConnection != null) {
            try {
                dbConnection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
            dbConnection = null;
        }
    }
}
```

## Memory Management

### Preventing Memory Leaks

```java
// WRONG: Static reference to UI components
public class LeakyComposer extends SelectorComposer<Component> {
    
    private static Listbox listbox; // Memory leak!
    
    @Wire
    private Listbox myListbox;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        listbox = myListbox; // Don't do this!
    }
}

// CORRECT: Instance references only
public class ProperComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox listbox;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
    }
}
```

### Event Listener Cleanup

```java
public class EventAwareComposer extends SelectorComposer<Component> {
    
    private EventListener<Event> customListener;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        
        customListener = event -> {
            handleCustomEvent(event);
        };
        
        EventQueues.lookup("globalQueue", EventQueues.APPLICATION, true)
            .subscribe(customListener);
    }
    
    @Listen("onDetach = #win")
    public void cleanup() {
        EventQueue<Event> queue = EventQueues.lookup("globalQueue", 
            EventQueues.APPLICATION, false);
        
        if (queue != null && customListener != null) {
            queue.unsubscribe(customListener);
        }
    }
}
```

### Efficient Data Transfer Objects

```java
// WRONG: Sending entire entity
@Command
public void updateProduct() {
    Product product = productService.findById(1L); // Full entity with all relations
    Clients.showNotification("Product: " + product.toString());
}

// CORRECT: Use DTOs
@Command
public void updateProduct() {
    ProductDTO dto = productService.findDTOById(1L);
    Clients.showNotification("Product: " + dto.getName());
}

class ProductDTO {
    private Long id;
    private String name;
    private BigDecimal price;
    
    // Only essential fields, no relations
}
```

### Detach Large Objects

```java
public class OptimizedVM {
    
    @Command
    @NotifyChange("products")
    public void loadProducts() {
        List<Product> fullProducts = productService.findAll();
        
        products = fullProducts.stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }
    
    private ProductDTO toDTO(Product product) {
        ProductDTO dto = new ProductDTO();
        dto.setId(product.getId());
        dto.setName(product.getName());
        dto.setPrice(product.getPrice());
        return dto;
    }
}
```
