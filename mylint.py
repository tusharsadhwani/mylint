import ast
import os
import sys
from typing import NamedTuple


class Checker(ast.NodeVisitor):
    def __init__(self):
        self.violating_nodes = set()


class LintRule(NamedTuple):
    issue_code: str
    issue_msg: int
    checker: Checker


class Linter:
    def __init__(self):
        self.lint_rules = set()

    def add_rule(self, issue_code, issue_msg, checker):
        self.lint_rules.add(LintRule(issue_code, issue_msg, checker))

    @staticmethod
    def print_violation(file_name, node, issue_code, issue_msg):
        print(
            f"{file_name}:{node.lineno}:{node.col_offset}: "
            f"{issue_code}: {issue_msg}"
        )

    def run(self, source_path):
        file_name = os.path.basename(source_path)

        with open(source_path) as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for issue_code, issue_msg, checker in self.lint_rules:
            checker.visit(tree)
            for node in checker.violating_nodes:
                self.print_violation(file_name, node, issue_code, issue_msg)


class SetDuplicateItemChecker(Checker):
    """Checks if a set in your code has duplicate constants."""

    def visit_Set(self, node: ast.Set):
        if len(node.elts) > 3:
            self.violating_nodes.add(node)


if __name__ == "__main__":
    source_paths = sys.argv[1:]

    linter = Linter()

    linter.add_rule(
        issue_code="W001",
        issue_msg="Set contains duplicate items",
        checker=SetDuplicateItemChecker(),
    )

    for source_path in source_paths:
        linter.run(source_path)
