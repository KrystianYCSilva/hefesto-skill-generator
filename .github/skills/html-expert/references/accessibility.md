# Accessibility (a11y) Checklist

## Images
-   **Decorative**: `<img src="bg.png" alt="">` (Empty alt tells reader to skip).
-   **Informative**: `<img src="chart.png" alt="Sales increased by 20% in Q4">`.

## Forms
-   **Labels**: Visible labels are best. `placeholder` is NOT a replacement for a label.
-   **Error Handling**: Use `aria-describedby` to link input to error message text.

## Focus Management
-   **Outline**: Never remove CSS focus outline (`outline: none`) without replacing it.
-   **Skip Links**: Provide a "Skip to Main Content" link for keyboard users.

## ARIA (Accessible Rich Internet Applications)
-   **Rule #1**: Don't use ARIA if HTML can do it.
-   **Roles**: `<div role="button">` (Requires JS for Enter/Space keys). Just use `<button>`.
