# Few-Shot Prompting - Deep Dive

Comprehensive guide to few-shot prompting, an In-Context Learning (ICL) technique that provides examples within prompts to guide AI model behavior without additional training.

---

## Overview

**Few-shot prompting** involves embedding 2 or more input-output examples in your prompt to establish a pattern that the AI can follow when processing new inputs.

**Key principle:** By demonstrating desired behavior through examples, you help the model generalize to similar tasks without fine-tuning or additional training.

---

## Comparison: Zero, One, and Few-Shot

| Approach | Examples | Best For | Limitations |
|----------|----------|----------|-------------|
| **Zero-Shot** | 0 | General knowledge tasks, simple questions | May misunderstand task format |
| **One-Shot** | 1 | Clarifying basic format/style | Limited pattern recognition |
| **Few-Shot** | 2-5+ | Pattern matching, formatting, complex tasks | Context window constraints |

---

## How It Works

Few-shot prompting leverages the model's pattern recognition capabilities:

1. **Pattern Establishment**: Multiple examples show the model what "good" looks like
2. **Generalization**: Model infers the underlying rule or pattern
3. **Application**: Model applies learned pattern to new input

This is **In-Context Learning (ICL)** - learning from prompt context rather than parameter updates.

---

## Structure and Formatting

### Format 1: Simple Input-Output (Recommended for Short Examples)

```
Task: Classify the sentiment of product reviews.

Input: "This product exceeded my expectations!"
Output: Positive

Input: "Terrible quality. Broke after one use."
Output: Negative

Input: "It's okay, nothing special."
Output: Neutral

Input: "Best purchase I've made all year!"
Output: ?
```

**Best for:** Classification, labeling, simple transformations

### Format 2: Structured INPUT/OUTPUT (Recommended for Long Content)

```
Extract key information from job postings.

INPUT:
Software Engineer - Remote
TechCorp Inc.
$120k-$150k/year
Required: Python, AWS, 5+ years experience

OUTPUT:
{
  "role": "Software Engineer",
  "company": "TechCorp Inc.",
  "salary_range": "120000-150000",
  "location": "Remote",
  "required_skills": ["Python", "AWS"],
  "experience_years": 5
}

INPUT:
[next job posting]

OUTPUT:
```

**Best for:** Data extraction, long-form content, structured outputs

### Format 3: Conversational Examples

```
You are a customer support chatbot.

Customer: I didn't receive my order yet.
Response: I apologize for the inconvenience. May I have your order number so I can check the status?

Customer: It's been 3 weeks!
Response: I understand your frustration. Let me prioritize this for you. Your order number will help me escalate this immediately.

Customer: My package arrived damaged.
Response: ?
```

**Best for:** Dialogue systems, tone matching, contextual responses

---

## Example Selection Best Practices

### 1. Number of Examples

- **2-3 examples**: Minimum for establishing pattern
- **3-5 examples**: Sweet spot for most tasks
- **5-10 examples**: Complex tasks with edge cases
- **10+ examples**: Diminishing returns, consider fine-tuning instead

**Context window constraint:** More examples = more tokens. Balance accuracy with cost/limits.

### 2. Example Diversity

Include varied examples covering:
- Typical cases (80% of examples)
- Edge cases (10-15%)
- Ambiguous cases (5-10%)

**Example: Sentiment Classification**
```
Good coverage:
- Clear positive: "Absolutely love it!"
- Clear negative: "Worst product ever."
- Neutral: "It's fine."
- Mixed sentiment: "Great quality but overpriced."
- Sarcasm: "Oh wonderful, it broke immediately." → Negative
```

### 3. Example Order

Recent research suggests **order matters**:
- Start with clearest examples
- End with examples most similar to expected input
- Avoid bias by randomizing when testing

### 4. Example Quality

Each example should:
- Be correct and representative
- Match the desired output format exactly
- Use realistic inputs (not toy examples when possible)
- Avoid ambiguity

---

## Advanced Techniques

### Technique 1: Output Format Control

Use examples to enforce specific structures:

```
Convert natural language to SQL queries.

Input: "Show me all users who signed up last week"
Output: SELECT * FROM users WHERE signup_date >= DATE_SUB(NOW(), INTERVAL 7 DAY);

Input: "Count how many orders were placed in January"
Output: SELECT COUNT(*) FROM orders WHERE MONTH(order_date) = 1;

Input: "List products sorted by price, most expensive first"
Output: SELECT * FROM products ORDER BY price DESC;

Input: "Find customers who spent more than $1000"
Output: ?
```

### Technique 2: Multi-Step Reasoning

Show reasoning process in examples:

