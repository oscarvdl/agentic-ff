import json

v = json.load(open("verdict.json"))
print(f"**Architecture fitness: {v['score']} (confidence {v['confidence']})**\n")
for f in v["findings"]:
    print(f"- `{f['criterion']}` at {f['evidence']}: {f['rationale']}")