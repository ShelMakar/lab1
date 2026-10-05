PRIORITY = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
}

OPERATORS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "//": lambda a, b: a // b,
    "%": lambda a, b: a % b,
}

LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
}

MASS = {
    "g": 1,
    "kg": 1000,
}

TIME = {
    "s": 1,
    "min": 60,
    "h": 3600,
}
