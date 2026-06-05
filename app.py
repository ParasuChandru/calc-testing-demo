"""
Flask REST API server for the Calculator app with live test runner.

Run with:  python app.py
Access at: http://localhost:5000
"""

import json
import os
import time
import traceback
from datetime import datetime

from flask import Flask, jsonify, request, render_template

from calculator import Calculator

app = Flask(__name__)

# --------------- Calculator API Endpoints ---------------


@app.route("/api/add", methods=["POST", "GET"])
def api_add():
    """Add two numbers."""
    a, b = _get_numbers()
    result = Calculator().add(a, b)
    return jsonify({"operation": "add", "a": a, "b": b, "result": result})


@app.route("/api/subtract", methods=["POST", "GET"])
def api_subtract():
    """Subtract two numbers."""
    a, b = _get_numbers()
    result = Calculator().subtract(a, b)
    return jsonify({"operation": "subtract", "a": a, "b": b, "result": result})


@app.route("/api/multiply", methods=["POST", "GET"])
def api_multiply():
    """Multiply two numbers."""
    a, b = _get_numbers()
    result = Calculator().multiply(a, b)
    return jsonify({"operation": "multiply", "a": a, "b": b, "result": result})


@app.route("/api/divide", methods=["POST", "GET"])
def api_divide():
    """Divide two numbers."""
    a, b = _get_numbers()
    try:
        result = Calculator().divide(a, b)
        return jsonify({"operation": "divide", "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"operation": "divide", "error": str(e)}), 400


@app.route("/api/power", methods=["POST", "GET"])
def api_power():
    """Raise base to exponent."""
    a, b = _get_numbers()
    try:
        result = Calculator().power(a, b)
        return jsonify({"operation": "power", "base": a, "exponent": b, "result": result})
    except ValueError as e:
        return jsonify({"operation": "power", "error": str(e)}), 400


@app.route("/api/factorial", methods=["POST", "GET"])
def api_factorial():
    """Compute factorial."""
    n = _get_number("n")
    try:
        result = Calculator().factorial(n)
        return jsonify({"operation": "factorial", "n": n, "result": result})
    except (ValueError, TypeError) as e:
        return jsonify({"operation": "factorial", "error": str(e)}), 400


@app.route("/api/is_palindrome", methods=["POST", "GET"])
def api_is_palindrome():
    """Check if string is palindrome."""
    text = request.args.get("text") or (request.json or {}).get("text", "")
    result = Calculator().is_palindrome(text)
    return jsonify({"operation": "is_palindrome", "text": text, "result": result})


@app.route("/api/fizz_buzz", methods=["POST", "GET"])
def api_fizz_buzz():
    """Generate FizzBuzz sequence."""
    n = _get_number("n")
    try:
        result = Calculator().fizz_buzz(n)
        return jsonify({"operation": "fizz_buzz", "n": n, "result": result})
    except ValueError as e:
        return jsonify({"operation": "fizz_buzz", "error": str(e)}), 400


# --------------- Unified Calculator Endpoint ---------------


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """Unified endpoint: POST with JSON body.

    Body example:
    {
        "operation": "add",
        "a": 5,
        "b": 3
    }

    Valid operations: add, subtract, multiply, divide, power, factorial, is_palindrome, fizz_buzz
    """
    data = request.json
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    operation = data.get("operation", "").lower()
    calc = Calculator()

    operations = {
        "add": lambda d: (d["a"], d["b"]),
        "subtract": lambda d: (d["a"], d["b"]),
        "multiply": lambda d: (d["a"], d["b"]),
        "divide": lambda d: (d["a"], d["b"]),
        "power": lambda d: (d["base"], d["exponent"]),
    }

    try:
        if operation in operations:
            a, b = operations[operation](data)
            result = getattr(calc, operation)(a, b)
            return jsonify({"operation": operation, "result": result})

        elif operation == "factorial":
            result = calc.factorial(data["n"])
            return jsonify({"operation": "factorial", "result": result})

        elif operation == "is_palindrome":
            result = calc.is_palindrome(data["text"])
            return jsonify({"operation": "is_palindrome", "result": result})

        elif operation == "fizz_buzz":
            result = calc.fizz_buzz(data["n"])
            return jsonify({"operation": "fizz_buzz", "result": result})

        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --------------- Health & Info ---------------


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})


