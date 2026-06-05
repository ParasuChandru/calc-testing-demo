#!/usr/bin/env python3
"""Test the Flask app endpoints."""
import json
import urllib.request
import urllib.error

BASE = "http://localhost:5001"

def get(path):
    try:
        resp = urllib.request.urlopen(f"{BASE}{path}")
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
    except Exception as e:
        return None, str(e)

def post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
    except Exception as e:
        return None, str(e)

def test(name, condition):
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"  {status}  {name}")
    return condition

all_pass = True

# 1. Health check
print("\n🏥 Health Check:")
code, data = get("/api/health")
all_pass &= test("health endpoint exists", code == 200)
all_pass &= test("status is healthy", data.get("status") == "healthy")

# 2. Endpoints list
code, data = get("/api/endpoints")
all_pass &= test("endpoints list exists", code == 200)
count = len(data.get("endpoints", []))
all_pass &= test(f"found {count} endpoints", count >= 9)

# 3. Add
code, data = get("/api/add?a=5&b=3")
all_pass &= test("add 5+3=8", data.get("result") == 8)

# 4. Subtract
code, data = get("/api/subtract?a=10&b=4")
all_pass &= test("subtract 10-4=6", data.get("result") == 6)

# 5. Multiply
code, data = get("/api/multiply?a=6&b=7")
all_pass &= test("multiply 6*7=42", data.get("result") == 42)

# 6. Divide
code, data = get("/api/divide?a=15&b=3")
all_pass &= test("divide 15/3=5", data.get("result") == 5.0)

# 7. Divide by zero
code, data = get("/api/divide?a=10&b=0")
all_pass &= test("divide by zero returns 400", code == 400)
all_pass &= test("divide by zero has error msg", "zero" in str(data).lower())

# 8. Power
code, data = get("/api/power?a=2&b=8")
all_pass &= test("power 2^8=256", data.get("result") == 256)

# 9. Factorial
code, data = get("/api/factorial?n=10")
all_pass &= test("factorial(10)=3628800", data.get("result") == 3628800)

# 10. Is Palindrome
code, data = get("/api/is_palindrome?text=racecar")
all_pass &= test("is_palindrome('racecar')=true", data.get("result") is True)

# 11. FizzBuzz
code, data = get("/api/fizz_buzz?n=5")
all_pass &= test("fizz_buzz(5) ends with Buzz", data.get("result")[-1] == "Buzz")

# 12. Unified API
code, data = post("/api/calculate", {"operation": "add", "a": 7, "b": 8})
all_pass &= test("unified add 7+8=15", data.get("result") == 15)

# 13. Dashboard loads
try:
    import urllib.request as ur
    resp = ur.urlopen(f"{BASE}/")
    html = resp.read().decode()
    all_pass &= test("dashboard page loads", "Calculator" in html)
    all_pass &= test("dashboard has test button", "Run All Tests" in html)
    print(f"  ✅ PASS  dashboard size: {len(html)} bytes")
except Exception as e:
    print(f"  ❌ FAIL  dashboard: {e}")

print(f"\n{'='*40}")
print(f"{'ALL TESTS PASSED! ✅' if all_pass else 'SOME TESTS FAILED ❌'}")
print(f"{'='*40}\n")
