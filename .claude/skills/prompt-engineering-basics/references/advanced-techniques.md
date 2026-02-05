# Advanced Prompting Techniques

Deep dive into sophisticated prompt engineering methods: Self-Criticism, Decomposition, Ensembling, and Thought Generation. These techniques significantly improve AI output quality for complex tasks.

---

## Overview

While basic techniques (zero-shot, few-shot, chain-of-thought) handle many use cases, advanced techniques unlock higher accuracy, reliability, and creativity for demanding applications.

**Trade-off:** Advanced techniques increase token usage (2-10x) and cost but provide substantial quality gains for critical tasks.

---

## Self-Criticism Prompting

### Concept

Instruct the AI to generate an initial response, critique it, and then produce an improved version based on the critique. This meta-cognitive approach catches errors and refines quality.

**Core pattern:**
1. Generate → 2. Critique → 3. Revise

### Why It Works

- **Error detection**: AI identifies flaws in its own reasoning
- **Quality refinement**: Iterative improvement mimics human editing
- **Reduced hallucinations**: Critique step catches inconsistencies
- **Transparency**: Exposes assumptions and reasoning

### Implementation

**Pattern 1: Two-Step Critique**

```
Task: [Your task]

Step 1: Provide an initial solution.
Step 2: Critique your solution by identifying weaknesses, errors, or improvements.
Step 3: Provide a revised solution addressing the critique.
```

**Example:**

```
Task: Write a Python function to check if a string is a valid email address.

Step 1: Initial solution:
def is_valid_email(email):
    return '@' in email and '.' in email

Step 2: Critique:
- Too simplistic - doesn't check position of @ and .
- Allows multiple @ symbols
- Doesn't validate domain structure
- No check for valid characters
- Edge cases: empty string, spaces

Step 3: Revised solution:
import re

def is_valid_email(email):
    """
    Validates email format using regex.
    Returns True if valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**Pattern 2: Aspect-Based Critique**

```
Task: [Your task]

Generate an initial response.

Then critique your response for:
- Accuracy: Are all facts correct?
- Completeness: Did you address all parts?
- Clarity: Is it easy to understand?
- Edge cases: What scenarios might break it?
- [Add domain-specific criteria]

Finally, provide an improved version.
```

**Pattern 3: Socratic Self-Questioning**

```
Task: [Your task]

Provide a solution, then ask yourself:
1. What assumptions did I make?
2. What evidence supports my approach?
3. What alternative approaches exist?
4. What are the limitations of my solution?
5. How could someone prove this wrong?

Based on these questions, refine your solution.
```

### Use Cases

**Software Development:**
```
Write a function to [task].

Step 1: Implement
Step 2: Review for:
  - Time/space complexity
  - Edge cases (null, empty, large inputs)
  - Error handling
  - Code clarity
Step 3: Refactor based on review
```

**Content Writing:**
```
Write a blog introduction about [topic].

Step 1: Draft introduction
Step 2: Critique for:
  - Hook effectiveness
  - Clarity of thesis
  - Grammar and style
  - Target audience fit
Step 3: Revised version
```

**Research and Analysis:**
```
Analyze [data/argument].

Step 1: Initial analysis
Step 2: Identify:
  - Potential biases in reasoning
  - Missing data or context
  - Alternative interpretations
  - Confidence level in conclusions
Step 3: Refined analysis
```

### Best Practices

1. **Be specific in critique criteria**: Don't just say "critique it" - specify what to look for
2. **Use domain expertise**: Leverage role prompting: "As an expert, critique..."
3. **Iterate multiple times**: For critical tasks, do 2-3 critique cycles
4. **Combine with examples**: Show example critiques in few-shot format
5. **Set high standards**: "Be ruthlessly critical" or "Assume this is for production"

### Limitations

- **Token intensive**: ~2-3x tokens compared to single-pass generation
- **May over-correct**: Sometimes introduces new errors while fixing old ones
- **Not always needed**: Overkill for simple tasks
- **Model dependent**: Works best with large, capable models (GPT-4, Claude Opus)

---

## Decomposition (Least-to-Most Prompting)

### Concept

Break complex problems into a sequence of simpler sub-problems. Solve each sub-problem independently, then compose solutions into a complete answer.

**Core pattern:**
Sub-problem 1 → Solution 1 → Sub-problem 2 → Solution 2 → ... → Final composition

### Why It Works

- **Reduces cognitive load**: Focuses AI on one aspect at a time
- **Improves accuracy**: Simpler sub-problems → fewer errors
- **Builds incrementally**: Later sub-problems can use earlier solutions
- **Transparent reasoning**: Shows problem-solving process

### Implementation

**Pattern 1: Sequential Decomposition**

```
Problem: [Complex problem]

