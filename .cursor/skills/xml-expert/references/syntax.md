# XML Syntax & Namespaces

## Basic Syntax
```xml
<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
  <book category="cooking">
    <title lang="en">Everyday Italian</title>
    <author>Giada De Laurentiis</author>
    <year>2005</year>
    <price>30.00</price>
  </book>
</bookstore>
```

## Namespaces
Avoid naming conflicts by using prefixes mapped to URIs.

```xml
<root xmlns:h="http://www.w3.org/TR/html4/"
      xmlns:f="https://www.w3schools.com/furniture">

  <h:table> <!-- HTML Table -->
    <h:tr>
      <h:td>Apples</h:td>
    </h:tr>
  </h:table>

  <f:table> <!-- Furniture Table -->
    <f:name>African Coffee Table</f:name>
    <f:width>80</f:width>
  </f:table>

</root>
```

## CDATA
Use CDATA to ignore parsing for a block of text (like code or HTML inside XML).
```xml
<script>
<![CDATA[
   function matchwo(a,b) {
      if (a < b && a < 0) then { return 1; }
   }
]]>
</script>
```
