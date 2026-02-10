---
name: zk-framework
description: |
  Expert guide for ZK Framework (ZUL + MVC/MVVM) covering architecture, component lifecycle, patterns, version history, and best practices.
  Use when: developing ZK applications, choosing between MVC/MVVM patterns, troubleshooting ZK issues, or migrating between ZK versions.
---

# ZK Framework Expert

ZK is a Java-based Ajax framework for building enterprise web applications using server-side event-driven architecture. This skill covers ZK's full lifecycle, patterns, versions, and expert-level techniques.

## What is ZK Framework

ZK Framework is an open-source Java web framework that enables building rich internet applications (RIA) without writing JavaScript.

- **Server-Centric**: Business logic runs on server, not client
- **Event-Driven**: Component-based model with server-side event handling
- **ZUML/ZUL**: XML-based markup language for UI definition
- **Ajax Engine**: Automatic client-server synchronization via Ajax
- **Component Library**: 80+ built-in UI components (Grid, Listbox, Tree, Chart, etc.)

**Core Philosophy**: "Write Once, Run Anywhere" - developers write Java, ZK handles Ajax complexity.

## How ZK Works (Architecture)

ZK uses a server-push architecture with automatic state synchronization.

**Request Flow**:
1. Browser renders ZK components via Ajax engine (zk.js)
2. User interaction triggers client event
3. ZK Ajax engine sends event to server via AU (Ajax Update)
4. Server-side composer/ViewModel processes event
5. Server updates component tree
6. Ajax engine synchronizes delta changes to browser (no full page reload)

**Key Architecture Layers**:
- **Client Engine** (zk.js): JavaScript runtime, widget rendering
- **AU Protocol**: Delta synchronization (only changes sent, not full DOM)
- **Server Engine**: Component tree, event queue, session management
- **Data Binding**: Automatic bidirectional sync (@bind, @load, @save)

## How to choose between MVC and MVVM Patterns

ZK supports two patterns. MVVM is preferred for new projects (cleaner separation).

### MVC Pattern (Composer-based)
**Use when**: Legacy projects, simple CRUD, team unfamiliar with MVVM

- **Composer**: Java class extends `SelectorComposer<Component>`
- **Wiring**: `@Wire` annotation for component references
- **Event Handling**: `@Listen("onClick=#btnSave")` on methods
- **Data Flow**: Manual - composer explicitly updates components

**Trade-off**: Tight coupling (composer references ZUL IDs directly).

**📖 Detailed Guide**: See `references/mvc-pattern.md` for complete examples, common issues, warnings, and tips.

### MVVM Pattern (ViewModel-based)
**Use when**: New projects, complex UI logic, testability required

- **ViewModel**: POJO annotated with `@Command`, `@NotifyChange`
- **Binder**: ZK's data binder connects ZUL to ViewModel automatically
- **Event Handling**: `@Command` methods triggered via `@command('save')`
- **Data Flow**: Automatic - binder synchronizes properties via `@bind(vm.propertyName)`

**Trade-off**: Steeper learning curve, but cleaner separation and easier testing.

**📖 Detailed Guide**: See `references/mvvm-pattern.md` for complete examples, common issues, warnings, and tips.

**Migration Path**: Use MVVM for new modules, keep MVC in legacy code (ZK supports both).

## How to apply Basic Techniques

### Component Manipulation
- **Create dynamically**: `Button btn = new Button("Click"); parent.appendChild(btn);`
- **Find by ID**: `Button btn = (Button) Path.getComponent("/win/btnSave");`
- **Query selector**: `List<Button> btns = win.query("button");`
- **Event listener**: `btn.addEventListener(Events.ON_CLICK, evt -> { /* logic */ });`

### ZUL Best Practices
- **Use apply attribute**: `<window apply="org.example.MyComposer">` (MVC)
- **Use viewModel attribute**: `<window viewModel="@id('vm') @init('org.example.MyVM')">` (MVVM)
- **Avoid inline Java**: Use composers/ViewModels, not `<zscript>`
- **Style with sclass**: `<button sclass="btn-primary">` (not inline style)

