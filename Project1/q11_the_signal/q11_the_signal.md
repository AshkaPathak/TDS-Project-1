# Project 1 — Q11: Network Game — The Signal

## Problem Summary

This task required solving the online escape-room style game **The Signal**. The facility consists of interconnected rooms containing items, terminals, logs, and locked progression paths. The objective was to solve four chained puzzles:

1. **PIN**
2. **Frequency**
3. **Verify**
4. **Passcode / Exit**

The final submission required the **completion JWT token** returned after escaping successfully.

---

## Facility Layout

The game map was:

```text
[ENT]—[SRA]—[SRB]
  |      |
 [STR]  [MAI]—[PWR]
  |      |
 [LAB]—[CTL]—[ARC]
          |
         [COR] ← EXIT
```

Where:

- `ENT` = Entrance Hall
- `SRA` = Server Room A
- `SRB` = Server Room B
- `STR` = Storage Room
- `MAI` = Maintenance Bay
- `PWR` = Power Room
- `LAB` = Laboratory
- `CTL` = Control Room
- `ARC` = Archive Room
- `COR` = Core Chamber / Exit area

---

## Initial Strategy

The game is deterministic, so the correct approach was:

- crawl all reachable rooms
- collect all visible items
- solve small puzzles first
- craft required items
- re-crawl newly unlocked rooms
- solve terminal-based puzzles in dependency order
- assemble final passcode
- extract the completion token

---

## Important Items Found

During traversal, the following relevant items were collected:

- `FACILITY_MAP`
- `MAINTENANCE_KEY`
- `BROKEN_RADIO`
- `NOTEBOOK`
- `INSPECTION_CERTIFICATE`
- `SPECIMEN_KEY`
- `DRIED_MARKER`
- `POWER_CELL`
- `SIGNAL_LOG`
- `BACKUP_LOG`
- `SYSTEM_BADGE`
- `UV_TORCH`
- `ACCESS_CARD` / `REPAIRED_ACCESS_CARD`
- `CLEANING_CLOTH`
- `SOLVENT_BOTTLE`
- `FREQUENCY_TUNER`
- `POWERED_TUNER`

---

## Crafting Logic

The game required specific crafting recipes.

### Recipe 1
```text
CLEANING_CLOTH + SOLVENT_BOTTLE → DEMAGNETISER
```

### Recipe 2
```text
DEMAGNETISER + ACCESS_CARD → REPAIRED_ACCESS_CARD
```

### Recipe 3
```text
FREQUENCY_TUNER + POWER_CELL → POWERED_TUNER
```

These crafted items unlocked later rooms and puzzles.

---

## Puzzle 1 — PIN

### Clues Used

From the **NOTEBOOK**:

```text
"PIN = inspection year + sublevel number"
"Level 2 sublevel"
"The floor number 2 is circled"
```

From the **INSPECTION_CERTIFICATE**:

```text
Inspection date: 2021
```

### PIN Derivation

```text
PIN = 2021 + 2 = 2023
```

### Result

Using `PIN_TERMINAL` with `2023` revealed:

```text
Fragment 1 = NPQL
```

---

## Puzzle 2 — Frequency

This puzzle initially appeared confusing because the transmitter only asked for a frequency and did not directly reveal one. The key requirement was:

- obtain `POWERED_TUNER`
- collect `SIGNAL_LOG`
- collect `BACKUP_LOG`

### Signal Log Readings

From `SIGNAL_LOG`, the extracted MHz values were:

```text
102.1, 100.9, 89.9, 102.7, 102.6, 88.4, 102.6, 90.5, 93.8, 96.0, 90.1, 107.1, 91.5, 103.9, 102.6
```

### Frequency Selection Rule

A hint indicated:

> Emergency channels were pre-set to avoid ambiguity. One channel was logged more frequently than others; the repetition was intentional.

Since `BACKUP_LOG` parsing did not yield a usable MHz list in the final working run, the repeated-frequency rule was applied.

The most frequent value in `SIGNAL_LOG` was:

```text
102.6 MHz
```

### Result

Using `RADIO_TRANSMITTER` with:

```text
102.6
```

revealed:

```text
Fragment 2 = R7GT
```

---

## Puzzle 3 — Verify

The **Control Room** contained `TERMINAL_3`, which required the first two fragments as ordered inputs.

### Inputs Used

```text
Fragment 1 = NPQL
Fragment 2 = R7GT
```

Using `TERMINAL_3` with:

```text
[NPQL, R7GT]
```

revealed:

```text
Fragment 3 = FMB9
```

and unlocked:

```text
CONTROL_CORE
```

---

## Puzzle 4 — Final Passcode

The final passcode was formed by concatenating the three fragments:

```text
NPQL + R7GT + FMB9 = NPQLR7GTFMB9
```

So the final passcode was:

```text
NPQLR7GTFMB9
```

---

## Final Escape

After Verify, the Control Room south path opened into the **Core Chamber**.

From there, using:

```text
EXIT_KEYPAD
```

with:

```text
NPQLR7GTFMB9
```

successfully completed the game and returned the **completion JWT token**.

---

## Automation Approach

A browser-console automation script was ultimately used to solve the game reliably. The script performed:

- session start
- room traversal using live exit data
- item pickup
- crafting known recipes
- room re-crawl after unlocking paths
- PIN derivation from notebook + certificate
- frequency derivation from signal logs
- verification at `TERMINAL_3`
- final navigation to Core Chamber
- exit keypad submission
- completion token extraction

---

## Final Answers

### Fragment 1
```text
NPQL
```

### Fragment 2
```text
R7GT
```

### Fragment 3
```text
FMB9
```

### Final Passcode
```text
NPQLR7GTFMB9
```

---

## Conclusion

The Signal was a structured multi-stage puzzle involving:

- deterministic map traversal
- item collection
- crafting dependencies
- text clue interpretation
- signal-frequency analysis
- ordered fragment verification
- final passcode assembly

The correct solution path was:

1. solve PIN → `NPQL`
2. solve Frequency → `R7GT`
3. verify both fragments → `FMB9`
4. concatenate into final passcode → `NPQLR7GTFMB9`
5. use exit keypad to receive the completion token

This completed **Project 1 — Q11** successfully.
