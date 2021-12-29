import os

from pytest import CaptureFixture

from mylint import cli


def test_mylint(capsys: CaptureFixture[str]) -> None:
    test_folder = os.path.dirname(__file__)
    cli(["mylint", f"{test_folder}/testcode.py"])

    stdout, _ = capsys.readouterr()

    assert sorted(stdout.splitlines()) == sorted(
        [
            "testcode.py:3:0: W002: Unused variable: 's'",
            "testcode.py:8:4: W002: Unused variable: 'var'",
            "testcode.py:21:0: W002: Unused variable: 's2'",
            "testcode.py:15:12: W001: Set contains duplicate item: 'PUT'",
            "testcode.py:21:15: W001: Set contains duplicate item: 1",
        ]
    )
