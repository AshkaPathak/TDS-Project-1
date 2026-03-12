# TDS Project 1 — Q2: Transcribe Spoken Digits

## Problem Summary

This task provided an audio clip containing a spoken **300-digit number**.  
The objective was to transcribe the full number exactly and submit it along with the provided SHA-256 hash.

Important constraint:

- A new audio sample is generated every time the page is reloaded.
- Therefore, the currently visible audio and hash had to be handled together without refreshing the page.

---

## Initial Observation

At first, the browser Network tab did not show any `.wav`, `.mp3`, or `.ogg` file request.

On inspecting the HTML of the audio player, the following pattern was found:

```html
<audio controls preload="none" src="data:audio/mpeg;base64,...">
```

This revealed that the full audio file was embedded directly in the page as a **Base64-encoded MP3**.

So the correct workflow became:

1. Extract the Base64 audio data from the HTML
2. Decode it into an MP3 file
3. Transcribe the spoken digits automatically
4. Join the digits into one continuous 300-digit number
5. Verify the number using the given SHA-256 hash

---

## Extraction Process

### Step 1 — Inspect the audio element

The audio player HTML showed:

```html
<audio controls preload="none" src="data:audio/mpeg;base64,...">
```

This confirmed that the audio was embedded directly in the page source.

### Step 2 — Copy the Base64 string

Only the part after:

```text
data:audio/mpeg;base64,
```

was copied and saved into a text file.

### Step 3 — Clean and decode the Base64

The Base64 string was cleaned and decoded into an MP3 file.

Example command used:

```bash
base64 -D -i audio_base64_clean.txt -o digits.mp3
```

### Step 4 — Verify audio file

```bash
file digits.mp3
```

Output confirmed that the file was a valid MP3 audio file.

---

## Transcription Process

### Step 5 — Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 6 — Install Whisper

```bash
pip install --upgrade pip
pip install openai-whisper
```

### Step 7 — Run speech recognition

Initial transcription with the `small` model produced a 302-digit sequence, indicating minor insertion errors.

A better transcription was obtained using the `medium` model:

```bash
python -m whisper digits.mp3 --model medium --language en
```

### Step 8 — Extract only digits

The transcript was processed to keep only numeric characters.

Verification script used:

```bash
python - <<'PY'
import re, hashlib
text = open("digits.txt").read()
digits = "".join(re.findall(r"\d", text))
print(digits)
print("length =", len(digits))
print("sha256 =", hashlib.sha256(digits.encode()).hexdigest())
PY
```

---

## Final Transcribed Number

```text
782176428563539843647502321530753319075407656483147620417267650019183269823095728606650681185717066806781693071483530842126956007856013829124336178703612828669042348697814954087279456718024314756857391844618124399398708057628320125066326554369882704401306985806960061330024266048787545132315747786708
```

Length:

```text
300
```

---

## Hash Verification

Given hash:

```text
1b6a8e55cba650dc68f6854b35741817daa4851d2d886c9d426dfda3a5fba95e
```

Computed SHA-256 of the transcribed 300-digit number:

```text
1b6a8e55cba650dc68f6854b35741817daa4851d2d886c9d426dfda3a5fba95e
```

The computed hash matched exactly.

---

## Final Submission JSON

```json
{
  "number": "782176428563539843647502321530753319075407656483147620417267650019183269823095728606650681185717066806781693071483530842126956007856013829124336178703612828669042348697814954087279456718024314756857391844618124399398708057628320125066326554369882704401306985806960061330024266048787545132315747786708",
  "hash": "1b6a8e55cba650dc68f6854b35741817daa4851d2d886c9d426dfda3a5fba95e"
}
```

---

## Key Insight

This question was not meant to be solved by brute force against SHA-256.

The real challenge was to:

- inspect the page carefully
- realize the audio was embedded in Base64 form
- decode it properly
- use speech recognition
- validate the transcription with the provided hash

The verification hash served only to confirm correctness of the transcription.

---

## Result

Successfully extracted the embedded audio, transcribed the spoken digits, verified the SHA-256 hash, and produced the correct 300-digit submission.
