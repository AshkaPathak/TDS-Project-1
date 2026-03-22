# Project 1 — Q9: Network Game — Data Labyrinth

## Problem Summary
Open the weekly Data Labyrinth game, explore the maze, collect all fragments, compute the required statistic, and submit the final answer to obtain the completion JWT. In this run, the question was: “How many records have response_ms greater than the 75th percentile of response_ms? Exclude incomplete records.”

## Approach Overview
This problem required interacting with the backend API instead of relying on the UI. The workflow was: collect all fragments → fetch inventory using session token → filter out distractors → parse valid data → compute percentile correctly → navigate to submission room (room 120) → submit answer via API → copy completion token.

## Step 1 — Get Session Token
Use the browser console to retrieve the session token:
sessionStorage.getItem("tds_token_labyrinth")

This token must be included in all API requests as:
"X-Session-Token": token

## Step 2 — Fetch Inventory Data
Run the following in console:
(async () => {
  const token = sessionStorage.getItem("tds_token_labyrinth");
  const res = await fetch("/labyrinth/inventory", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": token
    }
  });
  const inv = await res.json();
  console.log(inv);
})();

## Step 3 — Extract Valid Records
Filter out distractors and parse usable rows:
const rows = (inv.fragments || [])
  .filter(f => f.type !== "distractor")
  .map(f => {
    let d = f.data;
    if (typeof d === "string") {
      try { d = JSON.parse(d); } catch {}
    }
    return d;
  })
  .filter(d => d && d.response_ms != null && !Number.isNaN(Number(d.response_ms)));

const values = rows
  .map(d => Number(d.response_ms))
  .sort((a, b) => a - b);

## Step 4 — Compute 75th Percentile
Use nearest-rank method (the one accepted by the platform):
const n = values.length;
const idx = Math.ceil(0.75 * n) - 1;
const p75 = values[idx];
const answer = values.filter(v => v > p75).length;

console.log("FINAL ANSWER =", answer);

## Step 5 — Navigate to Room 120
Use API movement helper:
async function mv(direction) {
  const token = sessionStorage.getItem("tds_token_labyrinth");
  const res = await fetch("/labyrinth/move", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": token
    },
    body: JSON.stringify({ direction })
  });
  return await res.json();
}

Move only using available exits until:
room_id = 120

## Step 6 — Submit Answer
(async () => {
  const token = sessionStorage.getItem("tds_token_labyrinth");
  const res = await fetch("/labyrinth/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": token
    },
    body: JSON.stringify({ answer })
  });
  const json = await res.json();
  console.log(json);
})();

## Final Answer
3

## Conclusion
The key to solving this problem was avoiding UI-based assumptions and instead interacting directly with the API. Correct filtering of fragments, proper percentile computation (nearest-rank), and ensuring submission from room 120 were critical to obtaining the correct result and completion token.