@app.errorhandler(ValueError)
def handle_value_error(e):
    """Return JSON error for ValueError."""
    return jsonify({"error": str(e)}), 400


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON error for unhandled exceptions."""
    return jsonify({"error": str(e)}), 500


@app.route("/api/endpoints", methods=["GET"])
def endpoints():
    """List all available API endpoints."""
    return jsonify({
        "endpoints": [
            {"method": "POST/GET", "path": "/api/add", "description": "Add two numbers"},
            {"method": "POST/GET", "path": "/api/subtract", "description": "Subtract two numbers"},
            {"method": "POST/GET", "path": "/api/multiply", "description": "Multiply two numbers"},
            {"method": "POST/GET", "path": "/api/divide", "description": "Divide two numbers"},
            {"method": "POST/GET", "path": "/api/power", "description": "Power operation"},
            {"method": "POST/GET", "path": "/api/factorial", "description": "Compute factorial"},
            {"method": "POST/GET", "path": "/api/is_palindrome", "description": "Check palindrome"},
            {"method": "POST/GET", "path": "/api/fizz_buzz", "description": "FizzBuzz sequence"},
            {"method": "POST", "path": "/api/calculate", "description": "Unified calculator"},
            {"method": "GET", "path": "/api/health", "description": "Health check"},
            {"method": "GET", "path": "/api/endpoints", "description": "List endpoints"},
        ]
    })


# --------------- Live Test Runner API ---------------


@app.route("/api/run-tests", methods=["POST"])
def run_tests():
    """Run the automated test suite and return results."""
    test_data = request.json or {}
    selected_frameworks = test_data.get("frameworks", ["all"])
    start_time = time.time()

    results = {
        "frameworks": {},
        "total_tests": 0,
        "total_passed": 0,
        "total_failed": 0,
        "total_errors": 0,
        "duration_seconds": 0,
    }

    # ---- unittest tests ----
    if selected_frameworks in ("all", ["all"], "unittest", ["unittest"]):
        unittest_result = _run_unittest_tests()
        results["frameworks"]["unittest"] = unittest_result
        results["total_tests"] += unittest_result["total"]
        results["total_passed"] += unittest_result["passed"]
        results["total_failed"] += unittest_result["failed"]
        results["total_errors"] += unittest_result["errors"]

    # ---- pytest tests ----
    if selected_frameworks in ("all", ["all"], "pytest", ["pytest"]):
        pytest_result = _run_pytest_tests()
        results["frameworks"]["pytest"] = pytest_result
        results["total_tests"] += pytest_result["total"]
        results["total_passed"] += pytest_result["passed"]
        results["total_failed"] += pytest_result["failed"]
        results["total_errors"] += pytest_result["errors"]

    # ---- Doctest ----
    if selected_frameworks in ("all", ["all"], "doctest", ["doctest"]):
        doctest_result = _run_doctest_tests()
        results["frameworks"]["doctest"] = doctest_result
        results["total_tests"] += doctest_result["total"]
        results["total_passed"] += doctest_result["passed"]
        results["total_failed"] += doctest_result["failed"]
        results["total_errors"] += doctest_result["errors"]

    # ---- Functional smoke tests (independent of framework) ----
    if selected_frameworks in ("all", ["all"], "functional", ["functional"]):
        functional_result = _run_functional_tests()
        results["frameworks"]["functional"] = functional_result
        results["total_tests"] += functional_result["total"]
        results["total_passed"] += functional_result["passed"]
        results["total_failed"] += functional_result["failed"]
        results["total_errors"] += functional_result["errors"]

    results["duration_seconds"] = round(time.time() - start_time, 3)
    return jsonify(results)


def _run_unittest_tests():
    import unittest

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover test files
    try:
        suite.addTests(loader.discover(".", pattern="test_calculator_unittest.py"))
    except Exception:
        pass

    runner = unittest.TextTestRunner(stream=_StringIO())
    result = runner.run(suite)
    return {
        "framework": "unittest",
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "total": result.testsRun,
        "failures": [str(f[1]) for f in result.failures],
        "errors": [str(e[1]) for e in result.errors],
    }


def _run_pytest_tests():
    import pytest
    import io
    import contextlib

    f = io.StringIO()
    with contextlib.redirect_stderr(f), contextlib.redirect_stdout(f):
        result = pytest.main(["-v", "--tb=short", "test_calculator_pytest.py"])

    output = f.getvalue()
    return {
        "framework": "pytest",
        "passed": _count_passed(output),
        "failed": _count_failed(output),
        "errors": _count_errors(output),
        "total": _count_passed(output) + _count_failed(output) + _count_errors(output),
        "output": output[-2000:],  # last 2000 chars
        "exit_code": result,
    }


def _run_doctest_tests():
    import doctest
    import calculator

    result = doctest.testmod(m=calculator, verbose=False)
    return {
        "framework": "doctest",
        "passed": result.attempted - result.failed,
        "failed": result.failed,
        "errors": 0,
        "total": result.attempted,
        "output": f"Tests attempted: {result.attempted}, Failures: {result.failed}",
    }


def _run_functional_tests():
    """Run quick functional smoke tests directly (no framework dependency)."""
    calc = Calculator()
    tests = []
    failures = []

    tests.append(("add positive", calc.add(2, 3) == 5))
    tests.append(("add negative", calc.add(-1, -1) == -2))
    tests.append(("subtract", calc.subtract(5, 3) == 2))
    tests.append(("multiply", calc.multiply(3, 4) == 12))
    tests.append(("divide", calc.divide(10, 2) == 5.0))
    tests.append(("divide by zero", True))  # handled separately
    tests.append(("power", calc.power(2, 3) == 8))
    tests.append(("factorial", calc.factorial(5) == 120))
    tests.append(("palindrome", calc.is_palindrome("racecar") is True))
    tests.append(("not palindrome", calc.is_palindrome("hello") is False))
    tests.append(("fizz_buzz", calc.fizz_buzz(15)[-1] == "FizzBuzz"))

    # Test divide by zero
    try:
        calc.divide(1, 0)
    except ValueError:
        tests.append(("divide by zero raises", True))
    else:
        tests.append(("divide by zero raises", False))

    passed = sum(1 for _, ok in tests if ok)
    failed = sum(1 for _, ok in tests if not ok)

    for name, ok in tests:
        if not ok:
            failures.append(f"Failed: {name}")

    return {
        "framework": "functional",
        "passed": passed,
        "failed": failed,
        "errors": 0,
        "total": len(tests),
        "failures": failures,
    }


# --------------- Helpers ---------------


class _StringIO:
    """Minimal StringIO substitute for unittest runner."""

    def write(self, s):
        pass

    def flush(self):
        pass


def _get_numbers():
    """Extract two numbers from request args or JSON body."""
    a = request.args.get("a") or (request.json or {}).get("a")
    b = request.args.get("b") or (request.json or {}).get("b")
    if a is None or b is None:
        return jsonify({"error": "Both 'a' and 'b' parameters are required"}), 400
    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({"error": "Parameters must be numbers"}), 400
    return a, b


def _get_number(param="n"):
    """Extract a single number from request args or JSON body."""
    n = request.args.get(param) or (request.json or {}).get(param)
    if n is None:
        return jsonify({"error": f"Parameter '{param}' is required"}), 400
    try:
        n = int(n)
    except (ValueError, TypeError):
        return jsonify({"error": f"'{param}' must be a number"}), 400
    return n


def _count_passed(output):
    return output.count(" PASSED") + len([l for l in output.splitlines() if "passed" in l.lower() and "failed" not in l.lower()])


def _count_failed(output):
    lines = [l for l in output.splitlines() if "FAILED" in l and "PASSED" not in l]
    return len(lines)


def _count_errors(output):
    return output.count("ERROR")


# --------------- Web Dashboard ---------------


@app.route("/")
def dashboard():
    """Live testing dashboard."""
    return render_template("dashboard.html")


# --------------- Entry Point ---------------


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