### Data Binding (MVVM)
- **Load**: `<textbox value="@load(vm.username)"/>` (one-way, server → client)
- **Save**: `<textbox value="@save(vm.username)"/>` (one-way, client → server)
- **Bind**: `<textbox value="@bind(vm.username)"/>` (two-way)
- **Conditional**: `<label visible="@load(vm.count gt 0)"/>` (SpEL expression)

## How to apply Advanced Techniques

### Performance Optimization
- **Paging**: Use `Listbox` with `mold="paging" pageSize="20"` (avoid rendering 1000+ rows)
- **ROD (Render on Demand)**: Grid with `model="@load(vm.data)" mold="paging"` + lazy loading
- **Deferred rendering**: `<include mode="defer" src="heavy-panel.zul"/>` (load on visibility)
- **Client-side validation**: Use `constraint="no empty"` before server hit

### Custom Components
- **Extend existing**: `public class MyButton extends Button { ... }`
- **Composite**: Use `<apply>` to wrap reusable ZUL fragments
- **Shadow components**: Create custom tags with `.lang-addon.xml`

### Ajax Patterns
- **Server push**: Enable via `Executions.activate(desktop); Clients.showNotification(...);`
- **Long operations**: Use `EventQueues` for background tasks + UI notification
- **Polling**: `<timer delay="5000" repeats="true" onTimer="@command('refresh')"/>`

### Security
- **CSRF protection**: Built-in (ZK validates AU requests with token)
- **XSS prevention**: Escape user input via `Components.encodeText(userInput)`
- **Session fixation**: Call `session.invalidate(); Executions.sendRedirect(...)` after login

## Version History and Key Changes

### ZK 10.x (2023+)
- **Java 17+** support
- Jakarta EE 9+ (javax → jakarta namespace)
- Improved ARIA accessibility
- Modern look-and-feel updates

### ZK 9.x (2020-2022)
- **Shadow Elements**: Better custom component encapsulation
- **Webpack** integration for frontend build
- Spring Boot 2.x official support
- Deprecated `GenericForwardComposer` (use `SelectorComposer`)

### ZK 8.x (2016-2019)
- **Tablet/mobile** gestures (swipe, pinch)
- **Responsive Grid** component
- MVVM improvements (`@DependsOn` annotation)
- ZK Charts (based on Highcharts)

### ZK 7.x (2014-2015)
- **Tablet support** (touch events)
- Data binding 2.0 (cleaner syntax)
- Shadow components introduced

### ZK 6.x (2012-2013)
- **MVVM pattern** officially introduced
- Client-side binding (`@client`)
- Improved mobile support (ZK Mobile)

### ZK 5.x (2010-2011)
- Spring integration
- ROD (Render on Demand) for large datasets

### ZK 3.x-4.x (2007-2009)
- Original MVC pattern (GenericForwardComposer)
- Basic Ajax engine

**Migration Tips**:
- 6.x → 8.x: Replace `GenericForwardComposer` with `SelectorComposer`
- 8.x → 9.x: Update `javax.servlet` → `jakarta.servlet` (if using EE9+)
- Check ZK's official migration guide for breaking changes

## Compatibility Matrix

| ZK Version | Java Version | Servlet API | Spring | Jakarta EE |
|------------|--------------|-------------|--------|------------|
| 10.x | 11, 17+ | 5.0+ | 5.x, 6.x | 9+ |
| 9.x | 8, 11, 17 | 3.1+, 5.0+ | 4.x, 5.x | 8, 9 |
| 8.x | 7, 8 | 3.0+ | 3.x, 4.x | 7 |
| 7.x | 6, 7, 8 | 2.4+ | 3.x | 6 |
| 6.x | 5, 6, 7 | 2.3+ | 2.x, 3.x | 5 |

**Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge). IE11 supported up to ZK 9.x.

## Common Errors and Solutions

### Error: "Component not found"
- **Cause**: Accessing component before ZUL is fully rendered
- **Fix**: Use `@Wire` in composer or access in `doAfterCompose()`

