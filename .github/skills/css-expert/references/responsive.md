# Responsive Design Guide

## Viewport Meta Tag
Essential for mobile browsers to render correctly.
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## Breakpoints (Mobile First)
Start with mobile styles (no media query), then add:
```css
/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1024px) { ... }
```

## Responsive Units
-   **rem**: Root EM. Relative to html font-size (usually 16px). Accessible scaling.
-   **em**: Relative to parent font-size. Good for local component scaling.
-   **vw / vh**: % of Viewport Width/Height. Good for hero sections (`height: 100vh`).
-   **ch**: Character unit. Good for readable line lengths (`max-width: 65ch`).
