from __future__ import annotations

import ast
import os
import sys
from typing import NamedTuple, Sequence


class Violation(NamedTuple):
    """
    Every rule violation contains a node that breaks the rule,
    and a message that will be shown to the user.
    """

    node: ast.AST
    message: str


class Checker(ast.NodeVisitor):
    """
    A Checker is a Visitor that defines a lint rule, and stores all the
    nodes that violate that lint rule.
    """

    def __init__(self, issue_code: str) -> None:
        self.issue_code = issue_code
        self.violations: set[Violation] = set()


class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self) -> None:
        self.checkers: set[Checker] = set()

    @staticmethod
    def print_violations(checker: Checker, file_name: str) -> None:
        """Prints all violations collected by a checker."""
        for node, message in checker.violations:
            print(
                f"{file_name}:{node.lineno}:{node.col_offset}: "
                f"{checker.issue_code}: {message}"
            )

    def run(self, source_path: str) -> None:
        """Runs all lints on a source file."""
        file_name = os.path.basename(source_path)

        with open(source_path) as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, file_name)


class SetDuplicateItemChecker(Checker):
    """Checks if a set in your code has duplicate constants."""

    def visit_Set(self, node: ast.Set) -> None:
        """Stores all the constants this set holds, and finds duplicates"""
        seen_values = set()
        for element in node.elts:
            # We're only concerned about constant values like ints.
            if not isinstance(element, ast.Constant):
                continue

            # if it's already in seen values, raise a lint violation.
            value = element.value
            if value in seen_values:
                violation = Violation(
                    node=element,
                    message=f"Set contains duplicate item: {value!r}",
                )
                self.violations.add(violation)

            else:
                seen_values.add(element.value)


class UnusedVariableInScopeChecker(Checker):
    """Checks if any variables are unused in this node's scope."""

    def __init__(self, issue_code: str) -> None:
        super().__init__(issue_code)
        # unused_names is a dictionary that stores variable names, and
        # whether or not they've been found in a "Load" context yet.
        # If it's found to be used, its value is turned to False.
        self.unused_names: dict[str, bool] = {}

        # name_nodes holds the first occurences of variables.
        self.name_nodes: dict[str, ast.Name] = {}

    def visit_Name(self, node: ast.Name) -> None:
        """Find all nodes that only exist in `Store` context"""
        var_name = node.id

        if isinstance(node.ctx, ast.Store):
            # If it's a new name, save the node for later
            if var_name not in self.name_nodes:
                self.name_nodes[var_name] = node

            # If we've never seen it before, it is unused.
            if var_name not in self.unused_names:
                self.unused_names[var_name] = True

        else:
            # It's used somewhere.
            self.unused_names[var_name] = False


class UnusedVariableChecker(Checker):
    def check_for_unused_variables(self, node: ast.AST) -> None:
        """Find unused variables in the local scope of this node."""
        visitor = UnusedVariableInScopeChecker(self.issue_code)
        visitor.visit(node)

        for name, unused in visitor.unused_names.items():
            if unused:
                node = visitor.name_nodes[name]
                self.violations.add(Violation(node, f"Unused variable: {name!r}"))

    def visit_Module(self, node: ast.Module) -> None:
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_for_unused_variables(node)
        super().generic_visit(node)


def cli(argv: Sequence[str] = sys.argv) -> None:
    source_paths = argv[1:]

    linter = Linter()
    linter.checkers.add(SetDuplicateItemChecker(issue_code="W001"))
    linter.checkers.add(UnusedVariableChecker(issue_code="W002"))

    for source_path in source_paths:
        linter.run(source_path)