Let's break this down into sub-problems:

Sub-problem 1: [Simplest foundational question]
Solution 1: [Answer]

Sub-problem 2: [Next question, builds on Solution 1]
Solution 2: [Answer]

Sub-problem 3: [Continues building]
Solution 3: [Answer]

...

Final solution: [Combine all sub-solutions]
```

**Example: System Design**

```
Problem: Design a scalable URL shortener service.

Sub-problem 1: What core functionality does a URL shortener need?
Solution 1:
- Generate short URL from long URL
- Redirect short URL to long URL
- Track click analytics

Sub-problem 2: How do we generate short URLs?
Solution 2:
- Use base62 encoding (a-z, A-Z, 0-9)
- Generate from auto-incrementing ID or hash
- 7 characters = 62^7 = 3.5 trillion URLs

Sub-problem 3: What data storage is appropriate?
Solution 3:
- NoSQL (e.g., Cassandra, DynamoDB) for scalability
- Schema: {short_code: string, long_url: string, created_at: timestamp, clicks: int}
- Cache frequent URLs in Redis

Sub-problem 4: How do we handle high read traffic?
Solution 4:
- CDN for global distribution
- Read replicas for database
- Cache layer (Redis) for hot URLs
- Load balancer distributing requests

Sub-problem 5: How do we prevent collisions and handle security?
Solution 5:
- Check uniqueness before inserting
- Rate limiting to prevent abuse
- Validate URLs before shortening
- Expiration policies for old URLs

Final design: [Synthesize all components into architecture diagram + explanation]
```

**Pattern 2: Dependency-Driven Decomposition**

```
Problem: [Complex problem]

Step 1: Identify all sub-problems needed to solve this.
Step 2: Order sub-problems by dependencies (what must be solved first).
Step 3: Solve each sub-problem in order.
Step 4: Integrate solutions.
```

**Pattern 3: Divide-and-Conquer**

```
Problem: [Large problem]

Divide:
- Part A: [Subset of problem]
- Part B: [Another subset]
- Part C: [Remaining subset]

Conquer each part:
- Solution A: [...]
- Solution B: [...]
- Solution C: [...]

Combine:
[Merge solutions A + B + C into complete solution]
```

### Use Cases

**Algorithm Design:**
```
Design an algorithm to [complex task].

Sub-problem 1: What data structures are needed?
Sub-problem 2: How do we handle the core operation?
Sub-problem 3: What edge cases exist?
Sub-problem 4: How do we optimize time complexity?
Sub-problem 5: Combine into complete algorithm.
```

**Business Strategy:**
```
Develop a go-to-market strategy for [product].

Sub-problem 1: Who is the target customer?
Sub-problem 2: What is the value proposition?
Sub-problem 3: What channels reach this customer?
Sub-problem 4: What is the pricing strategy?
Sub-problem 5: What are key success metrics?
Final: Integrated GTM plan
```

**Learning Complex Topics:**
```
Explain quantum entanglement.

