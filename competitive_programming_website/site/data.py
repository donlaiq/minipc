#!/usr/bin/env python3
"""Generate JSON data for all 50 problems and tests."""
import json, re

DATA = []

for qid in range(1, 51):
    pfile = f"../problems/{qid:02d}.txt"
    tfile = f"../../tests/{qid:02d}_test.txt"

    with open(pfile) as f:
        text = f.read()

    # Parse fields
    m_name = re.search(r'# Problem \d+: (.+)', text)
    name = m_name.group(1).strip() if m_name else f"Question {qid}"
    m_diff = re.search(r'\*\*Difficulty:\*\* (\w+)', text)
    difficulty = m_diff.group(1).strip() if m_diff else "Easy"
    m_topic = re.search(r'\*\*Topic:\*\* (.+)', text)
    topic = m_topic.group(1).strip() if m_topic else "Unknown"
    m_stmt = re.search(r'## Statement\n(.*?)(?=\n## Examples)', text, re.DOTALL)
    statement = m_stmt.group(1).strip() if m_stmt else ""

    # Read test cases
    tests = []
    try:
        with open(tfile) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                import ast
                try:
                    t = ast.literal_eval(line)
                    if t.get('name') and t.get('expected') is not None:
                        tests.append(t)
                except:
                    pass
    except FileNotFoundError:
        pass

    DATA.append({
        "id": qid,
        "name": name,
        "difficulty": difficulty,
        "topic": topic,
        "statement": statement,
        "tests": tests,
    })

with open("problems.json", "w") as f:
    json.dump(DATA, f)

print(f"Generated {len(DATA)} problems")
