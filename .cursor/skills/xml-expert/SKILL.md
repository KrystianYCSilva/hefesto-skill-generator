---
name: xml-expert
description: |
  Comprehensive guide for XML technologies, including parsing, validation (XSD), transformation (XSLT), and best practices.
  Use when: processing XML data, designing schemas, debugging SOAP APIs, or configuring legacy systems.
---

# XML Expert

eXtensible Markup Language (XML) is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. Despite the rise of JSON, XML remains critical in enterprise, finance, and configuration.

## How to structure XML

XML must be **Well-Formed** to be parsed.

-   **Root Element**: Single root node (e.g., `<config>...</config>`).
-   **Tags**: Case-sensitive, must be closed properly (`<tag></tag>` or `<tag/>`).
-   **Attributes**: Values must be quoted (`id="123"`).
-   **Escaping**: Use entities for special chars: `<` (`&lt;`), `>` (`&gt;`), `&` (`&amp;`).

## How to validate XML (Schemas)

Validation ensures XML structure matches expectations.

-   **XSD (XML Schema Definition)**: The industry standard. Strong typing, namespaces.
-   **DTD (Document Type Definition)**: Legacy. simpler but limited.
-   **Schematron**: Rule-based validation (e.g., "End date must be after Start date").

## How to transform XML (XSLT)

XSLT (Extensible Stylesheet Language Transformations) transforms XML into other formats (HTML, PDF, JSON, or other XML).

-   **Template Matching**: `<xsl:template match="/">`.
-   **Iteration**: `<xsl:for-each select="item">`.
-   **XPath**: Query language to select nodes (`/catalog/book[@id='bk101']`).

## Common Warnings & Pitfalls

### XXE Injection (Security)
-   **Issue**: XML External Entity attacks allows reading system files (`/etc/passwd`).
-   **Fix**: Disable external entities resolution in your XML parser configuration.

### Namespace Hell
-   **Issue**: Tag collision (`<table:tr>` vs `<furniture:table>`).
-   **Fix**: Use XML Namespaces strictly (`xmlns:h="http://www.w3.org/TR/html4/"`).

### Whitespace Handling
-   **Issue**: Parsers might treat indentation as text nodes.
-   **Fix**: Configure parser to ignore whitespace or use `xml:space="preserve"`.

## Best Practices

| Aspect | Recommendation |
|--------|----------------|
| **Attributes vs Elements** | Use **Attributes** for metadata (ID, type). Use **Elements** for data/content. |
| **Encoding** | Always specify `<?xml version="1.0" encoding="UTF-8"?>`. |
| **Parsing** | Prefer **SAX/StAX** (Streaming) for large files (>10MB). Use **DOM** for small files requiring random access. |

## Deep Dives

-   **Syntax & Namespaces**: See [SYNTAX.md](references/syntax.md).
-   **XSD Validation**: See [SCHEMAS.md](references/schemas.md).
-   **Processing & Parsing**: See [PROCESSING.md](references/processing.md).

## References

-   [W3C XML Specification](https://www.w3.org/XML/)
-   [W3 Schools XML Tutorial](https://www.w3schools.com/xml/)
-   [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
