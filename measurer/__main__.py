# -*- coding: utf-8 -*-
import argparse
import pathlib

from rich.console import Console
from rich.table import Table
from importlib import import_module, invalidate_caches

from . import TestRunner

class CLI:
    possible_tests = ["runtime", "memory"]

    def __init__(self) -> None:
        argparser = argparse.ArgumentParser(
            prog = "tester",
            description = "Program for testing python modules.",
            fromfile_prefix_chars = "@"
            )
        argparser.add_argument(
            "module",
            type = str,
            help = "Given module for testing."
            )
        argparser.add_argument(
            "iters",
            type = int,
            help = "How many times module will be tested."
            )
        argparser.add_argument(
            "tests",
            choices = CLI.possible_tests,
            help = "Tests those measurer should do with given module.",
            nargs = "+"
            )

        arguments = argparser.parse_args()

        self.module = pathlib.Path(arguments.module)
        self.iters: int = arguments.iters
        self.tests: list[str] = arguments.tests

        if not self.module.exists():
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")

    def get_tests(self) -> list[str] | str:
        return self.tests

    def show_table(self, table: Table) -> None:
        console = Console()
        console.print(table)

class Tester:
    def __init__(self, tests: list[str] | str) -> None:
        if not isinstance(tests, list):
            tests = [tests]

        self.tests = tests
        self.testing_functions: list[TestRunner] = []

    def import_script(self, path_to_script: pathlib.Path) -> None:
        program_folder = pathlib.Path(__file__).parent
        new_script_path = program_folder / path_to_script.name

        new_script_path.write_text(path_to_script.read_text())
        invalidate_caches()
        script = import_module(path_to_script.stem)

        new_script_path.unlink()
        
        for name in dir(script):
            if isinstance(getattr(script, name), TestRunner):
                self.testing_functions.append(getattr(script, name))

    def make_tests(self, iters: int) -> None:
        self.results: dict[str: dict[str: list]] = {}
        for test in self.tests:
            if self.testing_functions != []:
                results = {}
                for function in self.testing_functions:
                    results.update({function.name: [function.test(test) for _ in range(iters)]})
                self.results.update({test: results})
            else:
                self.results.update({test: {"": ["" for _ in range(iters)]}})

    def get_results(self) -> dict:
        return self.results

    def create_table(self, iters: int) -> Table:
        table = Table()
        table.add_column("Tests.")
        table.add_column("Functions.")
        for i in range(1, iters+1):
            table.add_column(f"Iteration {i}.")
        table.add_column("Average.")

        for test, function_names in self.results.items():
            for name, values in function_names.items():
                table.add_row(test, name, *[str(value) for value in values], str(sum(values)/len(values)))

        return table

def main():
    cliManager = CLI()

    tester = Tester(cliManager.get_tests())
    tester.import_script(cliManager.module)
    tester.make_tests(cliManager.iters)

    table = tester.create_table(cliManager.iters)

    cliManager.show_table(table)

if __name__ == "__main__":
    main()
