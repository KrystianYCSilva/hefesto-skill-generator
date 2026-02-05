# Chain-of-Thought Prompting - Deep Dive

Comprehensive guide to Chain-of-Thought (CoT) prompting for step-by-step reasoning.

---

## Overview

**Chain-of-Thought (CoT)** enhances LLM performance on complex reasoning by embedding intermediate steps. Instead of jumping to answers, models articulate their thought process.

**Core insight:** Showing logical steps teaches systematic thinking, leading to more accurate results.

---

## Basic Implementation

### Simple Trigger Phrase

```
Problem: A farmer has 17 sheep. All but 9 die. How many are left?

Let's think step by step:
```

**Common triggers:**
- "Let's think step by step:"
- "Let's break this down:"
- "Let's approach this systematically:"

### Few-Shot CoT (Recommended)

```
Q: If 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets?

A: Let's think step by step:
- 5 machines make 5 widgets in 5 minutes
- Each machine makes 1 widget in 5 minutes
- 100 machines each make 1 widget in 5 minutes
- Therefore: 5 minutes

Q: [Your problem]
A: Let's think step by step:
```

---

## Use Cases

**Multi-Step Math:**
```
Problem: Store has 25% off, then additional 10% off sale price. $80 item?

Step 1: Apply 25%: $80 × 0.75 = $60
Step 2: Apply 10%: $60 × 0.90 = $54
Answer: $54
```

**Logical Reasoning:**
```
Premise: All programmers know ≥1 language. Sarah is a programmer.
Question: Does Sarah know ≥1 language?

Reasoning:
1. Universal rule: programmers → know ≥1 language
2. Sarah is a programmer (given)
3. Apply rule: Sarah knows ≥1 language
Answer: Yes
```

**Code Debugging:**
```
Code crashes with empty list. Let's debug:
1. Trace: numbers = [], sum = 0, loop skips
2. Return: sum / len(numbers) = 0 / 0
3. Issue: Division by zero
4. Fix: Validate input before calculation
```

---

## Best Practices

1. **Use for complex tasks**: Math, logic, multi-step problems
2. **Skip for simple tasks**: "What is 2+2?" doesn't need CoT
3. **Make steps concrete**: Avoid vague "think about it" steps
4. **Add verification**: Check if answer satisfies constraints

---

## Performance Impact

Research shows significant improvements:
- Math (GSM8K): 55% → 74% (+19%)
- Symbolic reasoning: ~60% → ~95% (+35%)

**Critical:** Works best with models ≥100B parameters. Smaller models may produce illogical chains.

---

## Advanced Variants

**Self-Consistency CoT:** Generate multiple reasoning paths, select most common answer.

**Least-to-Most:** Break into sub-problems, solve sequentially (see `advanced-techniques.md`).

---

## Further Reading

- Core: `../SKILL.md`
- Related: `few-shot-prompting.md`, `advanced-techniques.md`