Sub-problem 1: What is a quantum state?
Sub-problem 2: What is superposition?
Sub-problem 3: What happens when particles interact?
Sub-problem 4: What is measurement in quantum mechanics?
Sub-problem 5: How does entanglement emerge from these concepts?
Final: Complete explanation
```

### Best Practices

1. **Start with high-level decomposition**: Identify major sub-problems first
2. **Make sub-problems independent when possible**: Parallelizable if needed
3. **Order by dependency**: Solve prerequisites first
4. **Validate each sub-solution**: Before moving to next
5. **Show connections**: Explicitly state how sub-solutions relate

### Limitations

- **Can be verbose**: Many sub-problems = long output
- **May over-decompose**: Sometimes creates unnecessary complexity
- **Requires good problem structure**: Not all problems decompose neatly
- **Trade-off with holistic thinking**: Might miss interactions between parts

---

## Ensembling (Self-Consistency)

### Concept

Generate multiple independent solutions to the same problem using different reasoning paths, then select the most consistent or best answer through voting or analysis.

**Core pattern:**
Generate N solutions → Compare/vote → Select best

### Why It Works

- **Error averaging**: Random errors in individual paths cancel out
- **Robustness**: Less sensitive to single reasoning failures
- **Confidence estimation**: Agreement level indicates reliability
- **Catches hallucinations**: Inconsistent "facts" across paths are suspicious

### Implementation

**Pattern 1: Multi-Path Reasoning with Voting**

```
Problem: [Problem statement]

Generate 3 independent reasoning paths:

Path 1: [Approach using method A]
→ Answer: [Result 1]

Path 2: [Approach using method B]
→ Answer: [Result 2]

Path 3: [Approach using method C]
→ Answer: [Result 3]

Compare answers:
- Path 1 says: [Result 1]
- Path 2 says: [Result 2]
- Path 3 says: [Result 3]

Majority vote: [Most common answer]
Confidence: [High if 3/3 agree, Medium if 2/3, Low if all differ]

Final answer: [Selected answer with justification]
```

**Example: Math Problem**

```
Problem: A store offers 25% off, then an additional 10% off the sale price.
What's the final price of a $100 item?

Path 1 (Sequential discount):
- First discount: $100 × 0.25 = $25 off → $75
- Second discount: $75 × 0.10 = $7.50 off → $67.50
Answer: $67.50

Path 2 (Combined multipliers):
- Keep 75% after first discount
- Keep 90% after second discount
- Final: $100 × 0.75 × 0.90 = $67.50
Answer: $67.50

Path 3 (Working backwards):
- Total discount ≠ 35% (common mistake)
- Actual: 1 - (0.75 × 0.90) = 1 - 0.675 = 0.325 = 32.5% off
- Final: $100 × 0.675 = $67.50
Answer: $67.50

Majority: All 3 paths agree on $67.50
Confidence: HIGH
Final answer: $67.50
```

**Pattern 2: Diverse Perspective Ensembling**

```
Problem: [Problem requiring judgment]

Generate solutions from different perspectives:

Perspective 1 (Role: [Expert A]):
[Solution from viewpoint A]

Perspective 2 (Role: [Expert B]):
[Solution from viewpoint B]

Perspective 3 (Role: [Expert C]):
[Solution from viewpoint C]

Synthesize:
- Common ground: [What all perspectives agree on]
- Conflicts: [Where perspectives differ]
- Best approach: [Reasoned selection or hybrid]
```

**Pattern 3: Temperature-Based Ensembling (API only)**

```python
# Generate multiple outputs with temperature > 0
responses = []
for i in range(5):
    response = ai_model.generate(
        prompt="[Your prompt]",
        temperature=0.7  # Introduces variation
    )
    responses.append(response)

# Select most common answer or highest quality
final_answer = select_best(responses)
```

**Pattern 4: Self-Consistency CoT**

Combine ensembling with chain-of-thought:

```
Problem: [Problem]

Generate 3 chain-of-thought solutions:

Solution 1:
Step 1: [...]
Step 2: [...]
Step 3: [...]
Answer: X

Solution 2:
Step 1: [...]
Step 2: [...]
Step 3: [...]
Answer: Y

Solution 3:
Step 1: [...]
Step 2: [...]
Step 3: [...]
Answer: X

Majority vote: X (appears 2/3 times)
Verify reasoning: [Check which reasoning is more sound]
Final: X
```

### Use Cases

**Critical Decisions:**
```
Decision: Should we invest in [opportunity]?

