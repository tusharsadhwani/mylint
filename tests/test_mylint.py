import os

from pytest import CaptureFixture

from mylint import cli


def test_mylint(capsys: CaptureFixture[str]) -> None:
    test_folder = os.path.dirname(__file__)
    cli(["mylint", f"{test_folder}/testcode.py"])

    stdout, _ = capsys.readouterr()

    assert sorted(stdout.splitlines()) == sorted(
        [
            "testcode.py:1:0: W002: Unused variable: 's'",
            "testcode.py:5:4: W002: Unused variable: 'var'",
            "testcode.py:17:0: W002: Unused variable: 's2'",
            "testcode.py:12:12: W001: Set contains duplicate item: 'PUT'",
            "testcode.py:17:15: W001: Set contains duplicate item: 1",
        ]
    )
