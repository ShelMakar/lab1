from .constants import TIME, LENGTH, MASS


def convert(value, from_unit, to_unit):
    value = float(value)

    if from_unit.lower() in LENGTH and to_unit.lower() in LENGTH:
        return value * LENGTH[from_unit] / LENGTH[to_unit]
    if from_unit.lower() in MASS and to_unit.lower() in MASS:
        return value * MASS[from_unit] / MASS[to_unit]
    if from_unit.lower() in TIME and to_unit.lower() in TIME:
        return value * TIME[from_unit] / TIME[to_unit]
    if from_unit.lower() in ("c", "f", "k") and to_unit.lower() in ("c", "f", "k"):
        return convert_temperature(value, from_unit, to_unit)

    raise ValueError("Нельзя преобразовать")


def convert_temperature(value, from_unit, to_unit):
    # Сначала переводим в Цельсии
    if from_unit.lower() == "c":
        celsius = value
    elif from_unit.lower() == "f":
        celsius = (value - 32) * 5 / 9
    elif from_unit.lower() == "k":
        celsius = value - 273.15
    else:
        raise ValueError("Неизвестная единица температуры")

    if to_unit.lower() == "c":
        return celsius
    if to_unit.lower() == "f":
        return celsius * 9 / 5 + 32
    if to_unit.lower() == "k":
        return celsius + 273.15

    raise ValueError("Неизвестная единица температуры")
