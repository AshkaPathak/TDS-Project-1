import re
import base64
import hashlib
from pathlib import Path
import subprocess

# Step 1: read copied HTML source
html = Path("page.html").read_text()

# Step 2: extract base64 audio
match = re.search(r"data:audio/mpeg;base64,([A-Za-z0-9+/=]+)", html)

if not match:
    raise Exception("Base64 audio not found")

b64 = match.group(1)

# Step 3: decode audio
audio = base64.b64decode(b64)
Path("digits.mp3").write_bytes(audio)

print("Audio extracted")

# Step 4: run whisper
subprocess.run(
    ["python", "-m", "whisper", "digits.mp3", "--model", "medium", "--language", "en"],
    check=True
)

# Step 5: read transcript
text = Path("digits.txt").read_text()

digits = "".join(re.findall(r"\d", text))

print("Digits length:", len(digits))

# Step 6: compute hash
sha = hashlib.sha256(digits.encode()).hexdigest()

print("\nRESULT\n")
print(digits)
print("\nSHA256:", sha)
