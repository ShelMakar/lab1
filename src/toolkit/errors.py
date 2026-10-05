class ToolkitError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)


class EmptyExpressionError(ToolkitError):
    """Пустое выражение"""


class AbsZeroError(ToolkitError):
    """Температура ниже абсолютного нуля"""


class DivisionZeroError(ToolkitError):
    """Деление на ноль"""


class IncorrectSymbolError(ToolkitError):
    """Некорректный символ"""


class MissedOperandError(ToolkitError):
    """Пропущен операнд"""


class UnknownEdError(ToolkitError):
    """Неизвестная единица"""


class UnusableEdError(ToolkitError):
    """Несовместимые единицы"""


class IncorrectValueError(ToolkitError):
    """Некорректное числовое значение"""


class UncorrectExpression(ToolkitError):
    """Некорректное вфражение"""
