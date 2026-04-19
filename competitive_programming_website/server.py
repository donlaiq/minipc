#!/usr/bin/env python3
"""Minimal HTTP server for the CP Platform. Pure stdlib, no Flask."""
import json, os, subprocess, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE, "tests")
PROBLEMS_FILE = os.path.join(BASE, "problems.json")

# Write the runner script once at startup
RUNNER_PATH = os.path.join(BASE, "_runner.py")
with open(RUNNER_PATH, "w") as f:
    f.write("""import sys
import os
import json
import importlib.util

sol_path = os.environ["SOL_PATH"]
tests_path = os.environ["TESTS_FILE"]

# Load user solution
spec = importlib.util.spec_from_file_location("user_sol", sol_path)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except Exception as e:
    print("[✗] Load Error  EXCEPTION: " + str(e), file=sys.stderr)
    sys.exit(0)

# Load tests
with open(tests_path) as f:
    tests = json.load(f)

# Find the solve function — try func_name from tests first, then fallbacks
found_func = None
candidates = []

# Gather expected function names from test metadata
if tests and isinstance(tests, list) and len(tests) > 0:
    fn = tests[0].get('func_name')
    if fn:
        candidates.append(fn)

# Always include standard fallbacks
for candidate in ["solve", "solution"]:
    if candidate not in candidates:
        candidates.append(candidate)

for candidate in candidates:
    if hasattr(mod, candidate):
        found_func = getattr(mod, candidate)
        break

if not found_func:
    print("ERROR: No solve/solution function found in solution", file=sys.stderr)
    sys.exit(1)

# Run each test
passed = 0
failed = 0
for i, tc in enumerate(tests):
    name = tc.get("name", "Case " + str(i + 1))
    inp = tc.get("input")
    expected = tc.get("expected")
    try:
        if isinstance(inp, dict):
            result = found_func(**inp)
        elif isinstance(inp, list) and len(inp) == 0:
            result = found_func()
        else:
            result = found_func(inp)
    except Exception as e:
        print("[✗] " + name + "  EXCEPTION: " + str(e), file=sys.stderr)
        failed += 1
        continue
    if result == expected:
        print("[✓] " + name + "  OK")
        passed += 1
    else:
        print("[✗] " + name + "  FAILED", file=sys.stderr)
        failed += 1

print("PASSED=" + str(passed))
print("FAILED=" + str(failed))
""")

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/problems":
            with open(PROBLEMS_FILE) as f:
                data = json.load(f)
            body = json.dumps([
                {"id": p["id"], "name": p["name"],
                 "difficulty": p["difficulty"], "topic": p["topic"]}
                for p in data
            ]).encode()
            self._json(body)
            return

        if parsed.path == "/api/problem":
            qs = parse_qs(parsed.query)
            qid = qs.get("id", [None])[0]
            if not qid:
                self._json(b'{"error":"no qid"}', 400); return
            with open(PROBLEMS_FILE) as f:
                data = json.load(f)
            for p in data:
                if str(p["id"]) == qid:
                    self._json(json.dumps(p).encode()); return
            self._json(b'{"error":"not found"}', 404)
            return

        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            raw = self.rfile.read(length)
            payload = json.loads(raw)
        except Exception:
            self._json(b'{"error":"bad payload"}', 400); return

        qid = str(payload.get("qid", "")).zfill(2)
        code = payload.get("code", "")
        if not qid:
            self._json(b'{"error":"no qid"}', 400); return

        # Get problem + tests from problems.json
        with open(PROBLEMS_FILE) as f:
            all_problems = json.load(f)
        problem = None
        for p in all_problems:
            if p["id"] == int(qid):
                problem = p
                break
        if not problem:
            self._json(b'{"error":"problem not found"}', 404); return

        # Write user code to a temp file (NEVER overwrite tests/NN.py)
        sol_file = os.path.join(BASE, "_user_sol_tmp.py")
        with open(sol_file, "w") as f:
            f.write(code)

        # Write tests to a temp JSON file for the runner
        tests_file = os.path.join(BASE, "_tests_tmp.json")
        test_data = list(problem["tests"])  # copy the list
        if problem.get("func_name"):
            test_data[0]["func_name"] = problem["func_name"]  # tag first test with func_name
        with open(tests_file, "w") as f:
            json.dump(test_data, f)

        # Run the runner script
        env = os.environ.copy()
        env["SOL_PATH"] = sol_file
        env["TESTS_FILE"] = tests_file
        result = subprocess.run(
            [sys.executable, RUNNER_PATH],
            capture_output=True, text=True, timeout=30, env=env
        )
        output = result.stdout + result.stderr
        # Clean up temp files
        for tmp in [sol_file, tests_file]:
            if os.path.exists(tmp):
                os.remove(tmp)

        # Parse results
        test_results = []
        passed = 0
        failed = 0

        for line in output.split('\n'):
            if not line.strip():
                continue
            if line.startswith('[✓]'):
                rest = line.split('[✓]')[1].strip()
                name = rest.split('  OK')[0].strip() if '  OK' in rest else rest
                test_results.append({'name': name, 'status': 'pass', 'message': 'Correct!'})
                passed += 1
            elif line.startswith('[✗]'):
                rest = line.split('[✗]')[1].strip()
                name = rest.split('  FAILED')[0].strip() if '  FAILED' in rest else rest
                msg = rest.split('FAILED')[1].strip() if 'FAILED' in rest else ''
                test_results.append({'name': name, 'status': 'fail', 'message': msg})
                failed += 1
            elif line.startswith('[E]') or 'EXCEPTION' in line:
                test_results.append({'name': 'Error', 'status': 'error', 'message': line})
                failed += 1

        all_passed = passed == len(problem['tests']) and failed == 0
        # If the runner crashed silently (no test lines at all), mark as failed
        if passed == 0 and failed == 0 and result.returncode != 0:
            failed = len(problem['tests'])
            all_passed = False
            test_results = [{'name': 'Runtime Error', 'status': 'error', 'message': output.strip() if output.strip() else 'Unknown error'}]
        elif passed == 0 and failed == 0:
            # Runner exited cleanly but no tests ran — likely missing/invalid function
            failed = len(problem['tests'])
            all_passed = False
            test_results = [{'name': 'Runtime Error', 'status': 'error', 'message': 'No tests ran — verify the function name matches the signature shown above'}]

        response = {
            'passed': passed,
            'failed': failed,
            'total': passed + failed,
            'all_passed': all_passed,
            'test_results': test_results,
        }
        self._json(json.dumps(response).encode())

    def _json(self, body, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    os.chdir(BASE)
    server = HTTPServer(('0.0.0.0', port), Handler)
    print('CP Platform running on http://localhost:' + str(port))
    server.serve_forever()
