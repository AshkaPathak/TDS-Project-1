import json
from solution import parse_markdown

with open("commonmark_spec.json", "r", encoding="utf-8") as f:
    tests = json.load(f)

passed = 0
failed = 0

for i, item in enumerate(tests):
    if isinstance(item, dict):
        md = item.get("markdown") or item.get("md") or item.get("input")
        expected = item.get("html") or item.get("output")
    else:
        md, expected = item

    got = parse_markdown(md)

    if got == expected:
        passed += 1
    else:
        failed += 1
        print(f"\nFAILED TEST #{i}")
        print("MARKDOWN:")
        print(repr(md))
        print("EXPECTED:")
        print(repr(expected))
        print("GOT:")
        print(repr(got))
        print("-" * 80)

print(f"\nPassed: {passed}")
print(f"Failed: {failed}")
print(f"Total: {passed + failed}")

