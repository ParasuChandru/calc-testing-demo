"""
Unit tests for Calculator using Python's built-in unittest framework.
"""

import unittest
from calculator import Calculator


class TestCalculatorAdd(unittest.TestCase):
    """Test cases for the add method."""

    def setUp(self):
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_add_floats(self):
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3)

    def test_add_zeros(self):
        self.assertEqual(self.calc.add(0, 0), 0)


class TestCalculatorSubtract(unittest.TestCase):
    """Test cases for the subtract method."""

    def setUp(self):
        self.calc = Calculator()

    def test_subtract_positive_numbers(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_subtract_negative_result(self):
        self.assertEqual(self.calc.subtract(3, 5), -2)

    def test_subtract_same_numbers(self):
        self.assertEqual(self.calc.subtract(5, 5), 0)


class TestCalculatorMultiply(unittest.TestCase):
    """Test cases for the multiply method."""

    def setUp(self):
        self.calc = Calculator()

    def test_multiply_positive_numbers(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calc.multiply(5, 0), 0)

    def test_multiply_negative_numbers(self):
        self.assertEqual(self.calc.multiply(-3, -4), 12)

    def test_multiply_mixed_signs(self):
        self.assertEqual(self.calc.multiply(-3, 4), -12)


class TestCalculatorDivide(unittest.TestCase):
    """Test cases for the divide method."""

    def setUp(self):
        self.calc = Calculator()

    def test_divide_positive_numbers(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_with_remainder(self):
        self.assertEqual(self.calc.divide(7, 2), 3.5)

    def test_divide_by_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        self.assertEqual(self.calc.divide(-10, -2), 5)


class TestCalculatorPower(unittest.TestCase):
    """Test cases for the power method."""

    def setUp(self):
        self.calc = Calculator()

    def test_power_positive_integer(self):
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_power_zero_exponent(self):
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_power_fractional_result(self):
        self.assertEqual(self.calc.power(9, 0.5), 3)

    def test_power_negative_base_non_integer_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.power(-2, 0.5)


class TestCalculatorFactorial(unittest.TestCase):
    """Test cases for the factorial method."""

    def setUp(self):
        self.calc = Calculator()

    def test_factorial_zero(self):
        self.assertEqual(self.calc.factorial(0), 1)

    def test_factorial_one(self):
        self.assertEqual(self.calc.factorial(1), 1)

    def test_factorial_positive(self):
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_non_integer_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.factorial(3.5)


class TestCalculatorIsPalindrome(unittest.TestCase):
    """Test cases for the is_palindrome method."""

    def setUp(self):
        self.calc = Calculator()

    def test_simple_palindrome(self):
        self.assertTrue(self.calc.is_palindrome("racecar"))

    def test_not_palindrome(self):
        self.assertFalse(self.calc.is_palindrome("hello"))

    def test_palindrome_with_spaces(self):
        self.assertTrue(self.calc.is_palindrome("A man a plan a canal Panama"))

    def test_palindrome_case_insensitive(self):
        self.assertTrue(self.calc.is_palindrome("RaceCar"))

    def test_empty_string(self):
        self.assertTrue(self.calc.is_palindrome(""))


class TestCalculatorFizzBuzz(unittest.TestCase):
    """Test cases for the fizz_buzz method."""

    def setUp(self):
        self.calc = Calculator()

    def test_fizzbuzz_regular(self):
        result = self.calc.fizz_buzz(15)
        self.assertEqual(result, [
            "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
            "11", "Fizz", "13", "14", "FizzBuzz"
        ])

    def test_fizzbuzz_small(self):
        result = self.calc.fizz_buzz(5)
        self.assertEqual(result, ["1", "2", "Fizz", "4", "Buzz"])

    def test_fizzbuzz_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.fizz_buzz(0)

    def test_fizzbuzz_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.fizz_buzz(-1)


if __name__ == "__main__":
    unittest.main()
