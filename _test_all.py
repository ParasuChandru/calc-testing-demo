"""
Combined test: starts server, runs tests, stops server.
"""
import json
import urllib.request
import urllib.error
import signal
import sys
import time

# ---- Start server in child process ----
import os

pid = os.fork()
if pid == 0:
    # Child: start Flask server
    from app import app
    app.run(host="0.0.0.0", port=5001, debug=False)
else:
    # Parent: wait then test
    time.sleep(4)
    print(f"Server started as PID {pid}")

    BASE = "http://localhost:5001"
    all_pass = True

    def get(path):
        try:
            resp = urllib.request.urlopen(f"{BASE}{path}")
            return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                # Could be Flask HTML error page
                return e.code, {"error": body[:200]}
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
            body_text = e.read().decode()
            try:
                return e.code, json.loads(body_text)
            except json.JSONDecodeError:
                return e.code, {"error": body_text[:200]}
        except Exception as e:
            return None, str(e)

    def test(name, cond):
        s = "✅ PASS" if cond else "❌ FAIL"
        print(f"  {s}  {name}")
        return cond

    # Health
    print("\n🏥 Health Check:")
    code, data = get("/api/health")
    all_pass &= test("health endpoint exists", code == 200)
    all_pass &= test("status is healthy", data.get("status") == "healthy")

    # Endpoints
    code, data = get("/api/endpoints")
    all_pass &= test(f"endpoints list ({len(data.get('endpoints',[]))} found)", code == 200)

    # Arithmetic
    print("\n➕ Arithmetic:")
    code, d = get("/api/add?a=5&b=3")
    all_pass &= test("add 5+3=8", d.get("result") == 8)

    code, d = get("/api/subtract?a=10&b=4")
    all_pass &= test("subtract 10-4=6", d.get("result") == 6)

    code, d = get("/api/multiply?a=6&b=7")
    all_pass &= test("multiply 6*7=42", d.get("result") == 42)

    code, d = get("/api/divide?a=15&b=3")
    all_pass &= test("divide 15/3=5", d.get("result") == 5.0)

    code, d = get("/api/divide?a=10&b=0")
    is_error = code is not None and code >= 400
    is_json_error = code is not None and isinstance(d, dict) and "error" in d
    all_pass &= test("divide by zero → error response", is_error)
    all_pass &= test("divide by zero → JSON error message", is_json_error)

    # Advanced
    print("\n🔢 Advanced Operations:")
    code, d = get("/api/power?a=2&b=8")
    all_pass &= test("power 2^8=256", d.get("result") == 256)

    code, d = get("/api/factorial?n=10")
    all_pass &= test("factorial(10)=3628800", d.get("result") == 3628800)

    code, d = get("/api/is_palindrome?text=racecar")
    all_pass &= test("is_palindrome('racecar')=True", d.get("result") is True)

    code, d = get("/api/is_palindrome?text=hello")
    all_pass &= test("is_palindrome('hello')=False", d.get("result") is False)

    code, d = get("/api/fizz_buzz?n=5")
    all_pass &= test("fizz_buzz(5)[-1]='Buzz'", d.get("result")[-1] == "Buzz")

    # Unified API
    print("\n🔌 Unified API:")
    code, d = post("/api/calculate", {"operation": "add", "a": 7, "b": 8})
    all_pass &= test("POST add 7+8=15", d.get("result") == 15)

    code, d = post("/api/calculate", {"operation": "factorial", "n": 12})
    all_pass &= test("POST factorial(12)=479001600", d.get("result") == 479001600)

    # Dashboard
    print("\n🌐 Dashboard:")
    try:
        resp = urllib.request.urlopen(f"{BASE}/")
        html = resp.read().decode()
        all_pass &= test("dashboard page loads", "Calculator" in html)
        all_pass &= test("has 'Run All Tests'", "Run All Tests" in html)
        print(f"  ✅ PASS  dashboard: {len(html)} bytes")
    except Exception as e:
        print(f"  ❌ FAIL  dashboard: {e}")

    # Summary
    print(f"\n{'='*45}")
    if all_pass:
        print("🎉  ALL TESTS PASSED!  🎉")
    else:
        print("❌  SOME TESTS FAILED")
    print(f"{'='*45}\n")

    # Kill server
    os.kill(pid, signal.SIGTERM)
    os.waitpid(pid, 0)
    print("Server stopped.")
