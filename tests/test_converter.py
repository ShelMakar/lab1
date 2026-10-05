import pytest

from toolkit.converter import convert
from toolkit.errors import (
    AbsZeroError,
    IncorrectValueError,
    UnknownEdError,
    UnusableEdError,
)


def test_millimeters_to_meters():
    assert convert(1000, "mm", "m") == 1.0


def test_meters_to_millimeters():
    assert convert(1, "m", "mm") == 1000.0


def test_kilograms_to_grams():
    assert convert(1.5, "kg", "g") == 1500.0


def test_hours_to_minutes():
    assert convert(1, "h", "min") == 60.0


def test_hours_to_seconds():
    assert convert(1, "h", "s") == 3600.0


def test_celsius_to_f():
    assert convert(0, "c", "f") == 32.0


def test_celsius_to_kelvin():
    assert convert(0, "c", "k") == 273.15


def test_f_to_kelvin():
    assert convert(32, "f", "k") == 273.15


def test_same_unit():
    assert convert(100, "m", "m") == 100


def test_negative_value():
    with pytest.raises(IncorrectValueError):
        convert(-1, "m", "cm")


def test_absolute_zero():
    with pytest.raises(AbsZeroError):
        convert(-274, "c", "c")


def test_incorrect_string_value():
    with pytest.raises(IncorrectValueError):
        convert("abc", "m", "m")


def test_empty_value():
    with pytest.raises(IncorrectValueError):
        convert("", "m", "m")


def test_unknown_from_unit():
    with pytest.raises(UnknownEdError):
        convert(1, "unknown", "m")


def test_unknown_to_unit():
    with pytest.raises(UnknownEdError):
        convert(1, "m", "unknown")


def test_length_and_mass():
    with pytest.raises(UnusableEdError):
        convert(1, "kg", "m")
