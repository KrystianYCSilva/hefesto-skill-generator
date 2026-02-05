# Clean Code Guide

Comprehensive guide to writing clean, maintainable code following industry best practices.

## Naming Conventions

### Use Intention-Revealing Names
Variables, functions, and classes should reveal intent without needing comments.

### Variables
- Use nouns for variables
- Boolean variables: is_active, has_permission, can_edit
- Avoid single letter names (except loop counters)

### Functions
- Use verbs: calculate_total, send_email, validate_input
- Boolean functions: is_valid, has_errors, can_proceed

### Classes
- Use nouns: Customer, OrderProcessor, EmailValidator
- Avoid generic names: Manager, Data, Info

## Functions Should Be Small
Target: 5-15 lines per function
- Do one thing
- One level of abstraction per function
- Minimize arguments (0-2 ideal)

## Error Handling
- Use exceptions, not error codes
- Don't return null
- Don't pass null

## Comments
Good: Explain why, not what
Bad: Redundant, misleading, commented-out code

## Formatting
- Consistent indentation
- Lines under 120 characters
- Blank lines separate concepts
- Related code stays together

## Boy Scout Rule
Leave code cleaner than you found it.
