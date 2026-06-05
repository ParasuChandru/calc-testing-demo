"""
Tests for Calculator using the pytest framework.
Includes parametric tests, fixtures, and exceptions testing.
"""

import pytest
from calculator import Calculator


# --------------- Fixtures ---------------

@pytest.fixture
def calc():
    """Provide a Calculator instance for all tests."""
    return Calculator()


# --------------- Parametric tests for add ---------------

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, -1, -2),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add_parametric(calc, a, b, expected):
    """Parametric tests for the add method."""
    assert calc.add(a, b) == expected


def test_add_floats(calc):
    """Float addition uses approx because of floating-point precision."""
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


# --------------- Parametric tests for subtract ---------------

@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (3, 5, -2),
    (10, 10, 0),
    (-5, -3, -2),
    (0, 5, -5),
])
def test_subtract_parametric(calc, a, b, expected):
    """Parametric tests for the subtract method."""
    assert calc.subtract(a, b) == expected


# --------------- Parametric tests for multiply ---------------

@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (0, 5, 0),
    (-3, -4, 12),
    (-3, 4, -12),
    (1, 1, 1),
])
def test_multiply_parametric(calc, a, b, expected):
    """Parametric tests for the multiply method."""
    assert calc.multiply(a, b) == expected


# --------------- Parametric tests for divide ---------------

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (7, 2, 3.5),
    (-10, -2, 5),
    (0, 5, 0),
])
def test_divide_parametric(calc, a, b, expected):
    """Parametric tests for the divide method."""
    assert calc.divide(a, b) == expected


def test_divide_by_zero_raises(calc):
    """Test that dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)


# --------------- Tests for power ---------------

def test_power_positive_integer(calc):
    assert calc.power(2, 3) == 8


def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == 1


def test_power_fractional_result(calc):
    assert calc.power(9, 0.5) == 3


def test_power_negative_base_non_integer_raises(calc):
    with pytest.raises(ValueError, match="Cannot raise a negative number"):
        calc.power(-2, 0.5)


# --------------- Tests for factorial ---------------

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (5, 120),
    (10, 3628800),
])
def test_factorial_parametric(calc, n, expected):
    """Parametric tests for factorial."""
    assert calc.factorial(n) == expected


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError, match="not defined for negative"):
        calc.factorial(-1)


def test_factorial_non_integer_raises(calc):
    with pytest.raises(TypeError, match="only defined for integers"):
        calc.factorial(3.5)


# --------------- Tests for is_palindrome ---------------

@pytest.mark.parametrize("text, expected", [
    ("racecar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("RaceCar", True),
    ("", True),
    ("a", True),
    ("Ab ba", True),
])
def test_is_palindrome_parametric(calc, text, expected):
    """Parametric tests for is_palindrome."""
    assert calc.is_palindrome(text) == expected


# --------------- Tests for fizz_buzz ---------------

def test_fizzbuzz_regular(calc):
    result = calc.fizz_buzz(15)
    expected = [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
        "11", "Fizz", "13", "14", "FizzBuzz"
    ]
    assert result == expected


def test_fizzbuzz_small(calc):
    result = calc.fizz_buzz(5)
    expected = ["1", "2", "Fizz", "4", "Buzz"]
    assert result == expected


def test_fizzbuzz_zero_raises(calc):
    with pytest.raises(ValueError, match="positive integer"):
        calc.fizz_buzz(0)


def test_fizzbuzz_negative_raises(calc):
    with pytest.raises(ValueError, match="positive integer"):
        calc.fizz_buzz(-1)


# --------------- Integration test ---------------

def test_calculator_workflow(calc):
    """Test a realistic workflow combining multiple operations."""
    a = calc.add(10, 5)       # 15
    b = calc.multiply(a, 2)   # 30
    c = calc.divide(b, 3)     # 10
    d = calc.subtract(c, 2)   # 8
    assert d == 8.0
