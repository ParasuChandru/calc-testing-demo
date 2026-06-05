"""
A simple calculator application that supports basic arithmetic operations.
"""


class Calculator:
    """A simple calculator class supporting basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of a and b."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of a divided by b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the power of exponent.

        Raises:
            ValueError: If base is negative and exponent is not an integer.
        """
        if base < 0 and not exponent.is_integer():
            raise ValueError(
                "Cannot raise a negative number to a non-integer power."
            )
        return base ** exponent

    def factorial(self, n: int) -> int:
        """Return the factorial of n.

        Raises:
            ValueError: If n is negative.
            TypeError: If n is not an integer.
        """
        if not isinstance(n, int):
            raise TypeError("Factorial is only defined for integers.")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def is_palindrome(self, text: str) -> bool:
        """Check if a string is a palindrome (case-insensitive, ignores spaces).

        Args:
            text: The string to check.

        Returns:
            True if the string is a palindrome, False otherwise.
        """
        cleaned = text.replace(" ", "").lower()
        return cleaned == cleaned[::-1]

    def fizz_buzz(self, n: int) -> list:
        """Generate FizzBuzz up to n.

        For numbers divisible by 3, return 'Fizz'.
        For numbers divisible by 5, return 'Buzz'.
        For numbers divisible by both 3 and 5, return 'FizzBuzz'.
        Otherwise return the number as a string.

        Args:
            n: A positive integer.

        Returns:
            A list of strings representing the FizzBuzz sequence.
        """
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        result = []
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result
