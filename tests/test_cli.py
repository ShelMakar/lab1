import pytest

from toolkit.__main__ import main


def test_calc_command(capsys):
    result = main(["calc", "2+3*4"])

    captured = capsys.readouterr()

    assert result == 0
    assert float(captured.out.strip()) == 14.0
    assert captured.err == ""


def test_convert_command(capsys):
    result = main(
        [
            "convert",
            "1000",
            "--from",
            "mm",
            "--to",
            "m",
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert float(captured.out.strip()) == 1.0
    assert captured.err == ""


def test_calc_command_with_error(capsys):
    result = main(["calc", "1/0"])

    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert "Ошибка" in captured.err


def test_convert_command_with_error(capsys):
    result = main(
        [
            "convert",
            "1",
            "--from",
            "kg",
            "--to",
            "m",
        ]
    )

    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert "Ошибка" in captured.err


def test_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 0
    assert "Консольный набор утилит" in captured.out
    assert "calc" in captured.out
    assert "convert" in captured.out


def test_no_arguments(capsys):
    result = main([])

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == ""
    assert captured.err == ""
