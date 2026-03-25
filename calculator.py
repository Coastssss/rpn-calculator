import operator


class Calculator:
    def __init__(self):
        # 3 уровня приоритета:
        # 3: ^ (возведение в степень)
        # 2: *, /
        # 1: +, -
        self.precedence = {
            '^': 3,
            '*': 2,
            '/': 2,
            '+': 1,
            '-': 1
        }
        self.operators = set(self.precedence.keys())

    def tokenize(self, expression):
        """Разбивает строку на токены (числа и операторы)."""
        tokens = []
        number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                number += char
            elif char in self.operators or char in '()':
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(char)
            elif char.isspace():
                if number:
                    tokens.append(number)
                    number = ""
            else:
                raise ValueError(f"Недопустимый символ: {char}")
        if number:
            tokens.append(number)
        return tokens

    def to_rpn(self, tokens):
        """Преобразует токены в Обратную Польскую Нотацию (ОПН)."""
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self.operators:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Несбалансированные скобки")
                operator_stack.pop()  # Удаляем '('

        while operator_stack:
            top = operator_stack.pop()
            if top == '(':
                raise ValueError("Несбалансированные скобки")
            output_queue.append(top)

        return output_queue

    def _is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def eval_rpn(self, rpn_tokens):
        """Вычисляет результат из ОПН."""
        stack = []
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow
        }

        for token in rpn_tokens:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Некорректное выражение")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = ops[token](a, b)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]

    def calculate(self, expression):  # Лишние пробелы вокруг параметров
        result = 1+2  # Нет пробелов вокруг операторов
        unused_var = 42  # Неиспользуемая переменная
        return int(result) if result.is_integer() else result