Analysis 1 (Financial perspective): [...]
Analysis 2 (Risk perspective): [...]
Analysis 3 (Strategic perspective): [...]

Recommendation: [Based on consensus or synthesis]
```

**Fact Verification:**
```
Claim: [Factual claim to verify]

Verification 1 (Source-based): [...]
Verification 2 (Logical consistency): [...]
Verification 3 (Historical context): [...]

Confidence in claim: [Based on agreement across methods]
```

**Complex Calculations:**
```
Problem: [Math/logic problem]

Method 1: [Algebraic approach] → Answer: X
Method 2: [Numerical approach] → Answer: X
Method 3: [Geometric approach] → Answer: Y

Analysis: Methods 1&2 agree. Method 3 has error in [specific step].
Final: X
```

### Best Practices

1. **Use truly different approaches**: Not just rephrasing same method
2. **Aim for 3-5 paths**: More isn't always better (diminishing returns)
3. **Analyze disagreements**: When paths differ, investigate why
4. **Weight by reasoning quality**: Not just majority vote
5. **Combine with other techniques**: Ensembling + CoT, Ensembling + Self-Criticism

### Limitations

- **Very token intensive**: 3-5x tokens compared to single solution
- **Expensive**: High API costs for production use
- **Slower**: Multiple generations take time
- **Requires analysis**: Selecting "best" answer may need judgment
- **May converge on wrong answer**: If all paths share same misconception

---

## Thought Generation (Tree of Thoughts)

### Concept

Generate multiple reasoning branches exploring different solution approaches, evaluate each branch, and select or synthesize the optimal path. Unlike linear chain-of-thought, this explores the solution space tree-like.

**Core pattern:**
Generate branches → Evaluate branches → Select/combine best

### Why It Works

- **Explores alternatives**: Considers multiple strategies before committing
- **Evaluates trade-offs**: Compares approaches systematically
- **Creativity**: Generates novel solutions by exploring diverse paths
- **Robust decisions**: Less likely to miss better alternatives

### Implementation

**Pattern 1: Generate-Evaluate-Select**

```
Problem: [Problem statement]

Phase 1 - Generate Thought Branches:

Branch A: [Approach A]
  - Key idea: [...]
  - Steps: [...]
  - Predicted outcome: [...]

Branch B: [Approach B]
  - Key idea: [...]
  - Steps: [...]
  - Predicted outcome: [...]

Branch C: [Approach C]
  - Key idea: [...]
  - Steps: [...]
  - Predicted outcome: [...]

Phase 2 - Evaluate Each Branch:

Branch A:
  - Pros: [...]
  - Cons: [...]
  - Feasibility: [1-10]
  - Expected quality: [1-10]

Branch B:
  - Pros: [...]
  - Cons: [...]
  - Feasibility: [1-10]
  - Expected quality: [1-10]

Branch C:
  - Pros: [...]
  - Cons: [...]
  - Feasibility: [1-10]
  - Expected quality: [1-10]

Phase 3 - Select or Synthesize:

Selected approach: [Best branch or hybrid of multiple branches]
Justification: [Why this is optimal given constraints]
```

**Example: Trip Planning**

```
Problem: Plan a 3-day trip to Tokyo with $800 budget.

Branch A: Culture-focused itinerary
Day 1: Senso-ji Temple, Meiji Shrine, Harajuku (free/low-cost)
Day 2: Imperial Palace, Ueno Park museums ($20)
Day 3: Day trip to Nikko ($50 transport + $30 entry)
Accommodation: Hostel ($30/night × 3 = $90)
Food: Budget meals ($30/day × 3 = $90)
Total: ~$280
Pros: Rich cultural experience, under budget
Cons: Less modern Tokyo, lots of walking

