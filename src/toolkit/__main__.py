import argparse

from .calculator import calculate
from .converter import convert


def create_parser():
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


def main(argv=None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "calc":
        result = args.func(args.expression)
        print(result)

    elif args.command == "convert":
        result = convert(args.value, args.from_, args.to)
        print(result)


if __name__ == "__main__":
    main()
