# GA1 — Q10: Network Game — Graph Detective

## Problem Summary

In this task, we interact with an online **transaction graph game** where:

- Each node represents an account
- Edges represent transaction relationships
- We have a **limited query budget (55 queries)**
- Goal:
  - Identify the **compromised node**
  - Provide the **shortest proof path** from the anchor node

The system validates:
- Correct compromised node
- Valid shortest path
- JWT token returned after successful submission

---

## Game Understanding

### Initial Setup

- Anchor node: **11**
- Query budget: **55**
- Nodes are hidden initially (grey)
- Clicking a node reveals:
  - Degree
  - Neighbors
  - Transaction statistics

---

## Clues Interpretation

Given clues:

1. Only a handful of counterparties are involved, yet volumes are extraordinary  
2. Transactions are rare but individually massive  
3. The account moves enormous sums but almost never receives  

---

### Translating Clues → Metrics

| Clue | Metric |
|------|--------|
| Few counterparties | `counterparty_count LOW` |
| Rare transactions | `tx_count_daily LOW` |
| Huge volume | `tx_volume_daily HIGH` |
| Mostly outgoing | `in_out_ratio VERY LOW` |

---

## Exploration Strategy

### Step 1 — Start from Anchor Node

Queried node **11**:
- High degree (hub node)
- Balanced transactions
- Not suspicious

---

### Step 2 — Expand Neighbors

Explored multiple neighbors:
- 51
- 98
- 32
- 63
- 76
- 46
- etc.

Observation:
- Most nodes were:
  - High degree
  - Balanced in/out ratios
  - Moderate transaction counts

Conclusion:
👉 These are **normal nodes in dense cluster**

---

### Step 3 — Key Insight

Compromised node is likely:

- NOT a hub
- NOT central
- NOT highly connected

👉 Instead:
- Low connectivity
- Extreme behavior

---

### Step 4 — Move to Sparse / Outer Nodes

Shifted exploration to nodes away from cluster.

---

## Final Discovery

### Node 112

```
id: 112
degree: 3
neighbors: 7, 41, 103
tx_volume_daily: 30800
tx_count_daily: 3
in_out_ratio: 0.03
counterparty_count: 4
```

---

## Why Node 112 is Correct

| Metric | Value | Matches Clue |
|------|------|-------------|
| counterparty_count | 4 | ✅ few |
| tx_count_daily | 3 | ✅ rare |
| tx_volume_daily | 30800 | ✅ huge |
| in_out_ratio | 0.03 | ✅ mostly outgoing |

👉 Perfect match with all clues

---

## Shortest Proof Path

We verify connections:

- Node 112 neighbors → **7, 41, 103**
- Node 11 neighbors include → **7**

Thus:

```
11 → 7 → 112
```

---

### Final Path

```
11,7,112
```

- Valid edges
- Minimal hops
- Shortest path

---

## Final Submission

### Compromised Node
```
112
```

### Path
```
11,7,112
```

---

## Token Extraction

After clicking **Submit** in the game:

1. Open DevTools → Network tab
2. Locate final API response
3. Copy:
```
completion_token
```

---

## Final Result

- ✔ Correct node identified
- ✔ Shortest path verified
- ✔ Query budget respected
- ✔ JWT token generated successfully

---

## Key Learnings

- Graph anomaly detection relies on **relative behavior**, not absolute values
- Central nodes are often normal — anomalies hide in **sparse regions**
- Efficient querying is critical under constraints
- Clues map directly to measurable attributes

---

## Conclusion

The solution required:

- Careful interpretation of clues
- Strategic exploration (not brute force)
- Graph traversal reasoning (BFS-style thinking)
- Identification of anomalous patterns

Final Answer:
- **Compromised Node:** 112  
- **Shortest Path:** 11,7,112  

✔ Successfully solved within query limits.# GA1 — Q10: Network Game — Graph Detective

## Problem Summary

In this task, we interact with an online **transaction graph game** where:

- Each node represents an account
- Edges represent transaction relationships
- We have a **limited query budget (55 queries)**
- Goal:
  - Identify the **compromised node**
  - Provide the **shortest proof path** from the anchor node

The system validates:
- Correct compromised node
- Valid shortest path
- JWT token returned after successful submission

---

## Game Understanding

### Initial Setup

- Anchor node: **11**
- Query budget: **55**
- Nodes are hidden initially (grey)
- Clicking a node reveals:
  - Degree
  - Neighbors
  - Transaction statistics

---

## Clues Interpretation

Given clues:

1. Only a handful of counterparties are involved, yet volumes are extraordinary  
2. Transactions are rare but individually massive  
3. The account moves enormous sums but almost never receives  

---

### Translating Clues → Metrics

| Clue | Metric |
|------|--------|
| Few counterparties | `counterparty_count LOW` |
| Rare transactions | `tx_count_daily LOW` |
| Huge volume | `tx_volume_daily HIGH` |
| Mostly outgoing | `in_out_ratio VERY LOW` |

---

## Exploration Strategy

### Step 1 — Start from Anchor Node

Queried node **11**:
- High degree (hub node)
- Balanced transactions
- Not suspicious

---

### Step 2 — Expand Neighbors

Explored multiple neighbors:
- 51
- 98
- 32
- 63
- 76
- 46
- etc.

Observation:
- Most nodes were:
  - High degree
  - Balanced in/out ratios
  - Moderate transaction counts

Conclusion:
👉 These are **normal nodes in dense cluster**

---

### Step 3 — Key Insight

Compromised node is likely:

- NOT a hub
- NOT central
- NOT highly connected

👉 Instead:
- Low connectivity
- Extreme behavior

---

### Step 4 — Move to Sparse / Outer Nodes

Shifted exploration to nodes away from cluster.

---

## Final Discovery

### Node 112

```
id: 112
degree: 3
neighbors: 7, 41, 103
tx_volume_daily: 30800
tx_count_daily: 3
in_out_ratio: 0.03
counterparty_count: 4
```

---

## Why Node 112 is Correct

| Metric | Value | Matches Clue |
|------|------|-------------|
| counterparty_count | 4 | ✅ few |
| tx_count_daily | 3 | ✅ rare |
| tx_volume_daily | 30800 | ✅ huge |
| in_out_ratio | 0.03 | ✅ mostly outgoing |

👉 Perfect match with all clues

---

## Shortest Proof Path

We verify connections:

- Node 112 neighbors → **7, 41, 103**
- Node 11 neighbors include → **7**

Thus:

```
11 → 7 → 112
```

---

### Final Path

```
11,7,112
```

- Valid edges
- Minimal hops
- Shortest path

---

## Final Submission

### Compromised Node
```
112
```

### Path
```
11,7,112
```

---

## Token Extraction

After clicking **Submit** in the game:

1. Open DevTools → Network tab
2. Locate final API response
3. Copy:
```
completion_token
```

---

## Final Result

- ✔ Correct node identified
- ✔ Shortest path verified
- ✔ Query budget respected
- ✔ JWT token generated successfully

---

## Key Learnings

- Graph anomaly detection relies on **relative behavior**, not absolute values
- Central nodes are often normal — anomalies hide in **sparse regions**
- Efficient querying is critical under constraints
- Clues map directly to measurable attributes

---

## Conclusion

The solution required:

- Careful interpretation of clues
- Strategic exploration (not brute force)
- Graph traversal reasoning (BFS-style thinking)
- Identification of anomalous patterns

Final Answer:
- **Compromised Node:** 112  
- **Shortest Path:** 11,7,112  

✔ Successfully solved within query limits.
