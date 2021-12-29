# mylint

My really simple rendition of how a linter works.

This original version was written for my [AST article][1]. Since then I've added
tests and turned it into a package. Check the [original branch][2] for the
original version of this, that was used in the article.

[1]: https://sadh.life/post/ast
[2]: https://github.com/tusharsadhwani/mylint/tree/original

## Installation

```console
pip install mylint
```

## Usage

```console
mylint [...file names]
```

Example:

```console
$ mylint tests/testcode.py
testcode.py:17:15: W001: Set contains duplicate item: 1
testcode.py:12:12: W001: Set contains duplicate item: 'PUT'
testcode.py:1:0: W002: Unused variable: 's'
testcode.py:5:4: W002: Unused variable: 'var'
testcode.py:17:0: W002: Unused variable: 's2'
```

## Development / Testing

Setup a virtual environment, and install the package with:

```bash
pip install -r requirements-dev.txt
```

Then run `pytest` to run tests. Now, have fun playing with the code and tests!

## Type Checking

Run `mypy .`
