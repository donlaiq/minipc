import sys
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
