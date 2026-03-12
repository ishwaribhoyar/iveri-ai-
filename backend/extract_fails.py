"""Run tests and save to file."""
import subprocess
r = subprocess.run(["python", "test_api.py"], capture_output=True, text=True, cwd=".")
with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write(r.stdout)
print("Done. Results saved.")
# Quick summary
lines = r.stdout.splitlines()
passes = sum(1 for l in lines if "PASS |" in l)
fails = sum(1 for l in lines if "FAIL |" in l)
print(f"{passes} PASSED / {fails} FAILED / {passes+fails} TOTAL")
for l in lines:
    if "FAIL |" in l:
        print("  " + l.strip())
