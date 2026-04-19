#!/usr/bin/env python3
"""Generate problems.json with full descriptions, test data, and function names."""
import json
import os
import re
from ast import literal_eval

BASE = '/home/don/ai/openclaw_projects/competitive'

def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def format_inline(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*(.+?)\*', r'<i>\1</i>', s)
    return s

DATA = []

for qid in range(1, 51):
    pfile = os.path.join(BASE, 'problems', f'{qid:02d}.txt')
    tfile = os.path.join(BASE, 'tests', f'{qid:02d}_test.txt')
    sfile = os.path.join(BASE, 'tests', f'{qid:02d}.py')

    with open(pfile) as f:
        text = f.read()

    name = f'Question {qid}'
    m_name = re.search(r'# Problem \d+: (.+)', text)
    if m_name:
        name = m_name.group(1).strip()

    difficulty = 'Easy'
    m_diff = re.search(r'\*\*Difficulty:\*\* (.+)', text)
    if m_diff:
        difficulty = m_diff.group(1).strip()

    topic = 'Unknown'
    m_topic = re.search(r'\*\*Topic:\*\* (.+)', text)
    if m_topic:
        topic = m_topic.group(1).strip()

    body = text
    body = re.sub(r'^# Problem \d+: .+\n\n', '', body, count=1)
    body = re.sub(r'^\*\*Difficulty:\*\* .+\n', '', body, count=1)
    body = re.sub(r'^\*\*Topic:\*\* .+\n', '', body, count=1)

    lines = body.split('\n')
    html_lines = []
    in_ul = False
    in_pre = False
    pre_buf = []

    for line in lines:
        if line.startswith('## '):
            if in_ul: html_lines.append('</ul>'); in_ul = False
            if in_pre: html_lines.append('<pre style="background:#161b22;padding:12px 16px;border-radius:8px;margin:8px 0;overflow-x:auto;"><code>' + escape_html(''.join(pre_buf)) + '</code></pre>'); in_pre = False; pre_buf = []
            html_lines.append(f'<h3 style="color:#58a6ff;margin-top:16px;margin-bottom:8px;">{format_inline(line[3:])}</h3>')
        elif line.startswith('```'):
            if in_pre:
                html_lines.append('<pre style="background:#161b22;padding:12px 16px;border-radius:8px;margin:8px 0;overflow-x:auto;"><code>' + escape_html('\n'.join(pre_buf)) + '</code></pre>')
                in_pre = False; pre_buf = []
            else:
                in_pre = True
        elif in_pre:
            pre_buf.append(escape_html(line))
        elif line.startswith('- ') or line.startswith('* '):
            if not in_ul: html_lines.append('<ul style="padding-left:20px;margin:4px 0;">'); in_ul = True
            item = format_inline(line.lstrip('-* '))
            html_lines.append(f'<li style="margin:3px 0;color:#8b949e;">{item}</li>')
        elif in_ul and line.strip() == '':
            html_lines.append('</ul>'); in_ul = False
        elif line.strip() == '':
            if in_ul: html_lines.append('</ul>'); in_ul = False
            html_lines.append('')
        else:
            if in_ul: html_lines.append('</ul>'); in_ul = False
            html_lines.append(format_inline(line))

    if in_ul: html_lines.append('</ul>')
    if in_pre:
        html_lines.append('<pre style="background:#161b22;padding:12px 16px;border-radius:8px;margin:8px 0;overflow-x:auto;"><code>' + escape_html('\n'.join(pre_buf)) + '</code></pre>')

    body_html = '<br>'.join(html_lines)

    tests = []
    if os.path.exists(tfile):
        with open(tfile) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                if not line.startswith('{'):
                    continue
                try:
                    t = literal_eval(line)
                    if t.get('name') and t.get('expected') is not None:
                        tests.append(t)
                except Exception:
                    pass

    # Extract function name from solution file
    # Always prefer 'solve' if present (it's what the runner expects)
    func_name = 'solve'
    if os.path.exists(sfile):
        with open(sfile) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('def '):
                fname = line.split('(')[0].replace('def ', '').strip()
                if fname == 'solve':
                    func_name = fname
                    break
        else:
            # No solve found, pick the first def
            for line in lines:
                line = line.strip()
                if line.startswith('def '):
                    func_name = line.split('(')[0].replace('def ', '').strip()
                    break

    # Extract parameter names from tests for hints
    param_names = []
    if tests:
        first_input = tests[0].get('input', {})
        if isinstance(first_input, dict):
            param_names = list(first_input.keys())

    DATA.append({
        'id': qid,
        'name': name,
        'difficulty': difficulty,
        'topic': topic,
        'description': body_html,
        'tests': tests,
        'func_name': func_name,
        'param_names': param_names,
    })

with open(os.path.join(BASE, 'problems.json'), 'w') as f:
    json.dump(DATA, f)
print(f'Generated {len(DATA)} problems')
for p in DATA[:5]:
    print(f'  Q{p["id"]:2d}: {p["name"]:45s} func={p["func_name"]} params={p["param_names"]}')
