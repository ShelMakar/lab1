from toolkit.constants import LENGTH, MASS, TEMPERATURE, TIME
from toolkit.errors import (
    AbsZeroError,
    IncorrectValueError,
    UnknownEdError,
    UnusableEdError,
)


def type_const(unit: str) -> str:
    """
    Определяет тип единицы измерения

    Args:
        unit: Обозначение единицы измерения.

    Returns:
        Тип единицы измерения

    Raises:
        UnknownEdError: Если единица измерения неизвестна
    """
    unit = unit.lower()

    if unit in LENGTH:
        return "length"

    if unit in MASS:
        return "mass"

    if unit in TIME:
        return "time"

    if unit in TEMPERATURE:
        return "temperature"

    raise UnknownEdError(value=f"Неизвестная единица {unit}")


def validate(value: float, from_unit: str, to_unit: str) -> tuple[float, str, str]:
    """
    Проверяет корректность значения и единиц измерения

    Args:
        value: Значение, которое необходимо преобразовать
        from_unit: Исходная единица измерения
        to_unit: Единица измерения результата

    Returns:
        Кортеж из преобразованного значения, исходной
        единицы измерения и итоговой

    Raises:
        IncorrectValueError: Если значение не может быть преобразовано
            в число или является недопустимым
        UnusableEdError: Если исходная и итоговая единицы измерения
            относятся к разным типам
        AbsZeroError: Если температура ниже абсолютного нуля
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise IncorrectValueError(value=f"Некорректное значение: {value}")

    from_type = type_const(from_unit.lower())
    to_type = type_const(to_unit.lower())

    # Проверяем совместимость единиц
    if from_type != to_type:
        raise UnusableEdError(value=f"Несовместимые единицы {from_unit} и {to_unit}")

    # Длина, масса и время не могут быть отрицательными
    if from_type in ("length", "mass", "time") and value < 0:
        raise IncorrectValueError(
            value=f"Значение не может быть отрицательным: {value}"
        )

    # Для температуры проверяем абсолютный ноль
    if from_type == "temperature":
        if from_unit == "k" and value < 0:
            raise AbsZeroError("Температура не может быть ниже абсолютного нуля")

        if from_unit == "c" and value < -273.15:
            raise AbsZeroError("Температура ниже абсолютного нуля")

        if from_unit == "f" and value < -459.67:
            raise AbsZeroError("Температура ниже абсолютного нуля")

    return value, from_unit, to_unit


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Конвертирует значение из одной единицы измерения в другую

    Перед выполнением преобразования проверяет корректность значения
    и совместимость исходной и итоговой единиц измерения

    Args:
        value: Значение, которое необходимо преобразовать
        from_unit: Единица измерения исходного значения
        to_unit: Единица измерения результата

    Returns:
        Преобразованное значение в итоговой единице измерения
    """
    value, from_unit, to_unit = validate(value, from_unit.lower(), to_unit.lower())

    # Длина
    if from_unit in LENGTH:
        return value * LENGTH[from_unit] / LENGTH[to_unit]

    # Масса
    if from_unit in MASS:
        return value * MASS[from_unit] / MASS[to_unit]

    # Время
    if from_unit in TIME:
        return value * TIME[from_unit] / TIME[to_unit]

    # Температура
    return convert_temperature(value, from_unit, to_unit)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Конвертирует значение температуры между единицами измерения

    Args:
        value: Значение температуры
        from_unit: Единица измерения исходной температуры
        to_unit: Единица измерения результата

    Returns:
        Значение температуры в итоговой единице измерения
    """
    # Сначала переводим в Цельсии
    if from_unit.lower() == "c":
        celsius = value
    elif from_unit.lower() == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit.lower() == "c":
        return celsius
    if to_unit.lower() == "f":
        return celsius * 9 / 5 + 32

    return celsius + 273.15
