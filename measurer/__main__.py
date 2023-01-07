# -*- coding: utf-8 -*-
import argparse
import pathlib

from rich.table import Table
from rich.console import Console
from importlib import import_module, invalidate_caches

from . import TestRunner, TestResult

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
        
        if self.iters < 1:
            raise ValueError("Iters argument must be over 1")

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
        self.results: dict[str: dict[str: list[TestResult]]] = {}
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


class ResultTable:
    def __init__(self, iters: int, results: dict[str: dict[str: list[TestResult]]]) -> None:
        self.__iters = iters
        self.__results = results
    
    def create_console_table(self) -> Table:
        table = Table()
        table.add_column("Tests.")
        table.add_column("Functions.")
        for i in range(1, self.__iters+1):
            table.add_column(f"Iteration {i}.")
        
        if self.__iters > 1:
            table.add_column("Average.")
        for test, function_names in self.__results.items():
            for name, values in function_names.items():
                row = (
                    test,
                    name,
                    *(str(value) for value in values),
                )

                if self.__iters > 1:
                    row = (
                        *row,
                        str(self.__get_average(values))
                    )

                table.add_row(*row)

        return table

    def __get_average(self, results: list[TestResult]) -> TestResult:
        sum_ = 0
        for result in results:
            sum_ += result.result
        return sum_/len(results)

def main():
    cliManager = CLI()

    tester = Tester(cliManager.get_tests())
    tester.import_script(cliManager.module)
    tester.make_tests(cliManager.iters)

    table = ResultTable(cliManager.iters, tester.get_results()).create_console_table()

    cliManager.show_table(table)

if __name__ == "__main__":
    main()
