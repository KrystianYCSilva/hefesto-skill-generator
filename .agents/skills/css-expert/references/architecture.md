---
name: architecture
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# CSS Architecture & Methodologies

## BEM (Block Element Modifier)
Keeps CSS flat and maintainable.

```css
/* Block */
.card { }

/* Element (Double underscore) */
.card__image { }
.card__title { }

/* Modifier (Double dash) */
.card--featured { }
```

## CSS Variables (Custom Properties)
Native theming support.

```css
:root {
    --primary-color: #3498db;
    --spacing-md: 16px;
}

.button {
    background-color: var(--primary-color);
    padding: var(--spacing-md);
}
```

## Scoped CSS
-   **CSS Modules**: Local scope by default (React/Vue).
-   **Shadow DOM**: Web Components isolation.

