# Model-Specific Prompting Tips

Optimize prompts for ChatGPT, Claude, Gemini, and other models.

---

## ChatGPT (OpenAI GPT-4 / GPT-3.5)

**Strengths:** Versatile, creative writing, code generation, wide knowledge

**Optimization:**

1. **Use System Messages (API)**
```
System: You are a helpful assistant providing concise answers.
User: [prompt]
```

2. **Be Direct**
✅ "List 5 benefits of exercise, each in one sentence"
❌ "Tell me about exercise"

3. **Control Verbosity**
"Explain in exactly 3 sentences" or "Under 100 words"

4. **Structured Format**
"Format as: 1. Summary, 2. Key Points, 3. Recommendation"

---

## Claude (Anthropic)

**Strengths:** Long context (200K+ tokens), strong reasoning, precise instruction following

**Optimization:**

1. **XML Tags**
```
<context>
Background info
</context>

<task>
What to do
</task>

<constraints>
- Constraint 1
- Constraint 2
</constraints>
```

2. **Detailed Context**
Claude handles long documents well - include full context

3. **Explicit Constraints**
"Exactly 50 words" - Claude is very literal

4. **Leverage Strengths**
- Long document analysis
- Careful reasoning
- Complex multi-step instructions

---

## Gemini (Google)

**Strengths:** Multimodal (text + images), search integration, code, math

**Optimization:**

1. **Multimodal**
```
[Upload image]
Analyze this chart and summarize trends.
```

2. **Clear Delimiters**
```
===CONTEXT===
[info]

===TASK===
[what]

===FORMAT===
[how]
```

3. **Step-by-Step**
"Complete in order: Step 1..., Step 2..., Step 3..."

4. **Technical Precision**
"Calculate time complexity using Big O notation"

---

## Model Selection Guide

| Use Case | Best Model | Why |
|----------|-----------|-----|
| Long documents | Claude | 200K context |
| Creative writing | ChatGPT | Most creative |
| Code generation | GPT-4/Gemini | Strong technical |
| Multimodal | Gemini | Native support |
| Cost-sensitive | GPT-3.5 | Lower price |
| Reasoning | Claude/GPT-4 | Strong logic |

---

## Cross-Model Best Practices

**Universal Structure:**
```
Role: [optional]
Task: [clear]
Context: [background]
Requirements: [specific]
Format: [structure]
Input: [data]
```

**Portability Checklist:**
- [ ] Use standard delimiters
- [ ] Avoid model-specific syntax
- [ ] Be explicit about format
- [ ] Provide examples
- [ ] Test on 2+ models

---

## Performance Parameters (API)

**Temperature:**
- 0-0.3: Factual tasks
- 0.7-1.0: Creative tasks
- GPT-4: 0.3-0.7
- Claude: 0.5-0.8
- Gemini: 0.4-0.6

**Max Tokens:**
- GPT-3.5: 256-1024
- GPT-4: 512-2048
- Claude: 1024-4096
- Gemini: 1024-2048

---

## Further Reading

- Core: `../SKILL.md`
- Related: `few-shot-prompting.md`, `evaluation-testing.md`
