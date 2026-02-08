# Skill Template Reference

> This is the canonical template for generating skills compatible with the
> [agentskills.io](https://agentskills.io) specification. AI agents MUST follow
> this structure when creating new skills via `/hefesto.create`.

---

## Frontmatter (Required)

```yaml
---
name: <skill-name>
description: |
  <One paragraph, max 1024 chars. Start with action verb.>
  Use when: <specific trigger condition for discovery>.
---
```

### Frontmatter Rules

| Field       | Constraint                                          |
|-------------|-----------------------------------------------------|
| name        | lowercase, hyphens only, max 64 chars               |
| name format | `^[a-z0-9]+(-[a-z0-9]+)*$` (no consecutive hyphens) |
| description | max 1024 chars, non-empty                           |
| description | ~100 tokens ideal for discovery                     |
| description | MUST include "Use when:" trigger phrase              |

---

## SKILL.md Structure

```markdown
---
name: example-skill
description: |
  Guides implementation of X following best practices and patterns.
  Use when: creating, reviewing, or refactoring X in projects.
---

# example-skill

<Brief introduction: what this skill does and why it matters. 2-3 sentences max.>

## Instructions

<Step-by-step workflow. Use numbered lists for sequential steps.
Use bullet lists for non-sequential guidance.>

1. Step one
2. Step two
3. Step three

## Key Concepts

<Core knowledge the agent needs. Be concise - "concise is key" (Anthropic).
Prefer tables and lists over prose.>

## Examples

<At least 1 concrete input/output example. Show real usage, not abstract.>

### Example 1: <Descriptive Title>

**Input:** <what the user provides>

**Output:** <what the agent produces>

## References

<Min 2 official sources for technical skills. Use inline links.>

- [Official Documentation](https://...)
- [RFC/Standard](https://...)
```

---

## Progressive Disclosure Rules

| Constraint           | Limit                    |
|----------------------|--------------------------|
| SKILL.md lines       | max 500                  |
| SKILL.md tokens      | max ~5000                |
| Reference depth      | 1 level only             |
| References files     | Only if SKILL.md > 300 lines |

### When to use `references/`

Create `references/*.md` files when:
- SKILL.md would exceed 300 lines without them
- Detailed lookup tables or API references are needed
- Content is "just-in-time" (read only when needed)

Do NOT use references for:
- Core instructions (keep in SKILL.md)
- Examples (keep in SKILL.md)
- Content that is always needed

---

## Directory Structure

```
<skill-name>/
  SKILL.md              # Required - main skill file
  references/           # Optional - JIT deep-dive resources
    <topic>.md
  scripts/              # Optional - executable helpers
    <script>.<ext>
  assets/               # Optional - images, data files
    <file>.<ext>
```

---

## Naming Convention

| Rule                  | Example                    |
|-----------------------|----------------------------|
| Use lowercase         | `validate-email`           |
| Use hyphens           | `java-fundamentals`        |
| Be descriptive        | `react-testing-patterns`   |
| Domain first          | `python-error-handling`    |
| Max 64 chars          | -                          |
| No consecutive hyphens| `my-skill` not `my--skill` |

---

## Quality Indicators

A good skill MUST:
- [ ] Have a specific "Use when:" trigger in description
- [ ] Be concise (no obvious explanations)
- [ ] Include at least 1 concrete example
- [ ] Use consistent terminology throughout
- [ ] Have numbered steps for workflows
- [ ] Reference official sources (min 2 for technical skills)
- [ ] Contain no credentials or secrets
- [ ] Stay under 500 lines / ~5000 tokens
