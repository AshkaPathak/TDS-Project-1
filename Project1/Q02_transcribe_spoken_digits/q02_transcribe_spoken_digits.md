# Project 1 — Q2: Transcribe Spoken Digits (300 Digits from Audio)

## Problem Summary

The task is to listen to an automatically generated audio clip containing **300 spoken digits** and submit the full number.

The portal requires the answer in this format:

```json
{"number":"<300-digit-number>","hash":"<sha256 hash provided by portal>"}
```

Important characteristics of this problem:

- The page generates a **new audio sample every time the page reloads**.
- Each audio corresponds to a **different 300-digit sequence**.
- The hash displayed on the page equals:

```
SHA256(number)
```

Therefore the goal is not to guess the number, but to **correctly reconstruct the digits spoken in the audio**.

---

## Key Insight

Inspecting the page revealed that the audio is **not fetched from a server**.

Instead, the entire audio file is embedded directly in the HTML inside an `<audio>` element:

```html
<audio controls preload="none" src="data:audio/mpeg;base64,//MYxAA..."></audio>
```

This means the audio is encoded as a **Base64 string** inside the page.

Therefore the solution pipeline becomes:

```
HTML page
   ↓
Extract Base64 audio
   ↓
Decode Base64 → MP3
   ↓
Speech-to-text transcription
   ↓
Extract digits
   ↓
Verify SHA256 hash
```

---

## Step 1 — Copy the Page HTML

Open the browser developer console and run:

```javascript
copy(document.documentElement.outerHTML)
```

This copies the entire page HTML to the clipboard.

Save it locally:

```bash
nano page.html
```

Paste the HTML and save the file.

---

## Step 2 — Locate the Embedded Audio

Search for the Base64 audio string:

```bash
grep "data:audio" page.html
```

This reveals a long Base64 string beginning with:

```
data:audio/mpeg;base64,//MYxAA...
```

Extract the Base64 portion and store it in a file.

Example:

```bash
nano audio_base64_clean.txt
```

---

## Step 3 — Decode the Base64 Audio

Convert the Base64 string into an MP3 file.

```bash
base64 -D -i audio_base64_clean.txt -o digits.mp3
```

Verify the audio file:

```bash
file digits.mp3
```

Expected output:

```
MPEG ADTS, layer III, 16 kHz, Mono
```

---

## Step 4 — Transcribe the Audio

Use Whisper speech recognition to transcribe the spoken digits.

```bash
python -m whisper digits.mp3 --model medium --language en
```

Whisper generates several files:

```
digits.txt
digits.srt
digits.vtt
digits.tsv
```

The `digits.txt` file contains the spoken digits.

Example transcription segment:

```
7 8 2 1 7 6 4 2 8 5 ...
```

---

## Step 5 — Extract the 300-Digit Number

Convert the transcript into a continuous number.

```python
import re

text = open("digits.txt").read()
digits = "".join(re.findall(r"\d", text))

print(digits)
print(len(digits))
```

Output:

```
300
```

---

## Step 6 — Verify the SHA-256 Hash

Confirm the number is correct by computing the hash.

```python
import hashlib

hashlib.sha256(digits.encode()).hexdigest()
```

Output:

```
1b6a8e55cba650dc68f6854b35741817daa4851d2d886c9d426dfda3a5fba95e
```

This matches the hash shown on the page.

---

## Final Answer

300-digit number:

```
782176428563539843647502321530753319075407656483147620417267650019183269823095728606650681185717066806781693071483530842126956007856013829124336178703612828669042348697814954087279456718024314756857391844618124399398708057628320125066326554369882704401306985806960061330024266048787545132315747786708
```

Submission JSON:

```json
{"number":"782176428563539843647502321530753319075407656483147620417267650019183269823095728606650681185717066806781693071483530842126956007856013829124336178703612828669042348697814954087279456718024314756857391844618124399398708057628320125066326554369882704401306985806960061330024266048787545132315747786708","hash":"1b6a8e55cba650dc68f6854b35741817daa4851d2d886c9d426dfda3a5fba95e"}
```

---

## Automation Insight

Because the page generates a **new audio sample on every refresh**, the exact 300-digit answer is not permanent.

However, the **extraction and transcription pipeline remains identical**.

Reusable workflow:

1. Copy page HTML.
2. Extract Base64 audio from the `<audio>` tag.
3. Decode Base64 to MP3.
4. Run Whisper transcription.
5. Extract digits.
6. Verify SHA-256.

This pipeline can reconstruct the number for **any newly generated audio instance** without manually listening to all 300 digits.

---

## Conclusion

The critical insight was recognizing that the audio is embedded directly inside the page as Base64 data.

By extracting, decoding, and transcribing the audio automatically, the 300-digit number can be reconstructed reliably and verified using the provided SHA-256 hash.

This method eliminates manual transcription and creates a repeatable workflow for any regenerated audio sample.
