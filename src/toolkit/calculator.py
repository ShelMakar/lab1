from .constants import OPERATORS, PRIORITY


def corr_exp(expression):
    for i in range(len(expression)):
        if (not expression[i].isdigit()) and (expression[i] not in "()*-+%/. "):
            raise ValueError("некорректный символ")
    return 1


def tokenization(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
            continue

        if expression[i] == "/":
            if i != len(expression) - 1:
                if expression[i + 1] == "/":
                    tokens.append(expression[i : i + 2])
                    i += 1
                else:
                    tokens.append(expression[i])
        elif expression[i] in "()*-+%":
            tokens.append(expression[i])
        else:
            tok = ""
            for j in range(i, len(expression)):
                if expression[j].isdigit():
                    tok += expression[j]
                    continue
                if expression[j] == ".":
                    if (
                        (len(expression) - 1 > j)
                        and (expression[j + 1].isdigit())
                        and (expression[j - 1].isdigit())
                        and "." not in tok
                    ):
                        tok += expression[j]
                    else:
                        raise ValueError("некорректный выражение")
                if expression[j] in "()*-+%/":
                    tokens.append(tok)
                    i = j - 1
                    break
            else:
                i = j
                tokens.append(tok)
        i += 1
    return tokens


def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def validation(tokens):
    if not tokens:
        raise ValueError("пустое выражение")
    skobki = 0
    need_operand = True
    unary = False
    for token in tokens:
        if is_number(token):
            if not need_operand:
                raise ValueError("между операндами отсутствует оператор")
            need_operand = False
            unary = False
            continue
        if token == "(":
            if not need_operand:
                raise ValueError("перед '(' должен быть оператор")
            skobki += 1
            need_operand = True
            unary = False
            continue
        if token == ")":
            if skobki == 0:
                raise ValueError("лишняя закрывающая скобка")
            if need_operand:
                raise ValueError("перед ')' должен быть операнд")
            skobki -= 1
            need_operand = False
            continue
        if token in ("+", "-"):
            if need_operand:
                if unary:
                    raise ValueError("два унарных оператора подряд")
                unary = True
                continue
            need_operand = True
            unary = False
            continue
        if token in ("*", "/", "//", "%"):
            if need_operand:
                raise ValueError("оператор стоит без операнда")
            need_operand = True
            unary = False
            continue
        raise ValueError("некорректный токен")
    if skobki != 0:
        raise ValueError("неправильное количество скобок")
    if need_operand:
        raise ValueError("выражение заканчивается оператором")
    return True


def prepare_unary(tokens):
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ("+", "-") and (
            i == 0 or tokens[i - 1] in ("(", "+", "-", "*", "/", "//", "%")
        ):
            if i + 1 >= len(tokens):
                raise ValueError("после унарного оператора нет числа")
            next_token = tokens[i + 1]
            if not is_number(next_token):
                raise ValueError("унарный оператор должен стоять перед числом")
            if token == "-":
                result.append("-" + next_token)
            else:
                result.append(next_token)
            i += 2
            continue
        result.append(token)
        i += 1
    return result


def dijkstra(tokens):
    output = []
    stack = []
    for token in tokens:
        if is_number(token):
            output.append(token)
            continue
        if token == "(":
            stack.append(token)
            continue
        if token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("лишняя закрывающая скобка")
            stack.pop()
            continue
        if token in PRIORITY:
            while stack and stack[-1] != "(" and PRIORITY[stack[-1]] >= PRIORITY[token]:
                output.append(stack.pop())
            stack.append(token)
            continue
        raise ValueError("неизвестный токен")
    while stack:
        if stack[-1] == "(":
            raise ValueError("не хватает закрывающей скобки")
        output.append(stack.pop())
    return output


def calculate_rpn(rpn):
    values = []
    for token in rpn:
        if is_number(token):
            values.append(float(token))
            continue
        if token not in OPERATORS:
            raise ValueError(f"Неизвестный оператор: {token}")
        if len(values) < 2:
            raise ValueError(f"Недостаточно аргументов для {token!r}")
        right = values.pop()
        left = values.pop()
        if token in ("/", "//", "%") and right == 0:
            raise ZeroDivisionError("Деление на ноль")
        values.append(float(OPERATORS[token](left, right)))
    if len(values) != 1:
        raise ValueError("Не удалось получить единственный результат")
    return values[0]


def calculate(expression):
    corr_exp(expression)
    tokens = tokenization(expression)
    validation(tokens)
    tokens = prepare_unary(tokens)
    rpn = dijkstra(tokens)
    return calculate_rpn(rpn)