```
Solve word problems step-by-step.

Problem: Sarah has 12 apples. She gives 3 to John and 2 to Maria. How many does she have left?
Solution:
Step 1: Start with 12 apples
Step 2: Give away 3 to John: 12 - 3 = 9
Step 3: Give away 2 to Maria: 9 - 2 = 7
Answer: 7 apples

Problem: A store sells pencils for $0.50 each. If you buy 10, you get 20% off. How much for 10 pencils?
Solution:
Step 1: Regular price: 10 × $0.50 = $5.00
Step 2: Calculate discount: 20% of $5.00 = $1.00
Step 3: Subtract discount: $5.00 - $1.00 = $4.00
Answer: $4.00

Problem: [your problem]
Solution: ?
```

### Technique 3: Error Correction Examples

Include incorrect→correct patterns:

```
Fix grammar errors in sentences.

Incorrect: "She don't like pizza."
Correct: "She doesn't like pizza."

Incorrect: "There going to the store."
Correct: "They're going to the store."

Incorrect: "I seen that movie yesterday."
Correct: "I saw that movie yesterday."

Incorrect: "Him and me went fishing."
Correct: ?
```

---

## Common Use Cases

### 1. Text Classification

```
Classify these customer inquiries by department:

"I need to reset my password" → Technical Support
"When will my order arrive?" → Shipping
"I want to cancel my subscription" → Billing
"The product doesn't match the description" → Returns
"How do I use feature X?" → ?
```

### 2. Data Extraction

```
Extract entities from news headlines:

"Apple CEO Tim Cook announces new iPhone in California"
→ {"person": "Tim Cook", "organization": "Apple", "product": "iPhone", "location": "California"}

"Tesla opens new factory in Berlin, Germany"
→ {"organization": "Tesla", "facility": "factory", "location": "Berlin, Germany"}

"Microsoft acquires gaming company for $68 billion"
→ ?
```

### 3. Code Generation

```
Generate Python functions from descriptions:

Description: Function that checks if a number is even
Code:
def is_even(n):
    return n % 2 == 0

Description: Function that reverses a string
Code:
def reverse_string(s):
    return s[::-1]

Description: Function that finds the maximum value in a list
Code: ?
```

### 4. Creative Content with Style Matching

```
Write product descriptions in the brand voice:

Product: Organic Coffee Beans
Description: Wake up to sunshine in a cup! Our ethically sourced, hand-picked beans deliver a symphony of flavors that'll make your mornings magical. ☕✨

Product: Noise-Canceling Headphones
Description: Escape into your own world! These premium headphones wrap you in crystal-clear sound while blocking out life's distractions. Pure audio bliss! 🎧🎵

Product: Ergonomic Office Chair
Description: ?
```

---

## Troubleshooting

### Problem: Model Ignores Examples

**Symptoms:** Output doesn't match example format
**Solutions:**
- Add more examples (aim for 4-5)
- Make formatting more explicit/consistent
- Add instruction: "Follow the exact format shown in examples"
- Use stronger delimiters (===, ---, ###)

### Problem: Model Overfits to Examples

**Symptoms:** Only works for inputs very similar to examples
**Solutions:**
- Increase example diversity
- Include edge cases
- Add instruction: "Generalize the pattern to similar inputs"

### Problem: Inconsistent Outputs

**Symptoms:** Same input produces different results
**Solutions:**
- Ensure examples are unambiguous
- Add constraints to instruction
- Lower temperature parameter (if API access available)
- Add "Be consistent" instruction

### Problem: Context Window Exceeded

**Symptoms:** Error or truncated response
**Solutions:**
- Reduce number of examples
- Shorten individual examples
- Use one-shot instead of few-shot
- Consider prompt chaining (break into multiple requests)

---

## Performance Optimization

### Token Efficiency

Each example consumes tokens. Optimize by:
- Using concise examples without sacrificing clarity
- Abbreviating repeated instructions
- Removing unnecessary formatting/whitespace
- Considering one-shot for simple tasks

### Accuracy vs. Cost Trade-off

| Examples | Accuracy Impact | Cost Impact | Recommended When |
|----------|----------------|-------------|-------------------|
| 1-2 | Low | Low | Simple, well-defined tasks |
| 3-5 | Medium-High | Medium | Standard tasks, good balance |
| 6-10 | High | High | Complex tasks, critical accuracy |
| 10+ | Diminishing | Very High | Consider fine-tuning instead |

---

## Further Reading

- Core skill: `../SKILL.md`
- Related: `chain-of-thought.md` (combine few-shot with reasoning)
- Related: `prompt-templates.md` (reusable few-shot templates)
- Related: `evaluation-testing.md` (measuring prompt performance)
