# Prompt Templates Library

Reusable prompt templates for common AI tasks. Copy, customize, and deploy.

---

## Content Generation

### Blog Post Template
```
You are an experienced content writer specializing in [domain].

Task: Write a [word count]-word blog post about [topic].
Target audience: [readers]
Tone: [professional/casual/technical]

Requirements:
- Include: [point 1], [point 2], [point 3]
- Use H2/H3 headings every 200-300 words
- [grade level] reading level
- End with call-to-action

Content: [specific information]
```

### Email Template
```
Write a [type] email.
Sender: [role]
Recipient: [role/relationship]
Purpose: [goal]

Key points:
1. [Point 1]
2. [Point 2]

Tone: [formal/friendly]
Length: Under [N] words
```

### Product Description
```
Write product description for [product].

Details:
- Features: [list]
- Target: [customer]
- USP: [what makes it special]

Tone: [brand voice]
Length: [word count]
Focus on benefits, include CTA
```

---

## Data Processing

### Summarization
```
Summarize this [article/document] in [N] sentences.
Focus on: [themes]
Audience: [who]
Format: [paragraph/bullets]
Max: [word count] words

Text: [paste here]
```

### Data Extraction (Few-Shot)
```
Extract structured data as JSON: {key1, key2, key3}

Examples:
Input: "[text 1]" → Output: {json 1}
Input: "[text 2]" → Output: {json 2}

Extract from: "[your text]"
```

### Classification
```
Classify into: [Cat1], [Cat2], [Cat3]

Criteria:
- [Cat1]: [definition]
- [Cat2]: [definition]

Items:
1. [Item 1]
2. [Item 2]
```

---

## Code & Technical

### Code Generation
```
Generate [language] code for: [task]

Requirements:
- Input: [types]
- Output: [expected]
- Handle: [edge cases]
- Style: [conventions]

Example usage: [show]
```

### Code Explanation
```
Explain this [language] code for [beginner/intermediate]:

Focus on:
- What it does
- How it works
- Why this approach

Code:
```[language]
[paste]
```
```

### Debugging (CoT)
```
Debug this code producing [error].

Expected: [behavior]
Actual: [what happens]

Code: [paste]
Error: [message]

Let's debug step by step:
1. Identify issue
2. Explain why
3. Suggest fix
```

---

## Analysis

### Comparison
```
Compare [A] vs [B] on:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Context: [why this matters]
Format: [table/paragraphs]
Conclude with: [recommendation/summary]
```

### Pros/Cons
```
Evaluate [decision] with pros/cons.

Context: [background]
Criteria:
- [Cost]
- [Time]
- [Quality]

Format:
PROS: [list]
CONS: [list]
CONCLUSION: [recommendation]
```

---

## Creative

### Storytelling
```
Write [length] [genre] story.

Setting: [time, place]
Characters: [description]
Conflict: [problem]
Tone: [mood]
Ending: [type]

Length: [word count]
```

### Brainstorming
```
Generate [N] ideas for [project].

Goal: [objective]
Constraints:
- Budget: [range]
- Time: [duration]

For each idea: title, description, key benefit
Range from safe to innovative
```

### Naming
```
Generate [N] names for [product/company].

Industry: [sector]
Values: [attributes]
Tone: [modern/classic/playful]
Length: [one word/phrase]

For each: name, rationale, tagline
```

---

## Universal Template Structure

```
[ROLE - optional]
You are a [role] specializing in [domain].

[TASK]
Task: [clear statement]

[CONTEXT]
- Audience: [who]
- Purpose: [why]
- Background: [info]

[REQUIREMENTS]
- [Req 1]
- [Req 2]

[CONSTRAINTS]
- Length: [count]
- Tone: [style]
- Format: [structure]

[OUTPUT FORMAT]
[How to structure]

[INPUT DATA]
[Content to process]
```

---

## Combining with Techniques

- **Templates + Few-Shot:** Add examples within structure
- **Templates + CoT:** Include "step by step" for complex tasks
- **Templates + Self-Criticism:** Add critique/revision steps
- **Templates + Decomposition:** Break template into sub-tasks

---

## Further Reading

- Core: `../SKILL.md`
- Related: `few-shot-prompting.md`, `advanced-techniques.md`
