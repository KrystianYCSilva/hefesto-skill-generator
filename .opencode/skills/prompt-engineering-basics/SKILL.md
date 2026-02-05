---
name: prompt-engineering-basics
description: |
  Introduction to prompt engineering for working with generative AI models (ChatGPT, Claude, Gemini, etc.).
  Covers core concepts, key techniques (zero-shot, few-shot, chain-of-thought, self-criticism, decomposition, ensembling, thought generation), best practices, and common pitfalls.
  Use when: crafting prompts for LLMs, improving AI outputs, learning AI interaction fundamentals, debugging AI responses.
license: MIT
metadata: ./metadata.yaml
---

# Prompt Engineering Basics

Comprehensive guide to prompt engineering fundamentals for working effectively with generative AI models like ChatGPT, Claude, Gemini, Cohere Chat, and other large language models. Master essential and advanced techniques to maximize AI tool potential in your daily tasks.

---

## When to Use

Use this skill when you need to:

- **Craft effective prompts** for any generative AI model or chatbot
- **Improve AI output quality** through better instruction design
- **Learn prompt engineering fundamentals** as a beginner
- **Apply structured prompting techniques** (zero-shot, few-shot, chain-of-thought, self-criticism, decomposition, ensembling)
- **Debug poor AI responses** by understanding what went wrong
- **Design AI-powered workflows** requiring consistent, high-quality outputs
- **Evaluate prompt performance** across different models

**Not recommended for:** Advanced prompt optimization, model fine-tuning, RAG implementation, or AI safety research (see references).

---

## Instructions

### Step 1: Understand Core Concepts

**What is a Prompt?**
Any input you provide to an AI model to generate a response:
- Question: "What is photosynthesis?"
- Instruction: "Write a haiku about coding"
- Complex request with context, examples, and constraints

**Key AI Limitations:**
- **Hallucinations**: May generate plausible but false information
- **Biases**: Reflects training data biases
- **Knowledge cutoffs**: Limited to training timeframe
- **Context windows**: Limited conversation memory
- **Inconsistency**: Same prompt may yield different results

### Step 2: Master Prompt Components

**1. Context** - Provide background:
```
I'm a software developer working on a React application.
I need to implement user authentication.
```

**2. Task/Instruction** - State what you want:
```
Explain JWT tokens vs session-based authentication,
including pros and cons.
```

**3. Constraints** - Specify limits:
```
Keep under 200 words. Use simple language. Format as table.
```

**4. Examples** - Show patterns (see Few-Shot):
```
Input: "happy" → Output: "positive"
Input: "frustrated" → Output: "negative"
```

### Step 3: Core Techniques

**Zero-Shot Prompting**
Ask without examples. Best for: general knowledge, simple tasks.
```
Classify sentiment: "The product arrived late and damaged."
```

**Few-Shot Prompting**
Provide 2-5 examples to establish pattern. Best for: structured extraction, formatting.
```
Extract product and price:
"iPhone 14 - $999" → {"product": "iPhone 14", "price": 999}
"Galaxy S23 for $1199" → {"product": "Galaxy S23", "price": 1199}
"Pixel 7 only $599!" → ?
```
See `references/few-shot-prompting.md` for details.

**Chain-of-Thought (CoT)**
Guide step-by-step reasoning. Best for: math, logic, debugging.
```
Problem: Train travels 120 km in 2 hours, then 180 km in 1.5 hours.
Average speed for entire journey?

Let's solve step by step:
```
See `references/chain-of-thought.md` for details.

**Role Prompting**
Assign expertise to influence tone and depth.
```
You are an experienced cybersecurity consultant.
Explain zero-trust architecture to a non-technical CEO.
```

### Step 4: Advanced Techniques

**Self-Criticism**
Generate → Critique → Revise for higher quality.
```
Task: Write a function to validate emails.

Step 1: Initial solution
Step 2: Critique for edge cases, errors
Step 3: Revised solution
```
Token cost: ~2-3x. Best for: critical tasks, quality refinement.

**Decomposition**
Break complex problems into sub-problems.
```
Problem: Design scalable URL shortener.

Sub-problem 1: Core functionality?
Sub-problem 2: Generate short URLs how?
Sub-problem 3: Data storage?
Sub-problem 4: Handle high traffic?
Final: Combine solutions
```
Token cost: ~1.5-3x. Best for: complex systems, architecture.

**Ensembling**
Generate multiple solutions, select most consistent.
```
Problem: [Math problem]

Path 1: [Method A] → Answer X
Path 2: [Method B] → Answer X
Path 3: [Method C] → Answer Y

Majority: X (2/3 agree)
Final: X
```
Token cost: ~3-5x. Best for: critical accuracy, verification.

**Thought Generation**
Explore multiple approaches before selecting.
```
Problem: Plan 3-day Paris trip, $500 budget.

Branch A: Culture-focused → Cost $280, Pros/Cons
Branch B: Food-focused → Cost $535, Pros/Cons
Branch C: Balanced → Cost $305, Pros/Cons

Evaluate & select: Branch C (best trade-offs)
```
Token cost: ~3-10x. Best for: planning, strategy, optimization.

See `references/advanced-techniques.md` for comprehensive coverage.

### Step 5: Best Practices