### Error: "Unsupported browser"
- **Cause**: Using IE8-10 with ZK 9.x+
- **Fix**: Upgrade browser or downgrade to ZK 8.x

### Error: "Session timeout" on Ajax call
- **Cause**: User inactive beyond session timeout
- **Fix**: Increase timeout in `web.xml` or implement session keep-alive timer

### Error: "IllegalStateException: Component already has a parent"
- **Cause**: Trying to append same component to multiple parents
- **Fix**: Call `component.detach()` before moving to new parent

### Performance Issue: Slow Grid rendering
- **Cause**: Rendering 1000+ rows without paging
- **Fix**: Use `mold="paging"` or `model` with `ListModel` + ROD

### Memory Leak: Desktop not disposed
- **Cause**: Server push not properly closed
- **Fix**: Call `Executions.deactivate(desktop)` in finally block

## How to troubleshoot effectively

**Debug Tools**:
- **ZK DevTools**: Browser extension for component inspection
- **ZK Debug Mode**: Set `<library-property name="org.zkoss.zk.ui.debug" value="true"/>` in zk.xml
- **Server logs**: Check for `SEVERE` messages in ZK AU processing

**Common Troubleshooting Steps**:
1. Clear browser cache (ZK caches zk.wpd resources)
2. Check ZK version vs Java/Servlet version compatibility
3. Verify `zk.xml` configuration (listeners, library properties)
4. Use browser DevTools → Network to inspect AU requests
5. Enable ZK's error page (`<error-page>` in web.xml)

**Performance Profiling**:
- Use JProfiler/YourKit to detect memory leaks
- Check `DesktopCache` size (`Executions.getCurrent().getDesktop()`)
- Monitor AU request count (high frequency = inefficient binding)

## Best Practices

- **Prefer MVVM over MVC** for new projects (better testability)
- **Use ListModel/GridDataModel** for large datasets (lazy loading)
- **Avoid `zscript`**: Write logic in composers/ViewModels, not inline
- **Minimize AU requests**: Batch operations, use client-side validation
- **Stateless ViewModels**: Don't store session data in ViewModel fields
- **Version locking**: Use exact ZK version in Maven (avoid `LATEST`)
- **Test with ZK's JUnit integration**: `ZKTestCase` for UI testing
- **Monitor desktop count**: High count = memory leak (desktops not disposed)

## Community Edition vs Enterprise Edition

**ZK Community Edition (CE)** is fully functional for most applications. Core features are free:

### ✅ Community Edition (FREE)
- **All UI components**: Grid, Listbox, Tree, Window, Tabbox, Borderlayout, etc.
- **MVC & MVVM patterns**: Full support (see `references/` for details)
- **Data binding**: `@bind`, `@load`, `@save`, `@converter`, `@validator`
- **Event handling**: `@Listen`, `@Command`, `@GlobalCommand`
- **Themes**: Default (Breeze, Atlantic), Iceblue (partial)
- **Spring integration**: Full support
- **Client-side features**: JavaScript widgets, jQuery integration

### 💰 Enterprise Edition Only
- **ZK Charts**: Advanced charting component (Highcharts-based)
- **Spreadsheet**: Excel-like component with formulas
- **Pivottable**: OLAP pivot table component
- **Premium themes**: Silvertail, Atlantic (advanced features)
- **Stateless components**: Server-side rendering optimization
- **Professional support**: SLA, hotfixes, consulting

**For 95% of projects, Community Edition is sufficient.** Enterprise features are add-ons, not required.

## Official Documentation

- **ZK Framework Home**: https://www.zkoss.org/
- **Developer's Reference**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference
- **Component Reference**: https://www.zkoss.org/zkdemo/
- **MVC Pattern Guide**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVC
- **MVVM Pattern Guide**: https://www.zkoss.org/wiki/ZK_Developer%27s_Reference/MVVM
- **ZUL Reference**: https://www.zkoss.org/wiki/ZK_Component_Reference
- **Javadoc**: https://www.zkoss.org/javadoc/latest/zk/
- **Forum**: https://forum.zkoss.org/
- **GitHub**: https://github.com/zkoss/zk
