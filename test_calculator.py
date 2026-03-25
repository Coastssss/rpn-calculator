import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_simple_addition(self):
        self.assertEqual(self.calc.calculate("2 + 2"), 4)

    def test_simple_subtraction(self):
        self.assertEqual(self.calc.calculate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertEqual(self.calc.calculate("3 * 4"), 12)

    def test_division(self):
        self.assertEqual(self.calc.calculate("10 / 2"), 5)

    def test_power_operator(self):
        # Уровень приоритета 3
        self.assertEqual(self.calc.calculate("2 ^ 3"), 8)

    def test_precedence_level_1_vs_2(self):
        # 2 + 2 * 2 должно быть 6, а не 8
        self.assertEqual(self.calc.calculate("2 + 2 * 2"), 6)

    def test_precedence_level_2_vs_3(self):
        # 2 * 3 ^ 2 должно быть 18 (2 * 9), а не 36 ((2*3)^2)
        self.assertEqual(self.calc.calculate("2 * 3 ^ 2"), 18)

    def test_parentheses_override(self):  # проверка на скобки
        # (2 + 2) * 2 должно быть 8
        self.assertEqual(self.calc.calculate("(2 + 2) * 2"), 8)

    def test_complex_expression(self):
        # 2 + (3 * 4) ^ 2 / 2 - 1
        # 2 + 144 / 2 - 1 -> 2 + 72 - 1 -> 73
        self.assertEqual(self.calc.calculate("2 + (3 * 4) ^ 2 / 2 - 1"), 73)

    def test_rpn_conversion_simple(self):
        # проверка шага преобразования
        tokens = self.calc.tokenize("1 + 2")
        rpn = self.calc.to_rpn(tokens)
        self.assertEqual(rpn, ['1', '2', '+'])

    def test_rpn_conversion_precedence(self):
        tokens = self.calc.tokenize("1 + 2 * 3")
        rpn = self.calc.to_rpn(tokens)
        # ожидаем 1 2 3 * +
        self.assertEqual(rpn, ['1', '2', '3', '*', '+'])

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("(2 + 2")


if __name__ == '__main__':
    unittest.main()
