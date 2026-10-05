import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def create_parser() -> argparse.ArgumentParser:
    """
    Создаёт и настраивает парсер аргументов командной строки.

    Парсер поддерживает две команды: ``calc`` для вычисления
    арифметических выражений и ``convert`` для конвертации единиц
    измерения.

    Returns:
        Настроенный экземпляр ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="toolkit", description="Консольный набор утилит"
    )

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Калькулятор
    calculator_parser = subparsers.add_parser("calc", help="Калькулятор")

    calculator_parser.add_argument("expression", help="Вычисляемое выражение")

    calculator_parser.set_defaults(func=calculate)

    # Конвертер
    converter_parser = subparsers.add_parser(
        "convert", help="Конвертер единиц измерения"
    )

    converter_parser.add_argument("value", help="числовое значение")

    converter_parser.add_argument(
        "--from", dest="from_", required=True, help="исходная единица"
    )

    converter_parser.add_argument("--to", required=True, help="целевая единица")

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Обрабатывает аргументы командной строки и запускает выбранную утилиту.

    В зависимости от указанной команды выполняет вычисление
    арифметического выражения или конвертацию единиц измерения.
    Ошибки, связанные с работой утилит, выводятся в стандартный
    поток ошибок.

    Args:
        argv: Список аргументов командной строки. Если значение
            не указано, аргументы берутся из sys.argv.

    Returns:
        Код завершения программы: ``0`` при успешном выполнении
        и ``2`` при возникновении ошибки ToolkitError.

    Raises:
        SystemExit: Если аргументы командной строки имеют некорректный
            формат. Исключение вызывается argparse.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = args.func(args.expression)
            print(result)

        elif args.command == "convert":
            result = convert(args.value, args.from_, args.to)
            print(result)

    except ToolkitError as e:
        print(f"Ошибка {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    main()
