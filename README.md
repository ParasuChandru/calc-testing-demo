# Calculator App — Multi-Framework Testing Demo

A simple calculator application tested with three different Python testing frameworks.

## Application

`calculator.py` contains a `Calculator` class with the following methods:

| Method | Description |
|---|---|
| `add(a, b)` | Returns the sum |
| `subtract(a, b)` | Returns the difference |
| `multiply(a, b)` | Returns the product |
| `divide(a, b)` | Returns the quotient |
| `power(base, exponent)` | Returns base raised to exponent |
| `factorial(n)` | Returns n! |
| `is_palindrome(text)` | Checks if text is a palindrome |
| `fizz_buzz(n)` | Returns FizzBuzz sequence up to n |

## Testing Frameworks

### 1. unittest (Python built-in)
```bash
python -m unittest test_calculator_unittest -v
```

### 2. pytest
```bash
pip install -r requirements.txt
python -m pytest test_calculator_pytest.py -v
```

### 3. doctest
```bash
python -m doctest test_calculator_doctest.py -v
```

## Project Structure

```
├── calculator.py          # Application code
├── test_calculator_unittest.py   # unittest framework tests
├── test_calculator_pytest.py     # pytest framework tests
├── test_calculator_doctest.py    # Doctest framework tests
├── requirements.txt           # Dependencies
└── README.md                  # This file
```
