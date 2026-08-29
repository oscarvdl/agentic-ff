import json, os, subprocess, sys, urllib.request

base = os.environ["BASE_SHA"]
result = subprocess.run(["git", "diff", base, "HEAD"], capture_output=True, text=True)
if result.returncode != 0:
    sys.exit(f"git diff against {base} failed: {result.stderr.strip()}")

diff = result.stdout[:60000]
if not diff.strip():
    sys.exit(f"no changes between {base} and HEAD, nothing to evaluate")

rubric = open("docs/adr/rubrics/boundary-intent.yml").read()

prompt = (
    "You are an architecture reviewer. Evaluate the diff against the rubric.\n"
    "Return ONLY JSON: {\"score\": float, \"confidence\": float, "
    "\"findings\": [{\"criterion\": str, \"evidence\": str, \"rationale\": str}]}\n"
    "Advisory only. Do not recommend blocking.\n\n"
    f"RUBRIC:\n{rubric}\n\nDIFF:\n{diff}"
)

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({
        "model": "claude-opus-5",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode(),
    headers={
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
)
body = json.loads(urllib.request.urlopen(req).read())

# The model thinks before it answers, so content[0] is a thinking block.
# Select the text block by type rather than by position.
text = next(b["text"] for b in body["content"] if b["type"] == "text")

# Models wrap JSON in a markdown fence even when told not to.
fence = "`" * 3
text = text.strip().removeprefix(fence + "json").removeprefix(fence).removesuffix(fence)

verdict = json.loads(text.strip())
json.dump(verdict, open("verdict.json", "w"), indent=2)
print(f"score {verdict['score']} at confidence {verdict['confidence']}, "
      f"{len(verdict['findings'])} finding(s)")
