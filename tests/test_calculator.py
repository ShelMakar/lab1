import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionZeroError,
    EmptyExpressionError,
    IncorrectSymbolError,
    MissedOperandError,
    UncorrectExpression,
)


def test_unary_minus():
    assert calculate("2*-3") == -6


def test_unary_plus_after_binary():
    assert calculate("1++2") == 3


def test_unary_minus_after_binary():
    assert calculate("1--2") == 3


def test_unary_plus_minus():
    assert calculate("1+-2") == -1


def test_minus_plus():
    assert calculate("1-+2") == -1


def test_skobki():
    assert calculate("(2+3)*4") == 20


def test_many_operations():
    assert calculate("2+3*4-10/2") == 9


def test_operations_with_spaces():
    assert calculate(" 2 + 3 * 4 ") == 14


def test_empty_expression():
    with pytest.raises(EmptyExpressionError):
        calculate("   ")


def test_incorrect_symbol():
    with pytest.raises(IncorrectSymbolError):
        calculate("2+a")


def test_missing_operand_at_end():
    with pytest.raises(MissedOperandError):
        calculate("2+3*")


def test_missing_operand_at_beginning():
    with pytest.raises(MissedOperandError):
        calculate("*2+3")


def test_missing_operand_after_operator():
    with pytest.raises(MissedOperandError):
        calculate("2+")


def test_two_numbers_without_operator():
    with pytest.raises(UncorrectExpression):
        calculate("2 3")


def test_unclosed_skobka():
    with pytest.raises(UncorrectExpression):
        calculate("(2+3")


def test_extra_closing_skobka():
    with pytest.raises(UncorrectExpression):
        calculate("2+3)")


def test_wrong_number_at_end():
    with pytest.raises(UncorrectExpression):
        calculate("2.")


def test_wrong_number_at_beginning():
    with pytest.raises(UncorrectExpression):
        calculate(".5")


def test_two_decimal_points():
    with pytest.raises(UncorrectExpression):
        calculate("2.5.3")


def test_two_unary_operators():
    with pytest.raises(UncorrectExpression):
        calculate("--3")


def test_unary_operator_before_skobka():
    with pytest.raises(UncorrectExpression):
        calculate("-(2+3)")


def test_unary_operator_before_unary_expression():
    with pytest.raises(UncorrectExpression):
        calculate("2*-(-3)")


def test_division_by_zero():
    with pytest.raises(DivisionZeroError):
        calculate("1/0")