1. **Be specific**: "List 5 health issues in Golden Retrievers" vs "Tell me about dogs"
2. **Use delimiters**: Separate Context / Task / Format clearly
3. **Specify output format**: "As JSON", "As numbered list", "As table"
4. **Iterate**: Start simple, add constraints based on results
5. **Combine techniques**: Few-Shot + CoT, Decomposition + Ensembling

### Step 6: Avoid Pitfalls

- Don't assume perfect knowledge or real-time data
- Don't overload with too many instructions
- Don't ignore context window limits
- Always verify critical information
- Define ambiguous terms ("better" means what?)
- Test for consistency and edge cases
- Reserve advanced techniques for tasks that need them

---

## Examples

**Content Summarization**
```
Role: Executive assistant
Task: Summarize article in 3 bullet points, actionable insights
Article: [text]
Format: Bullets starting with action verbs
```

**Code with Decomposition**
```
Explain this Python function using decomposition:
def fibonacci(n): ...

1. Function purpose?
2. Base cases?
3. Recursive case?
4. Time complexity?
Combine into beginner explanation.
```

**Problem with Self-Criticism**
```
Design API caching strategy.
Step 1: Propose design
Step 2: Critique (bottlenecks? edge cases? invalidation?)
Step 3: Improved design
```

**Decision with Thought Generation**
```
Decision: Migrate to microservices?
Branch 1: Assume 5 devs
Branch 2: Assume 20 devs
Branch 3: Assume tight budget
Evaluate each, recommend based on context.
```

---

## Technique Selection Guide

| Technique | Token Cost | Accuracy | Use When |
|-----------|------------|----------|----------|
| Zero-Shot | Low | Medium | Simple tasks |
| Few-Shot | Medium | High | Pattern matching |
| Chain-of-Thought | Med-High | High | Math, logic |
| Self-Criticism | High (2-3x) | Very High | Quality critical |
| Decomposition | Med-High (1.5-3x) | High | Complex problems |
| Ensembling | Very High (3-5x) | Very High | Accuracy critical |
| Thought Generation | Very High (3-10x) | High | Planning, strategy |

**Strategy:** Start simple → Add CoT if needed → Advanced for critical tasks.

---

## Use Cases by Domain

**Business:** Emails, proposals, marketing copy, meeting summaries, strategy (thought generation)

**Development:** Code explanation, debugging (decomposition), test generation, documentation

**Research:** Paper summaries, theory comparison (ensembling), concept explanation (decomposition)

**Education:** Lesson plans, practice problems, explanations, feedback (self-criticism)

**Personal:** Trip planning (thought generation), correspondence, learning, brainstorming

---

## Advanced Topics

Explore references directory for deep dives:

- `few-shot-prompting.md` - Pattern learning techniques
- `chain-of-thought.md` - Reasoning and decomposition
- `advanced-techniques.md` - Self-criticism, ensembling, thought generation, decomposition
- `prompt-templates.md` - Reusable templates
- `model-specific-tips.md` - Optimize for ChatGPT, Claude, Gemini
- `evaluation-testing.md` - Measure and improve performance

---

## Quick Reference

| Technique | Trigger | Example |
|-----------|---------|---------|
| Instruction | Direct | "Translate...", "List..." |
| Role | "You are..." | "You are an expert..." |
| Zero-Shot | Question | "What is...?" |
| Few-Shot | Examples | Input→Output, Input→Output, Input→? |
| CoT | "Step by step:" | "Let's solve step by step:" |
| Self-Criticism | "Generate, critique, revise" | Step 1/2/3 pattern |
| Decomposition | "Sub-problems" | Sub-problem 1, 2, 3... |
| Ensembling | "Multiple paths" | Path 1/2/3, select best |
| Thought Gen | "Multiple branches" | Branch A/B/C, evaluate |

---

## Troubleshooting

**Vague responses** → Add constraints, use role prompting, provide examples

**Hallucinations** → Use CoT reasoning, self-criticism, ensembling for verification

**Inconsistent format** → Few-shot with examples, explicit structure specification

**Refusals** → Rephrase to clarify legitimate use, check safety filter triggers

**Too long/short** → Specify exact word/sentence count

**Not optimal** → Use thought generation (explore alternatives), decomposition (tackle complexity)

**Too complex** → Decompose into sub-problems, solve independently, combine

---

## Combining Techniques

Powerful combinations:
- **Few-Shot + CoT**: Examples with reasoning
- **Decomposition + Ensembling**: Solve sub-problems multiple ways
- **Self-Criticism + Thought Generation**: Critique each branch
- **All Advanced (critical tasks)**: Decompose → Thought Gen each sub-problem → Ensemble solutions → Self-Criticize final

**Warning:** Advanced combos can cost 20-50x tokens. Reserve for genuinely critical tasks.

---

## Resources

**Primary source:** Learn Prompting (https://learnprompting.org)

**Complete citations:** See `metadata.yaml`

**Deep dives:** See `references/` directory (6 detailed guides)

---

## Performance Notes

- Longer prompts = higher cost + time
- CoT: ~2x tokens
- Self-Criticism: ~2-3x tokens
- Decomposition: ~1.5-3x tokens
- Ensembling: ~3-5x tokens
- Thought Generation: ~3-10x tokens
- Advanced combos: ~20-50x tokens

Use advanced techniques strategically where quality justifies cost.
