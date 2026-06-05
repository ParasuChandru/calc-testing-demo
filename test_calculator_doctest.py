"""
Doctests for Calculator.

These doctests are embedded in the docstrings of the Calculator class methods.
Run with: python -m doctest calculator.py -v

Examples of usage in docstrings:

    >>> from calculator import Calculator
    >>> calc = Calculator()

Addition:

    >>> calc.add(2, 3)
    5
    >>> calc.add(-1, 1)
    0
    >>> round(calc.add(0.1, 0.2), 1)
    0.3

Subtraction:

    >>> calc.subtract(5, 3)
    2
    >>> calc.subtract(3, 5)
    -2

Multiplication:

    >>> calc.multiply(3, 4)
    12
    >>> calc.multiply(-3, 4)
    -12

Division:

    >>> calc.divide(10, 2)
    5.0
    >>> calc.divide(7, 2)
    3.5

Power:

    >>> calc.power(2, 3)
    8
    >>> calc.power(9, 0.5)
    3.0

Factorial:

    >>> calc.factorial(5)
    120
    >>> calc.factorial(0)
    1

Is Palindrome:

    >>> calc.is_palindrome("racecar")
    True
    >>> calc.is_palindrome("hello")
    False
    >>> calc.is_palindrome("A man a plan a canal Panama")
    True

FizzBuzz:

    >>> calc.fizz_buzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    >>> calc.fizz_buzz(15)[-1]
    'FizzBuzz'
"""

import doctest
from calculator import Calculator

if __name__ == "__main__":
    # Run doctests on the calculator module
    results = doctest.testmod(m=globals(), verbose=True)
    print(f"\nTests: {results.attempted}, Failures: {results.failed}")
