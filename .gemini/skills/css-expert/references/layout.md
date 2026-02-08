# Modern CSS Layout

## The Box Model
Every element is a box.
-   **Content**: The text/image.
-   **Padding**: Space between content and border. (Internal).
-   **Border**: The line around the padding.
-   **Margin**: Space outside the border. (External).

## Flexbox (1D)
`display: flex;`
-   **Justify Content** (Main Axis): `flex-start`, `center`, `space-between`.
-   **Align Items** (Cross Axis): `stretch`, `center`, `flex-start`.
-   **Gap**: `gap: 1rem;` (Spacing between items).

## Grid (2D)
`display: grid;`
-   **Columns**: `grid-template-columns: repeat(3, 1fr);` (3 equal columns).
-   **Areas**: Name areas for layout.
    ```css
    grid-template-areas:
        "header header"
        "sidebar main";
    ```

## Centering (The Holy Grail)
```css
.center-me {
    display: grid;
    place-items: center;
    /* OR */
    display: flex;
    justify-content: center;
    align-items: center;
}
```
