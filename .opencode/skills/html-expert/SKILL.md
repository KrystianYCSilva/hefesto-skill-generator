---
name: html-expert
description: |
  Comprehensive guide for HTML5 development, focusing on semantics, accessibility (a11y), SEO, and modern best practices.
  Use when: building web pages, debugging rendering issues, auditing accessibility, or optimizing for search engines.
---

# HTML Expert

HyperText Markup Language (HTML) is the backbone of the web. Writing modern HTML means focusing on Semantics (meaning) and Accessibility (usability for all).

## How to use Semantic HTML

Use elements that describe *what* content is, not just how it looks.

-   **Structure**: `<header>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>`.
-   **Text**: `<h1>` to `<h6>` (Hierarchy), `<p>` (Paragraph), `<blockquote>` (Quotes).
-   **Interaction**: `<button>` (Actions), `<a>` (Navigation), `<input>` (Data).

## How to ensure Accessibility (a11y)

The web must be usable by everyone, including those using screen readers.

-   **Alt Text**: Always provide `alt="..."` for `<img>`.
-   **Forms**: Always link `<label for="id">` with `<input id="id">`.
-   **Keyboard**: Ensure all interactive elements are focusable (Tab key).
-   **ARIA**: Use ARIA attributes only when native HTML elements fall short.

## How to optimize for SEO

Search engines parse HTML to understand content.

-   **Meta Tags**: `<meta name="description">`, `<title>`.
-   **Headings**: Use one `<h1>` per page. Maintain strict hierarchy (`h2` inside `h1`).
-   **Links**: Use descriptive text (`<a href="...">Read report</a>` vs `Click here`).

## Common Warnings & Pitfalls

### Div Soup
-   **Issue**: Using `<div>` for everything (`<div class="button">`). No semantic meaning.
-   **Fix**: Use native elements (`<button>`, `<section>`).

### Skipping Heading Levels
-   **Issue**: `<h1>` -> `<h4>` because "it looks better".
-   **Fix**: Use CSS for styling. Keep HTML for structure (`h1` -> `h2` -> `h3`).

### Invalid Nesting
-   **Issue**: Putting a block element (`<div>`) inside an inline element (`<span>` or `<a>` in older specs).
-   **Fix**: Validate HTML against the W3C spec.

## Best Practices

| Category | Rule |
|----------|------|
| **Doctype** | Always start with `<!DOCTYPE html>`. |
| **Lang** | Always declare language: `<html lang="en">`. |
| **Charset** | Always define encoding: `<meta charset="UTF-8">`. |

## Deep Dives

-   **Semantic Elements**: See [SEMANTICS.md](references/semantics.md).
-   **Accessibility Guide**: See [ACCESSIBILITY.md](references/accessibility.md).
-   **SEO & Meta Data**: See [SEO.md](references/seo.md).

## References

-   [MDN Web Docs - HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
-   [W3C HTML Validator](https://validator.w3.org/)
-   [WebAIM Accessibility Checklist](https://webaim.org/standards/wcag/checklist)