Branch B: Food & entertainment focus
Day 1: Tsukiji fish market, Shibuya, karaoke
Day 2: Ramen tour, Akihabara, gaming cafes
Day 3: Cooking class ($80), teamLab Borderless ($35)
Accommodation: Mid-range hotel ($80/night × 3 = $240)
Food: Mid-range restaurants ($60/day × 3 = $180)
Total: ~$535
Pros: Memorable food experiences, entertainment variety
Cons: Less cultural depth, higher cost

Branch C: Balanced approach
Day 1: Mix of temple (free) + Shibuya crossing + local ramen
Day 2: Imperial Palace + Akihabara + budget izakaya
Day 3: Morning at Meiji Shrine + afternoon in Harajuku + evening in Shinjuku
Accommodation: Capsule hotel ($45/night × 3 = $135)
Food: Mix of budget and splurge ($40/day × 3 = $120)
Activities: $50 for one special experience
Total: ~$305
Pros: Diverse experiences, good budget balance
Cons: May feel rushed, no deep focus

Evaluation:
Branch A: Feasibility 9/10, Cultural depth 10/10, Entertainment 5/10
Branch B: Feasibility 8/10, Cultural depth 5/10, Entertainment 10/10
Branch C: Feasibility 9/10, Cultural depth 7/10, Entertainment 7/10

Selected: Branch C (balanced)
Justification: Best overall experience within budget, diversified risk,
appeals to multiple interests, leaves buffer for unexpected costs.
```

**Pattern 2: Iterative Depth Exploration**

```
Problem: [Problem]

Level 1 - High-level approaches:
  - Option 1: [...]
  - Option 2: [...]
  - Option 3: [...]

Evaluate: [Quick assessment] → Most promising: Option 2

Level 2 - Expand Option 2:
  - Sub-option 2.1: [...]
  - Sub-option 2.2: [...]
  - Sub-option 2.3: [...]

Evaluate: [Detailed assessment] → Best: Sub-option 2.2

Level 3 - Detail Sub-option 2.2:
  [Fully specified solution]
```

**Pattern 3: Constraint-Based Branching**

```
Problem: [Problem with multiple constraints]

Generate branches assuming different constraint priorities:

Branch A: Optimize for [constraint 1]
  [Solution optimizing constraint 1]
  Constraint 1 score: [high]
  Constraint 2 score: [low]
  Constraint 3 score: [medium]

Branch B: Optimize for [constraint 2]
  [Solution optimizing constraint 2]
  Constraint 1 score: [medium]
  Constraint 2 score: [high]
  Constraint 3 score: [low]

Branch C: Balanced across all constraints
  [Solution balancing trade-offs]
  Constraint 1 score: [medium]
  Constraint 2 score: [medium]
  Constraint 3 score: [medium]

Given actual priorities [specify], select: [Best match]
```

### Use Cases

**Strategic Planning:**
```
Strategy: Grow SaaS business to $10M ARR.

Branch A: Focus on enterprise
Branch B: Focus on SMB volume
Branch C: Hybrid (mid-market)

Evaluate on: Revenue potential, CAC, sales cycle, churn, resources needed
Select: [Optimal strategy]
```

**Architecture Decisions:**
```
Decision: Choose database for new application.

Branch A: Relational (PostgreSQL)
  - Pros/cons for our use case
  - Performance projections
  - Team expertise

Branch B: Document (MongoDB)
  - Pros/cons for our use case
  - Performance projections
  - Team expertise

Branch C: Hybrid (Postgres + Redis)
  - Pros/cons for our use case
  - Performance projections
  - Team expertise

Evaluate: [Based on requirements] → Select best
```

**Creative Work:**
```
Task: Design logo for [company].

Concept A: [Minimalist approach]
  - Mockup: [Description]
  - Strengths: [...]
  - Weaknesses: [...]

Concept B: [Bold/colorful approach]
  - Mockup: [Description]
  - Strengths: [...]
  - Weaknesses: [...]

Concept C: [Symbolic approach]
  - Mockup: [Description]
  - Strengths: [...]
  - Weaknesses: [...]

