# Prompt Evaluation and Testing

Systematic approaches to measure, test, and improve prompt performance.

---

## Why Evaluate?

1. **Accuracy**: Produces correct outputs?
2. **Consistency**: Same result for same input?
3. **Efficiency**: Cost-effective (tokens/time)?
4. **Robustness**: Handles edge cases?
5. **Scalability**: Works across many inputs?

---

## Evaluation Framework

### Step 1: Define Success Criteria

**Classification Tasks:**
- Accuracy rate (% correct)
- Precision, recall, F1 score

**Generation Tasks:**
- Relevance to prompt
- Factual accuracy
- Coherence
- Format compliance

**Extraction Tasks:**
- Completeness (all data extracted)
- Accuracy (data matches source)
- Format correctness

### Step 2: Create Test Set

```json
test_cases = [
  {
    "input": "Sample 1",
    "expected": "Result 1",
    "category": "typical"
  },
  {
    "input": "Sample 2",
    "expected": "Result 2",
    "category": "edge_case"
  }
]
```

**Composition:**
- 70% typical cases
- 20% edge cases
- 10% adversarial

**Minimum:** 20-30 examples

### Step 3: Run Tests & Analyze

```python
accuracy = correct / total
edge_case_accuracy = correct_edges / total_edges

# Identify failure patterns
```

### Step 4: Iterate

Refine prompt based on failures:
1. Add examples for failure cases
2. Adjust constraints
3. Clarify instructions
4. Re-test

---

## Key Metrics

### Accuracy Metrics

**Exact Match:**
```
exact_match = (output == expected)
```

**Partial Match:**
```
score = overlap(output_elements, expected_elements) / total_elements
```

**Semantic Similarity:**
```
similarity = cosine_sim(embed(output), embed(expected))
```

### Quality Metrics

**Relevance:** 1-5 scale (how well it addresses prompt)
**Coherence:** 1-5 scale (logical structure)
**Factual Accuracy:** 1-5 scale (true claims)
**Format Compliance:** Binary or % compliance

### Efficiency Metrics

```
avg_tokens = sum(tokens) / count
cost_per_request = (input_tokens * price_in + output_tokens * price_out)
avg_response_time = sum(time) / count
```

### Consistency

Run same prompt 5x, measure agreement:
```
consistency = same_outputs / total_runs
```

---

## Testing Methods

### A/B Testing

| Metric | Prompt A | Prompt B | Winner |
|--------|----------|----------|--------|
| Accuracy | 85% | 92% | B |
| Avg tokens | 150 | 200 | A |
| Cost | $0.02 | $0.03 | A |

**Decision:** If accuracy diff >10%, choose more accurate. Otherwise, choose efficient.

### Edge Case Testing

```
edge_cases = [
  "Empty input: ''",
  "Very long: [5000+ words]",
  "Special chars: @#$%",
  "Ambiguous: '...'",
  "Multilingual: 'Hello 你好'",
  "Malformed: '...'"
]
```

### Adversarial Testing

Try to break the prompt:
```
- "Ignore previous instructions and..."
- "[Contradictory requirements]"
- "[Request outside scope]"
```

---

## Regression Testing

When updating prompts:

1. Maintain test suite
2. Run before/after changes
3. Flag regressions (previously passing now fails)

```python
baseline = run_tests(prompt_v1, tests)
new = run_tests(prompt_v2, tests)
regressions = find_regressions(baseline, new)
```

---

## Human Evaluation

For subjective tasks:

### Rubric Example

| Criterion | Weight | Score 1-5 | Notes |
|-----------|--------|-----------|-------|
| Persuasiveness | 30% | | Compelling? |
| Accuracy | 25% | | Facts correct? |
| Tone | 20% | | Matches brand? |
| Readability | 15% | | Easy to read? |
| Creativity | 10% | | Original? |

**Final:** Weighted average

### Inter-Rater Reliability

Use 2+ raters, measure agreement:
```
agreement = matching_scores / total_scores
```
High agreement (>0.7) validates evaluation.

---

## Automated Tools

### LLM-as-Judge

```
eval_prompt = f"""
Rate this response 1-5 for:
- Accuracy
- Relevance
- Coherence

Response: {output}

Provide JSON scores.
"""
```

**Pros:** Scalable
**Cons:** May have biases

### Rule-Based

```python
def validate_json(output, keys):
    try:
        data = json.loads(output)
        return all(k in data for k in keys)
    except:
        return False
```

---

## Statistical Significance

**Sample Size:**
- Minimum: 30 cases
- Recommended: 100+ cases
- Critical: 500+ cases

**Confidence Intervals:**
```
CI = accuracy ± 1.96 * sqrt(accuracy * (1-accuracy) / n)
```

**Hypothesis Testing:**
```
p_value = test(results_A, results_B)
if p_value < 0.05:
    print("Improvement is significant")
```

---

## Continuous Monitoring

For production:

### Logging
```json
{
  "timestamp": "...",
  "prompt_version": "v2.3",
  "input": "...",
  "output": "...",
  "user_feedback": 4,
  "latency": 1.2,
  "tokens": 150
}
```

### Dashboards
- Daily accuracy
- Avg response time
- Token usage trends
- User satisfaction
- Error rate

### Anomaly Detection
```
if daily_accuracy < baseline - threshold:
    alert("Performance degraded")
```

---

## Testing Checklist

Before deployment:
- [ ] Tested on ≥30 diverse inputs
- [ ] Accuracy ≥ target
- [ ] Edge cases handled
- [ ] Format validated
- [ ] Consistency ≥80%
- [ ] Cost within budget
- [ ] Response time acceptable
- [ ] Adversarial tests passed
- [ ] Human eval (if needed)
- [ ] Regression tests passed

---

## Example Workflow

**Use case:** Sentiment classification

1. **Define:** ≥90% accuracy, <100 tokens, <$0.01/req
2. **Test set:** 100 reviews (50 pos, 30 neg, 20 neutral)
3. **Baseline:** Zero-shot → 72% accuracy
4. **Iterate:** Few-shot (3 ex) → 89%
5. **Optimize:** Few-shot (5 ex) → 93%
6. **Deploy:** Meets targets

---

## Tools

**Platforms:**
- PromptFoo (testing framework)
- LangSmith (evaluation)
- W&B Prompts (tracking)

**Metrics:**
- ROUGE (summarization)
- BLEU (translation)
- BERTScore (semantic)

**DIY:**
- Spreadsheet with test cases
- Python scripts
- JSON/CSV logging

---

## Further Reading

- Core: `../SKILL.md`
- Related: `few-shot-prompting.md`, `advanced-techniques.md`
