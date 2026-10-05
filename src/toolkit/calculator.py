from .constants import OPERATORS, PRIORITY
from .errors import (
    IncorrectSymbolError,
    EmptyExpressionError,
    UncorrectExpression,
    DivisionZeroError,
)


def corr_exp(expression: str) -> bool:
    """
    Проверяет выражение на наличие недопустимых символов

    Args:
        expression: Арифметическое выражение в виде строки

    Returns:
        True, если все символы выражения допустимы

    Raises:
        IncorrectSymbolError: Если выражение содержит недопустимый символ
    """
    for symbol in expression:
        if not symbol.isdigit() and symbol not in "()*-+%/. ":
            raise IncorrectSymbolError(f"Некорректный символ: {symbol}")

    return True


def tokenization(expression: str) -> list[str]:
    """
    Разбивает арифметическое выражение на отдельные токены

    Args:
        expression: Арифметическое выражение в виде строки

    Returns:
        Список токенов выражения

    Raises:
        UncorrectExpression: Если выражение содержит некорректное число
    """
    tokens = []
    i = 0

    while i < len(expression):
        symbol = expression[i]

        if symbol.isspace():
            i += 1
            continue

        if symbol == "/":
            if i + 1 < len(expression) and expression[i + 1] == "/":
                tokens.append("//")
                i += 2
            else:
                tokens.append("/")
                i += 1
            continue

        if symbol in "()*-+%":
            tokens.append(symbol)
            i += 1
            continue

        if symbol.isdigit() or symbol == ".":
            number = ""
            dots = 0

            while i < len(expression):
                symbol = expression[i]

                if symbol.isdigit():
                    number += symbol
                    i += 1
                    continue

                if symbol == ".":
                    dots += 1

                    if dots > 1:
                        raise UncorrectExpression("Некорректное число")

                    number += symbol
                    i += 1
                    continue

                break

            if number == "." or number[0] == "." or number[-1] == ".":
                raise UncorrectExpression(f"Некорректное число: {number}")

            tokens.append(number)

    return tokens


def validation(tokens: list[str]) -> bool:
    """
    Проверяет корректность структуры арифметического выражения

    Унарные операторы ``+`` и ``-`` разрешены только непосредственно
    перед числом. Проверяются последовательность операндов и операторов,
    расположение скобок и наличие парных скобок

    Args:
        tokens: Список токенов арифметического выражения

    Returns:
        True, если структура выражения корректна

    Raises:
        EmptyExpressionError: Если выражение пустое
        UncorrectExpression: Если структура выражения некорректна
    """
    if not tokens:
        raise EmptyExpressionError("Пустое выражение")

    skobki = 0
    need_operand = True
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Число
        if token not in PRIORITY:
            if not need_operand:
                raise UncorrectExpression("Между операндами отсутствует оператор")

            need_operand = False
            i += 1
            continue

        # Открывающая скобка
        if token == "(":
            if not need_operand:
                raise UncorrectExpression("Перед '(' должен быть оператор")

            skobki += 1
            need_operand = True
            i += 1
            continue

        # Закрывающая скобка
        if token == ")":
            if skobki == 0:
                raise UncorrectExpression("Лишняя закрывающая скобка")

            if need_operand:
                raise UncorrectExpression("Перед ')' должен быть операнд")

            skobki -= 1
            need_operand = False
            i += 1
            continue

        # Плюс или минус
        if token in ("+", "-"):
            # Если ожидается операнд, + или - является унарным.
            if need_operand:
                if i + 1 >= len(tokens):
                    raise UncorrectExpression(
                        "После унарного оператора должен быть операнд"
                    )

                # Унарный оператор может стоять
                # только непосредственно перед числом.
                if tokens[i + 1] in PRIORITY:
                    raise UncorrectExpression(
                        "Унарный оператор должен стоять перед числом"
                    )

                i += 1
                continue

            # В противном случае это бинарный оператор.
            need_operand = True
            i += 1
            continue

        # Бинарные *, /, //, %
        if token in ("*", "/", "//", "%"):
            if need_operand:
                raise UncorrectExpression("Оператор стоит без операнда")

            need_operand = True
            i += 1
            continue

        raise UncorrectExpression(f"Некорректный токен: {token}")

    if skobki != 0:
        raise UncorrectExpression("Неправильное количество скобок")

    if need_operand:
        raise UncorrectExpression("Выражение заканчивается оператором")

    return True


def prepare_unary(tokens: list[str]) -> list[str]:
    """
    Заменяет унарные операторы ``+`` и ``-`` на знаки чисел
    Args:
        tokens: Список токенов арифметического выражения

    Returns:
        Список токенов с обработанными унарными операторами
    """
    result = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token in ("+", "-") and (
            i == 0
            or tokens[i - 1]
            in (
                "(",
                "+",
                "-",
                "*",
                "/",
                "//",
                "%",
            )
        ):
            next_token = tokens[i + 1]

            if token == "-":
                result.append("-" + next_token)
            else:
                result.append(next_token)

            i += 2
            continue

        result.append(token)
        i += 1

    return result


def dijkstra(tokens: list[str]) -> list[str]:
    """
    Переводит инфиксную запись выражения в постфиксную (польскую)

    Для преобразования используется алгоритм сортировочной станции
    Дейкстры

    Args:
        tokens: Список токенов инфиксного выражения

    Returns:
        Список токенов, в постфиксной записи
    """
    output = []
    stack = []

    for token in tokens:

        # Открывающая скобка
        if token == "(":
            stack.append(token)
            continue

        # Закрывающая скобка
        if token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())

            stack.pop()
            continue

        # Число
        if token not in PRIORITY:
            output.append(token)
            continue

        # Оператор
        if token in PRIORITY:
            while stack and stack[-1] != "(" and PRIORITY[stack[-1]] >= PRIORITY[token]:
                output.append(stack.pop())

            stack.append(token)
            continue

    # Выгружаем оставшиеся операторы
    while stack:
        output.append(stack.pop())

    return output


def calculate_rpn(rpn: list[str]) -> float:
    """
    Вычисляет выражение, представленное в постфиксной записи.

    Args:
        rpn: Список токенов выражения в постфиксной записи.

    Returns:
        Результат вычисления выражения в виде числа float

    Raises:
        UncorrectExpression: Если для выполнения операции недостаточно аргументов
            или после вычисления получен некорректный стек значений
        DivisionZeroError: Если выполняется деление, целочисленное
            деление или остаток от деления на ноль
    """
    values = []

    for token in rpn:
        # Число
        if token not in PRIORITY:
            values.append(float(token))
            continue

        if len(values) < 2:
            raise UncorrectExpression("Недостаточно аргументов")

        right = values.pop()
        left = values.pop()

        if token in ("/", "//", "%") and right == 0:
            raise DivisionZeroError("Деление на ноль")

        result = OPERATORS[token](left, right)
        values.append(float(result))

    if len(values) != 1:
        raise UncorrectExpression("Не удалось получить единственный результат")

    return values[0]


def calculate(expression: str) -> float:
    """
    Последовательно выполняет все стадии обработки выражения и выводит результат

    Args:
        expression: Арифметическое выражение в виде строки

    Returns:
        Результат вычисления выражения

    Raises:
        все предыдущие (уже отработаны)
    """
    corr_exp(expression)
    tokens = tokenization(expression)
    validation(tokens)
    tokens = prepare_unary(tokens)
    rpn = dijkstra(tokens)
    return calculate_rpn(rpn)
