#!/usr/bin/env python3
"""
Test runner for competitive programming problems.
Run: python3 run_tests.py                    # all questions
     python3 run_tests.py 01                 # only question 01
     python3 run_tests.py 01 02 03           # specific questions

File structure:
  tests/
    01.py           - solution for Q1
    01_test.txt     - test cases for Q1
    run_tests.py    - this runner
"""
import sys, os, importlib.util, traceback

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

def load_solution(qid):
    path = os.path.join(TEST_DIR, f"{qid:02d}.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(f"q{qid}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_tests():
    qids = sorted([int(f.replace('.py','')) for f in os.listdir(TEST_DIR)
                   if f.endswith('.py') and f[0].isdigit() and f[0] != '_'])

    if len(sys.argv) > 1:
        selected = set()
        for a in sys.argv[1:]:
            try:
                qid = int(a)
                if 1 <= qid <= 50:
                    selected.add(qid)
            except ValueError:
                pass
        if selected:
            qids = [q for q in qids if q in selected]

    overall_pass = True
    total_p = total_f = total_s = 0

    for qid in qids:
        mod = load_solution(qid)
        if not mod:
            print(f"\n[SKIP] Q{qid:02d}: no solution file")
            continue

        # Find the main solve function
        fn = None
        for name in ['solve', 'solution', f'solve{qid}', f'solution{qid}']:
            if hasattr(mod, name):
                fn = getattr(mod, name); break

        if not fn:
            print(f"\n[SKIP] Q{qid:02d}: no 'solve' or 'solution' function found")
            continue

        test_file = os.path.join(TEST_DIR, f"{qid:02d}_test.txt")
        if not os.path.exists(test_file):
            print(f"\n[SKIP] Q{qid:02d}: no test file found")
            continue

        with open(test_file) as f:
            tests = []
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line: continue
                try:
                    import ast
                    t = ast.literal_eval(line)
                    tests.append(t)
                except:
                    pass

        passed = failed = skipped = 0
        failures = []
        name_w = max((len(t.get('name', f'case{i}')) for i,t in enumerate(tests)), default=10)

        print(f"\n{'='*72}")
        print(f"  Q{qid:02d} — {len(tests)} test cases")
        print(f"{'='*72}")

        for i, tc in enumerate(tests):
            name = tc.get('name', f'Case {i+1}')
            inp = tc.get('input')
            expected = tc.get('expected')

            try:
                if isinstance(inp, dict):
                    result = fn(**inp)
                elif isinstance(inp, list) and len(inp) == 0:
                    result = fn()
                else:
                    result = fn(inp) if not isinstance(inp, dict) else fn(**inp)
            except Exception as e:
                print(f"  [✗] {name:>{name_w}}  EXCEPTION: {e}")
                failures.append((i+1, name, str(e))); failed += 1; continue

            if result == expected:
                print(f"  [✓] {name:>{name_w}}  OK"); passed += 1
            else:
                reason = f"got={result}, expected={expected}"
                print(f"  [✗] {name:>{name_w}}  FAILED — {reason}"); failed += 1
                failures.append((i+1, name, reason))

        ok = failed == 0
        overall_pass = overall_pass and ok
        total_p += passed; total_f += failed; total_s += skipped
        status = "✅ PASSED" if ok else f"❌ {failed}/{len(tests)} FAILED"
        print(f"\n  Result: {status} ({passed} passed)")
        if failures:
            for cn, cname, creason in failures:
                print(f"    Case {cn} ({cname}): {creason}")

    print(f"\n{'#'*72}")
    print(f"  TOTAL: {total_p} passed, {total_f} failed")
    print(f"  {'✅ ALL PASSED!' if overall_pass else '❌ SOME FAILED'}")
    print(f"{'#'*72}\n")
    sys.exit(0 if overall_pass else 1)

if __name__ == '__main__':
    run_tests()