Recommendation: [Best concept or hybrid]
```

### Best Practices

1. **Generate diverse branches**: Ensure meaningful differences between options
2. **Use clear evaluation criteria**: Define what "better" means upfront
3. **Consider constraints**: Budget, time, resources, priorities
4. **Prune poor branches**: Don't explore every path to completion
5. **Synthesize when appropriate**: Best solution may combine elements
6. **Iterate depth**: Start broad, dive deep into promising branches

### Limitations

- **Extremely token intensive**: 3-10x tokens depending on branch depth
- **Requires structured thinking**: AI must organize thoughts coherently
- **Complexity**: Can become unwieldy with too many branches
- **May over-analyze**: Not needed for simple decisions
- **Best for open-ended problems**: Less useful for problems with clear optimal solution

---

## Combining Advanced Techniques

### Decomposition + Ensembling

```
Problem: [Complex problem]

Decompose:
  Sub-problem 1: [...]
  Sub-problem 2: [...]

For each sub-problem, use ensembling:

Sub-problem 1:
  Path 1: [Solution A]
  Path 2: [Solution B]
  Path 3: [Solution C]
  Best: [Selected solution]

Sub-problem 2:
  Path 1: [Solution A]
  Path 2: [Solution B]
  Path 3: [Solution C]
  Best: [Selected solution]

Final: Combine best sub-solutions
```

### Self-Criticism + Thought Generation

```
Problem: [Problem]

Phase 1 - Generate thought branches:
  Branch A: [...]
  Branch B: [...]
  Branch C: [...]

Phase 2 - Self-critique each branch:
  Branch A critique: [Identify flaws]
  Branch B critique: [Identify flaws]
  Branch C critique: [Identify flaws]

Phase 3 - Select best OR create improved hybrid:
  Selected/Hybrid approach: [Best based on critiques]
```

### All Four Combined (Maximum Quality)

```
Problem: [Critical problem requiring highest accuracy]

Step 1 - Decompose:
  [Break into sub-problems]

Step 2 - For each sub-problem:

  2a. Generate thought branches (3 approaches)
  2b. Self-critique each branch
  2c. Select best branch
  2d. Ensemble: Solve best branch with 3 reasoning paths
  2e. Final sub-solution: Most consistent + critiqued

Step 3 - Integrate all sub-solutions

Step 4 - Final self-criticism of complete solution

Step 5 - Deliver refined final answer
```

**Warning:** This is overkill for most tasks. Token usage can be 20-50x single-pass prompting. Reserve for genuinely critical decisions.

---

## Quick Comparison Table

| Technique | Token Multiplier | Accuracy Gain | Best For | Avoid When |
|-----------|------------------|---------------|----------|------------|
| **Self-Criticism** | 2-3x | Medium-High | Quality refinement | Simple tasks |
| **Decomposition** | 1.5-3x | High | Complex problems | Holistic tasks |
| **Ensembling** | 3-5x | Very High | Critical accuracy | Cost-sensitive |
| **Thought Generation** | 3-10x | Medium-High | Strategy, planning | Clear solutions exist |

---

## When to Use Which Technique

**Decision Tree:**

1. **Is the task simple and well-defined?**
   - Yes → Use basic techniques (zero-shot, few-shot, CoT)
   - No → Continue

2. **Is there one clear solution approach?**
   - Yes → Use Decomposition (if complex) or Self-Criticism (if quality matters)
   - No → Use Thought Generation to explore approaches

3. **Is accuracy critical (e.g., medical, legal, financial)?**
   - Yes → Use Ensembling for verification
   - No → Continue

4. **Is this going into production?**
   - Yes → Use Self-Criticism for quality assurance
   - No → Basic techniques may suffice

5. **What's the budget?**
   - High → Combine techniques for maximum quality
   - Low → Use simpler techniques

---

## Further Reading

- Core skill: `../SKILL.md`
- Related: `chain-of-thought.md` (foundation for these techniques)
- Related: `few-shot-prompting.md` (can be combined with advanced techniques)
- Related: `evaluation-testing.md` (measure effectiveness of advanced techniques)

---

## References

- Wei et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Wang et al. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
- Zhou et al. (2022). "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models"
- Yao et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
- Madaan et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback"
