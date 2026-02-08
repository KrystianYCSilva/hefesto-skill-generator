# Semantic HTML Guide

## Content Sectioning
-   **`<main>`**: Dominant content of the `<body>`. Unique per page.
-   **`<article>`**: Self-contained composition (Blog post, comment).
-   **`<section>`**: Thematic grouping of content, typically with a heading.
-   **`<nav>`**: Section containing navigation links.
-   **`<aside>`**: Content indirectly related to the main content (Sidebar).

## Text Semantics
-   **`<strong>`**: Strong importance (Bold).
-   **`<em>`**: Emphasized text (Italic).
-   **`<time>`**: Machine-readable dates/times (`<time datetime="2023-01-01">`).
-   **`<mark>`**: Highlighted text (Search result match).

## Bad Practices
-   Using `<b>` and `<i>` purely for styling (Use CSS).
-   Using `<br>` to create spacing between paragraphs (Use CSS `margin`).
