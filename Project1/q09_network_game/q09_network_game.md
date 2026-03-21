# TDS Project 1 — Q9: Network Game — Data Labyrinth

## Problem Summary

This task involved solving an interactive browser-based maze game where:

- The maze is explored through API calls
- Each move reveals new positions and possible directions
- Data fragments are collected during traversal
- A final analytics question must be answered using the collected data
- The output is a completion JWT token returned by the game

---

## Core Insight

This is not a traditional game-solving problem.

The correct approach is to:
- Reverse engineer the backend API using browser network calls
- Programmatically explore the maze
- Collect all fragments
- Compute the final answer using data analysis

---

## Approach

### Step 1: Inspect Network Traffic

- Open browser DevTools → Network tab
- Filter for **Fetch/XHR requests**
- Perform movements in the maze
- Observe API calls triggered on each move

Key observations:
- Each move sends a request (e.g., `/move`)
- Responses contain:
  - Current position
  - Available directions
  - Optional data fragments

---

### Step 2: Understand API Structure

From network inspection:

- Movement is controlled via API calls with direction input
- The maze behaves deterministically
- Responses include all necessary state information

This allows full automation of exploration.

---

### Step 3: Automate Exploration

A Python script was used to simulate the game:

- Send requests to move in directions
- Track visited positions
- Avoid revisiting nodes
- Explore the entire maze using DFS/BFS

---

### Step 4: Maze Traversal Strategy

- Use a set to track visited states
- Use recursion or queue-based BFS
- Explore all reachable nodes

Data tracked:
- Position (coordinates or identifiers)
- Available moves
- Fragment data

---

### Step 5: Collect Data Fragments

During traversal:
- Extract fragment data from API responses
- Store all fragments in a list

Example structure:
- JSON objects containing attributes required for final analysis

---

### Step 6: Perform Data Analysis

After collecting all fragments:

- Convert data into structured format (e.g., Pandas DataFrame)
- Apply required transformations:
  - Filtering
  - Aggregation (sum, average, count, etc.)
  - Grouping if needed

Solve the final analytics question using this dataset.

---

### Step 7: Submit Final Answer

- Send computed result back through the game interface
- The system returns a **completion JWT token**

---

## Output

The final submission consists of:

- A JWT token returned by the system after correct solution

This token:
- Is signed using the game’s public key
- Contains:
  - User identifier
  - Game identifier
  - Week identifier
  - Timestamp

---

## Verification Conditions

The submission is validated based on:

1. Valid JWT signature
2. Matching user email
3. Correct game identifier (`labyrinth`)
4. Current ISO week match
5. Completion timestamp within valid range

---

## Key Learnings

- Reverse engineering APIs using browser DevTools
- Treating UI-based problems as backend data problems
- Applying graph traversal (DFS/BFS) in real-world scenarios
- Automating workflows using Python and requests
- Performing data analysis on dynamically collected datasets

---

## Conclusion

This problem required combining:
- Web debugging skills
- Algorithmic thinking
- Data processing

Instead of manually navigating the maze, the optimal solution involved automating the exploration and solving the problem programmatically, demonstrating a practical application of data science and systems thinking.
