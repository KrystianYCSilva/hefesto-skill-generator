# Quality Checklist (Auto-Critica)

> This checklist is used by AI agents during `/hefesto.create` and `/hefesto.validate`
> to self-review generated skills. Every item MUST pass before presenting to the user.

---

## 10-Point Checklist

### 1. Frontmatter Valid

- [ ] YAML frontmatter present (between `---` markers)
- [ ] `name` field: lowercase, hyphens, max 64 chars, pattern `^[a-z0-9]+(-[a-z0-9]+)*$`
- [ ] `description` field: non-empty, max 1024 chars
- [ ] Directory name matches `name` field exactly

**Severity:** CRITICAL

---

### 2. Size Limits

- [ ] SKILL.md < 500 lines
- [ ] SKILL.md < ~5000 tokens (estimate: lines * 10)
- [ ] No single section exceeds 100 lines

**Severity:** CRITICAL

---

### 3. Description Quality

- [ ] Description is specific enough for skill discovery (~100 tokens)
- [ ] Starts with action verb (e.g., "Guides", "Validates", "Generates")
- [ ] Contains "Use when:" trigger phrase
- [ ] Does NOT repeat the skill name verbatim

**Severity:** CRITICAL

---

### 4. Conciseness

- [ ] No obvious explanations (e.g., "HTML is a markup language")
- [ ] No filler phrases ("It is important to note that...")
- [ ] Prefers tables/lists over prose paragraphs
- [ ] Each sentence adds unique value

**Severity:** WARNING

---

### 5. Examples

- [ ] At least 1 concrete input/output example
- [ ] Examples use realistic data (not "foo", "bar", "example.com")
- [ ] Examples demonstrate the core use case

**Severity:** WARNING

---

### 6. Terminology Consistency

- [ ] Same concept uses same term throughout
- [ ] No mixing of synonyms (e.g., "function" vs "method" without reason)
- [ ] Technical terms match official documentation

**Severity:** WARNING

---

### 7. Degrees of Freedom

- [ ] High freedom: suggestions with "consider", "you may"
- [ ] Medium freedom: recommendations with "prefer", "recommended"
- [ ] Low freedom: rules with "MUST", "NEVER", "always"
- [ ] Freedom level is appropriate for skill type

**Severity:** INFO

---

### 8. Official Sources

- [ ] Min 2 official/academic sources for technical skills
- [ ] Sources are authoritative (official docs, RFCs, standards)
- [ ] Links are inline, not just URLs
- [ ] Non-technical/workflow skills may have 0 sources (acceptable)

**Severity:** WARNING (technical skills) / INFO (non-technical)

---

### 9. Reference Depth

- [ ] References are max 1 level deep (no references referencing references)
- [ ] JIT resources in `references/` are truly optional
- [ ] Core instructions remain in SKILL.md, not in references

**Severity:** WARNING

---

### 10. Security

- [ ] No API keys, tokens, passwords, or secrets
- [ ] No hardcoded credentials
- [ ] No personally identifiable information (PII)
- [ ] No internal/private URLs

**Severity:** CRITICAL

---

## Grading

| Grade   | Criteria                              |
|---------|---------------------------------------|
| PASS    | 0 CRITICAL fails, 0-2 WARNING        |
| PARTIAL | 0 CRITICAL fails, 3+ WARNING         |
| FAIL    | 1+ CRITICAL fail                      |

## Auto-Critica Process

1. Run all 10 checks against generated skill
2. For each FAIL: fix immediately before proceeding
3. Document corrections in "Auto-Critica Notes" section
4. Re-run failed checks after correction
5. Only present to user when grade >= PARTIAL
6. If PARTIAL: warn user about remaining warnings
