# TDS Project 1 — Q1: Secret Agent Password Exchange

## Problem Summary

In this task, each participant is assigned a **secret agent ID and password**.  
To complete the question, we must retrieve the **email and password of three other agents** and submit them in the required JSON format.

My assigned agent details:

Agent ID: **083**  
Password: **d8ee91c442469516**

The assignment required collecting the credentials of the following agents:

- Agent 042
- Agent 004
- Agent 082

The final submission must include three objects with:

- `agent_id`
- `email`
- `password`

---

## Strategy

This question is designed as a **distributed coordination problem** rather than a programming challenge.

Possible ways to obtain the required credentials included:

1. Searching discussion forums where students exchange credentials.
2. Posting our own agent information to encourage cooperative exchange.
3. Collecting credentials shared publicly by other participants.

During the process, a community-built indexing tool aggregated publicly shared credentials and allowed searching by agent ID. Using this tool, the required agent credentials were retrieved quickly.

The retrieved information was then formatted into the required JSON structure for submission.

---

## Retrieved Agent Credentials

### Agent 042

Email  
```
21f1000006@ds.study.iitm.ac.in
```

Password  
```
af762065b1a6a7c4
```

---

### Agent 004

Email  
```
21f1000003@ds.study.iitm.ac.in
```

Password  
```
0400e9ac955a018c
```

---

### Agent 082

Email  
```
21f1000241@ds.study.iitm.ac.in
```

Password  
```
03732fd9fdbc27b3
```

---

## Final Submission JSON

```json
[
  {
    "agent_id": "042",
    "email": "21f1000006@ds.study.iitm.ac.in",
    "password": "af762065b1a6a7c4"
  },
  {
    "agent_id": "004",
    "email": "21f1000003@ds.study.iitm.ac.in",
    "password": "0400e9ac955a018c"
  },
  {
    "agent_id": "082",
    "email": "21f1000241@ds.study.iitm.ac.in",
    "password": "03732fd9fdbc27b3"
  }
]
```

---

## Key Insight

This problem demonstrates how **network coordination and information exchange** are often required in distributed environments.

Rather than solving a computational problem, the task tests:

- collaboration among participants
- discovery of publicly shared information
- efficient data aggregation
- formatting data correctly for submission

These principles mirror real-world distributed systems where independent agents must cooperate to obtain information.

---

## Result

Credentials for all required agents were successfully retrieved and formatted into the required JSON structure for submission.
