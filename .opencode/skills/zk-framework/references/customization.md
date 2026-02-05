# ZK Framework Customization

Complete guide to customizing ZK themes, styling, and components.

## Table of Contents

1. [Themes and CSS](#themes-and-css)
2. [Custom CSS](#custom-css)
3. [Component Extension](#component-extension)
4. [Lang Addon](#lang-addon)
5. [Client-Side Widget Override](#client-side-widget-override)
6. [Custom Renderers](#custom-renderers)

## Themes and CSS

### Built-in Themes

```xml
<!-- zk.xml -->
<zk>
    <!-- Atlantic Theme (default) -->
    <library-property>
        <name>org.zkoss.theme.preferred</name>
        <value>atlantic</value>
    </library-property>
    
    <!-- Silvertail Theme -->
    <library-property>
        <name>org.zkoss.theme.preferred</name>
        <value>silvertail</value>
    </library-property>
    
    <!-- Sapphire Theme -->
    <library-property>
        <name>org.zkoss.theme.preferred</name>
        <value>sapphire</value>
    </library-property>
</zk>
```

### Theme Switcher

```java
package com.example.util;

import org.zkoss.zk.ui.Executions;
import org.zkoss.zk.ui.Session;
import org.zkoss.zk.ui.Sessions;

public class ThemeSwitcher {
    
    private static final String THEME_COOKIE = "zktheme";
    
    public static void setTheme(String theme) {
        Session session = Sessions.getCurrent();
        session.setAttribute(THEME_COOKIE, theme);
        Executions.sendRedirect(null);
    }
    
    public static String getTheme() {
        Session session = Sessions.getCurrent();
        String theme = (String) session.getAttribute(THEME_COOKIE);
        return theme != null ? theme : "atlantic";
    }
    
    public static List<String> getAvailableThemes() {
        return Arrays.asList("atlantic", "silvertail", "sapphire");
    }
}
```

```xml
<window>
    <combobox id="themeSelector" 
              model="@load(vm.availableThemes)"
              selectedItem="@bind(vm.currentTheme)"
              onChange="@command('changeTheme')">
        <template name="model">
            <comboitem label="@load(each)" />
        </template>
    </combobox>
</window>
```

## Custom CSS

### Adding Custom CSS

```xml
<!-- global.css in webapp/css/ -->
<zk>
    <style src="/css/global.css" />
</zk>
```

```css
/* global.css */
.custom-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.custom-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.custom-listbox .z-listitem {
    border-bottom: 1px solid #e0e0e0;
    padding: 10px;
}

.custom-listbox .z-listitem:hover {
    background-color: #f5f5f5;
}

.custom-window {
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.custom-window .z-window-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px 10px 0 0;
}
```

### Using sclass Attribute

```xml
<window sclass="custom-window">
    <button label="Click Me" sclass="custom-button" />
    
    <listbox sclass="custom-listbox">
        <listitem label="Item 1" />
        <listitem label="Item 2" />
    </listbox>
</window>
```

### Dynamic Styling

```java
package com.example.composer;

public class DynamicStyleComposer extends SelectorComposer<Component> {
    
    @Wire
    private Button myButton;
    
    @Wire
    private Div container;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        applyDynamicStyles();
    }
    
    private void applyDynamicStyles() {
        myButton.setStyle("background-color: #4CAF50; color: white;");
        container.setSclass("custom-container");
    }
    
    @Listen("onClick = #myButton")
    public void onClick() {
        myButton.setStyle("background-color: #f44336; color: white;");
    }
}
```

### Inline Styles

```xml
<window style="background: #f0f0f0; padding: 20px;">
    <label value="Title" 
           style="font-size: 24px; font-weight: bold; color: #333;" />
    
    <button label="Submit" 
            style="background: #4CAF50; color: white; 
                   padding: 10px 20px; border: none;" />
</window>
```

## Component Extension

### Extending ZK Components

```java
package com.example.component;

import org.zkoss.zul.Button;

public class CustomButton extends Button {
    
    private String iconClass;
    private boolean loading = false;
    
    public CustomButton() {
        super();
        setSclass("custom-btn");
    }
    
    public CustomButton(String label) {
        super(label);
        setSclass("custom-btn");
    }
    
    @Override
    public void setLabel(String label) {
        if (loading) {
            super.setLabel("Loading...");
            setDisabled(true);
        } else {
            super.setLabel(label);
            setDisabled(false);
        }
    }
    
    public void setLoading(boolean loading) {
        this.loading = loading;
        smartUpdate("loading", loading);
        
        if (loading) {
            setIconSclass("z-icon-spinner z-icon-spin");
        } else {
            setIconSclass(iconClass);
        }
    }
    
    public boolean isLoading() {
        return loading;
    }
    
    public void setIconClass(String iconClass) {
        this.iconClass = iconClass;
        if (!loading) {
            setIconSclass(iconClass);
        }
    }
    
    public String getIconClass() {
        return iconClass;
    }
}
```

### Component Namespace Configuration

```xml
<!-- lang-addon.xml in WEB-INF -->
<?xml version="1.0" encoding="UTF-8"?>
<language-addon>
    <addon-name>custom-components</addon-name>
    <language-name>xul/html</language-name>
    
    <component>
        <component-name>customButton</component-name>
        <component-class>com.example.component.CustomButton</component-class>
    </component>
    
    <component>
        <component-name>customWindow</component-name>
        <component-class>com.example.component.CustomWindow</component-class>
    </component>
</language-addon>
```

```xml
<!-- zk.xml -->
<zk>
    <language-config>
        <addon-uri>/WEB-INF/lang-addon.xml</addon-uri>
    </language-config>
</zk>
```

### Using Custom Components

```xml
<zk xmlns:custom="custom">
    <window>
        <custom:customButton label="Save" iconClass="z-icon-save" />
        <custom:customButton label="Delete" iconClass="z-icon-trash" />
    </window>
</zk>
```

### Composite Component

```java
package com.example.component;

import org.zkoss.zk.ui.HtmlBasedComponent;
import org.zkoss.zk.ui.event.Events;
import org.zkoss.zul.*;

public class SearchBox extends Div {
    
    private Textbox searchInput;
    private Button searchButton;
    private Button clearButton;
    
    public SearchBox() {
        init();
    }
    
    private void init() {
        setSclass("search-box");
        
        searchInput = new Textbox();
        searchInput.setPlaceholder("Search...");
        searchInput.setHflex("1");
        searchInput.addEventListener(Events.ON_OK, event -> performSearch());
        
        searchButton = new Button("Search");
        searchButton.setIconSclass("z-icon-search");
        searchButton.addEventListener(Events.ON_CLICK, event -> performSearch());
        
        clearButton = new Button();
        clearButton.setIconSclass("z-icon-times");
        clearButton.addEventListener(Events.ON_CLICK, event -> clear());
        
        Hbox hbox = new Hbox();
        hbox.setWidth("100%");
        hbox.setSpacing("5px");
        hbox.appendChild(searchInput);
        hbox.appendChild(searchButton);
        hbox.appendChild(clearButton);
        
        appendChild(hbox);
    }
    
    private void performSearch() {
        Events.postEvent("onSearch", this, searchInput.getValue());
    }
    
    private void clear() {
        searchInput.setValue("");
        Events.postEvent("onClear", this, null);
    }
    
    public String getValue() {
        return searchInput.getValue();
    }
    
    public void setValue(String value) {
        searchInput.setValue(value);
    }
}
```

## Lang Addon

### Complete Lang Addon Example

```xml
<!-- lang-addon.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<language-addon>
    <addon-name>myapp-components</addon-name>
    <language-name>xul/html</language-name>
    
    <component>
        <component-name>searchBox</component-name>
        <component-class>com.example.component.SearchBox</component-class>
    </component>
    
    <component>
        <component-name>dataTable</component-name>
        <component-class>com.example.component.DataTable</component-class>
    </component>
    
    <component>
        <component-name>fileUploader</component-name>
        <component-class>com.example.component.FileUploader</component-class>
    </component>
    
    <component>
        <component-name>colorPicker</component-name>
        <component-class>com.example.component.ColorPicker</component-class>
    </component>
</language-addon>
```

### Custom Event Definition

```xml
<language-addon>
    <addon-name>myapp-components</addon-name>
    <language-name>xul/html</language-name>
    
    <component>
        <component-name>customGrid</component-name>
        <component-class>com.example.component.CustomGrid</component-class>
    </component>
    
    <event>
        <event-name>onCustomAction</event-name>
        <event-class>org.zkoss.zk.ui.event.Event</event-class>
    </event>
</language-addon>
```

## Client-Side Widget Override

### Custom Widget JavaScript

```javascript
/* CustomButton.js */
zk.$package('com.example.zkex');

com.example.zkex.CustomButton = zk.$extends(zul.wgt.Button, {
    
    _loading: false,
    
    setLoading: function(loading) {
        this._loading = loading;
        if (this.desktop) {
            this.rerender();
        }
    },
    
    getLoading: function() {
        return this._loading;
    },
    
    bind_: function() {
        this.$supers('bind_', arguments);
        
        if (this._loading) {
            this._showLoading();
        }
    },
    
    _showLoading: function() {
        var icon = this.$n('icon');
        if (icon) {
            jq(icon).addClass('z-icon-spinner z-icon-spin');
        }
        this.setDisabled(true);
    },
    
    doClick_: function(evt) {
        if (!this._loading) {
            this.$super('doClick_', evt);
        }
    }
});
```

### Widget Package Definition

```javascript
/* zk.wpd */
<package name="com.example.zkex" language="xul/html">
    <widget name="CustomButton"/>
    <widget name="CustomWindow"/>
</package>
```

### Client-Side Data Binding

```java
package com.example.component;

import org.zkoss.zk.ui.sys.ContentRenderer;
import org.zkoss.zul.Button;
import java.io.IOException;

public class CustomButton extends Button {
    
    private boolean loading;
    
    public void setLoading(boolean loading) {
        if (this.loading != loading) {
            this.loading = loading;
            smartUpdate("loading", loading);
        }
    }
    
    public boolean isLoading() {
        return loading;
    }
    
    @Override
    protected void renderProperties(ContentRenderer renderer) 
            throws IOException {
        super.renderProperties(renderer);
        
        if (loading) {
            render(renderer, "loading", loading);
        }
    }
    
    @Override
    public String getWidgetClass() {
        return "com.example.zkex.CustomButton";
    }
}
```

## Custom Renderers

### List Item Renderer

```java
package com.example.renderer;

import org.zkoss.zul.*;
import com.example.model.Product;

public class ProductRenderer implements ListitemRenderer<Product> {
    
    @Override
    public void render(Listitem item, Product product, int index) {
        item.setValue(product);
        
        new Listcell(String.valueOf(product.getId())).setParent(item);
        
        Listcell nameCell = new Listcell();
        Label nameLabel = new Label(product.getName());
        nameLabel.setStyle("font-weight: bold;");
        nameCell.appendChild(nameLabel);
        nameCell.setParent(item);
        
        Listcell priceCell = new Listcell("$" + product.getPrice());
        priceCell.setStyle("text-align: right;");
        priceCell.setParent(item);
        
        Listcell actionCell = new Listcell();
        Hbox hbox = new Hbox();
        
        Button editBtn = new Button("Edit");
        editBtn.setIconSclass("z-icon-edit");
        editBtn.addEventListener(Events.ON_CLICK, event -> {
            Events.postEvent("onEditProduct", item.getListbox(), product);
        });
        
        Button deleteBtn = new Button("Delete");
        deleteBtn.setIconSclass("z-icon-trash");
        deleteBtn.addEventListener(Events.ON_CLICK, event -> {
            Events.postEvent("onDeleteProduct", item.getListbox(), product);
        });
        
        hbox.appendChild(editBtn);
        hbox.appendChild(deleteBtn);
        actionCell.appendChild(hbox);
        actionCell.setParent(item);
        
        if (index % 2 == 0) {
            item.setSclass("even-row");
        } else {
            item.setSclass("odd-row");
        }
    }
}
```

### Using Custom Renderer

```xml
<window viewModel="@id('vm') @init('com.example.viewmodel.ProductVM')">
    <listbox model="@load(vm.products)" 
             itemRenderer="com.example.renderer.ProductRenderer"
             onEditProduct="@command('editProduct', product=event.data)"
             onDeleteProduct="@command('deleteProduct', product=event.data)">
        <listhead>
            <listheader label="ID" width="80px" />
            <listheader label="Name" />
            <listheader label="Price" width="120px" />
            <listheader label="Actions" width="150px" />
        </listhead>
    </listbox>
</window>
```

### Grid Row Renderer

```java
package com.example.renderer;

import org.zkoss.zul.*;
import com.example.model.User;

public class UserRowRenderer implements RowRenderer<User> {
    
    @Override
    public void render(Row row, User user, int index) {
        row.setValue(user);
        
        new Label(String.valueOf(user.getId())).setParent(row);
        
        Image avatar = new Image(user.getAvatarUrl());
        avatar.setWidth("40px");
        avatar.setHeight("40px");
        avatar.setParent(row);
        
        new Label(user.getName()).setParent(row);
        new Label(user.getEmail()).setParent(row);
        
        Checkbox activeCheck = new Checkbox();
        activeCheck.setChecked(user.isActive());
        activeCheck.setDisabled(true);
        activeCheck.setParent(row);
        
        Hlayout actions = new Hlayout();
        
        Toolbarbutton viewBtn = new Toolbarbutton();
        viewBtn.setIconSclass("z-icon-eye");
        viewBtn.setTooltiptext("View");
        viewBtn.addEventListener(Events.ON_CLICK, event -> {
            Events.postEvent("onViewUser", row.getGrid(), user);
        });
        
        Toolbarbutton editBtn = new Toolbarbutton();
        editBtn.setIconSclass("z-icon-edit");
        editBtn.setTooltiptext("Edit");
        editBtn.addEventListener(Events.ON_CLICK, event -> {
            Events.postEvent("onEditUser", row.getGrid(), user);
        });
        
        actions.appendChild(viewBtn);
        actions.appendChild(editBtn);
        actions.setParent(row);
    }
}
```

### Combobox Item Renderer

```java
package com.example.renderer;

import org.zkoss.zul.*;
import com.example.model.Country;

public class CountryRenderer implements ComboitemRenderer<Country> {
    
    @Override
    public void render(Comboitem item, Country country, int index) {
        item.setValue(country);
        
        Hbox hbox = new Hbox();
        hbox.setAlign("center");
        
        Image flag = new Image("/images/flags/" + country.getCode() + ".png");
        flag.setWidth("24px");
        flag.setHeight("16px");
        
        Label label = new Label(country.getName());
        label.setStyle("margin-left: 10px;");
        
        hbox.appendChild(flag);
        hbox.appendChild(label);
        
        item.appendChild(hbox);
    }
}
```

### Template-Based Rendering

```xml
<listbox model="@load(vm.products)">
    <listhead>
        <listheader label="Product" />
        <listheader label="Price" />
        <listheader label="Stock" />
    </listhead>
    
    <template name="model">
        <listitem sclass="@load(each.stock lt 10 ? 'low-stock' : '')">
            <listcell>
                <hlayout>
                    <image src="@load(each.imageUrl)" width="50px" />
                    <vlayout>
                        <label value="@load(each.name)" 
                               style="font-weight: bold;" />
                        <label value="@load(each.description)" 
                               style="color: #666; font-size: 11px;" />
                    </vlayout>
                </hlayout>
            </listcell>
            
            <listcell>
                <label value="@load(each.price) @converter('formattedNumber', format='$###,##0.00')" 
                       style="color: #4CAF50; font-weight: bold;" />
            </listcell>
            
            <listcell>
                <hlayout>
                    <label value="@load(each.stock)" />
                    <label value="Low Stock!" 
                           style="color: red; margin-left: 10px;"
                           visible="@load(each.stock lt 10)" />
                </hlayout>
            </listcell>
        </listitem>
    </template>
</listbox>
```
