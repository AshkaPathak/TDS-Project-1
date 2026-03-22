# GA6 — Q2: Build a Binary Eval Rubric

## Problem Summary
The task was to design a binary evaluation rubric for grading SQL query quality using an LLM-as-judge system. Instead of vague criteria like "Is the query good?", the goal was to decompose quality into precise YES/NO checks that can be reliably evaluated from the query output alone.

The rubric must:
- Contain exactly 6 binary checks
- Each check must be answerable as YES/NO
- Each check must correlate with quality (GOOD vs POOR)
- Avoid degenerate checks (always YES or always NO)

The evaluation system tests each check on hidden examples and measures correlation with ground truth labels. At least 4 out of 6 checks must pass with correlation > 0.7.

---

## Key Insight
Vague rubrics fail because they rely on subjective interpretation. Binary checks work better when they:
- Capture structural correctness instead of style
- Reflect real query quality signals (aggregation, grouping, filtering)
- Are generalizable across different SQL queries
- Avoid overfitting to specific constants (like fixed dates or thresholds)

The goal is not to perfectly describe the "GOOD" example, but to identify patterns that consistently separate GOOD from POOR queries.

---

## Why Initial Attempts Failed
Earlier checks failed due to:
- Over-specific conditions (e.g., exact date filter)
- Weak signals (e.g., ORDER BY — not always necessary)
- Degenerate checks (always YES or NO)
- Low correlation with actual quality labels

This highlighted an important lesson:
Strong checks must reflect **core analytical structure**, not superficial features.

---

## Final Binary Rubric Checks
The following 6 checks were designed to be:
- General
- Non-degenerate
- Strongly correlated with query quality

Does the query avoid using `SELECT *`?
Does the query compute at least one business metric with an aggregate function such as `SUM`, `COUNT`, `AVG`, `MIN`, or `MAX`?
Does the query group results at the reporting level instead of returning raw row-level records?
Does the query give a clear alias to at least one derived or aggregated column?
Does the query break the logic into at least one named intermediate step using a `WITH` clause or a subquery?
Does the query apply at least one explicit filter with a `WHERE` or `HAVING` clause?

---

## Step-by-Step Reasoning Behind Each Check

### 1. Avoid SELECT *
Using `SELECT *` is a strong indicator of poor query quality because it:
- Returns unnecessary data
- Reduces clarity
- Suggests lack of intent

This reliably distinguishes POOR queries from GOOD ones.

---

### 2. Presence of Aggregation
Analytical SQL queries typically compute metrics such as totals or counts.
The presence of aggregate functions like `SUM` or `COUNT` strongly correlates with meaningful analysis.

---

### 3. Proper Grouping
Grouping ensures that results are summarized at the correct level (e.g., per customer).
Queries without grouping often return raw data instead of insights.

---

### 4. Use of Aliases
Aliasing improves readability and interpretability of results.
It signals that the query is designed for consumption, not just execution.

---

### 5. Structured Logic (CTE/Subquery)
Breaking logic into steps using `WITH` or subqueries indicates:
- Better organization
- Higher complexity handling
- More maintainable queries

This is a strong signal of high-quality SQL.

---

### 6. Presence of Filtering
Good analytical queries usually focus on a subset of data.
Using `WHERE` or `HAVING` demonstrates intent and relevance.

---

## Why This Rubric Works
These checks succeed because they:
- Focus on structure, not formatting
- Capture essential components of analytical SQL
- Generalize across different datasets and tasks
- Avoid dependence on specific constants or values
- Maintain balanced YES/NO distribution (non-degenerate)

At least 4 of these checks achieve high correlation with ground truth, satisfying the evaluation criteria.

---

## Final Answer Submitted
Does the query avoid using `SELECT *`?
Does the query compute at least one business metric with an aggregate function such as `SUM`, `COUNT`, `AVG`, `MIN`, or `MAX`?
Does the query group results at the reporting level instead of returning raw row-level records?
Does the query give a clear alias to at least one derived or aggregated column?
Does the query break the logic into at least one named intermediate step using a `WITH` clause or a subquery?
Does the query apply at least one explicit filter with a `WHERE` or `HAVING` clause?
