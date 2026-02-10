---
name: css-expert
description: |
  Comprehensive guide for CSS (Cascading Style Sheets) mastery, covering Layout (Flexbox/Grid), Responsive Design, Architecture (BEM/Tailwind), and Animations.
  Use when: styling web pages, fixing layout bugs, organizing CSS architecture, or creating animations.
---

# CSS Expert

Cascading Style Sheets (CSS) controls the visual presentation of web pages. Mastering it requires understanding the Box Model, Cascading rules, and modern Layout systems.

## How to master Layouts

Forget `float` and `table`. Use modern layout engines.

-   **Flexbox**: 1D layout (Row OR Column). Best for components, navigation bars, centering items.
-   **CSS Grid**: 2D layout (Rows AND Columns). Best for page skeletons, complex galleries.
-   **Positioning**: `absolute`, `relative`, `fixed`, `sticky` for overlaying elements.

## How to implement Responsive Design

"Mobile First" is the standard.

-   **Media Queries**: `@media (min-width: 768px) { ... }`. Define base styles for mobile, add complexity for larger screens.
-   **Fluid Units**: Use `%`, `vw/vh`, `rem` instead of fixed `px`.
-   **Images**: `max-width: 100%; height: auto;` to prevent overflow.

## How to organize CSS Architecture

Avoid "Spaghetti CSS" in large projects.

-   **BEM (Block Element Modifier)**: Naming convention (`.card__button--primary`) to isolate styles.
-   **Utility-First (Tailwind)**: Composing designs directly in HTML (`class="p-4 bg-blue-500 text-white"`).
-   **CSS Variables**: `--main-color: #333;` for theming and maintainability.

## Common Warnings & Pitfalls

### The `z-index` War
-   **Issue**: Elements overlapping incorrectly because of `z-index: 9999`.
-   **Fix**: Manage Stacking Contexts. `z-index` only works on positioned elements (`relative`, `absolute`).

### Specificity Wars
-   **Issue**: Using `!important` to override styles.
-   **Fix**: Understand specificity (`ID > Class > Tag`). Reduce selector complexity.

### Box Model Confusion
-   **Issue**: Padding increases element size unexpectedly.
-   **Fix**: Always use `* { box-sizing: border-box; }` reset.

## Best Practices

| Concept | Rule |
|---------|------|
| **Reset/Normalize** | Start with a reset to remove browser default inconsistencies. |
| **Shorthand** | Use `margin: 10px 20px;` instead of 4 separate lines (when clear). |
| **Performance** | Avoid expensive properties like `box-shadow` or `filter` on scroll-heavy elements. |

## Deep Dives

-   **Layout (Flex/Grid)**: See [LAYOUT.md](references/layout.md).
-   **Responsive Design**: See [RESPONSIVE.md](references/responsive.md).
-   **Architecture (BEM)**: See [ARCHITECTURE.md](references/architecture.md).

## References

-   [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
-   [CSS-Tricks Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
-   [CSS-Tricks Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
