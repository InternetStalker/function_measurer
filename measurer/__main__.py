import pathlib
import argparse


from importlib import import_module, invalidate_caches

from . import TestRunner, TestResult
from .result_tables import create_result_table, BaseResultTable

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
            "--csv",
            help = "Path to csv file where results would be saved.",
            default = None,
            action = "store"
        )

        arguments = argparser.parse_args()

        self.module = pathlib.Path(arguments.module)
        self.iters: int = arguments.iters
        self.tests: list[str] = arguments.tests
        self.save_to_csv = bool(arguments.csv)

        if self.save_to_csv:
            self.path_to_csv = pathlib.Path(arguments.csv)
        
        else:
            self.path_to_csv = None

        if not self.module.exists():
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")
        
        if self.iters < 1:
            raise ValueError("Iters argument must be over 1")

    def get_tests(self) -> list[str] | str:
        return self.tests


class Tester:
    def __init__(self, tests: list[str] | str, iters: int) -> None:
        if not isinstance(tests, list):
            tests = [tests]

        self.__tests = tests
        self.__iters = iters
        self.__testing_functions: list[TestRunner] = []

    def import_script(self, path_to_script: pathlib.Path) -> None:
        program_folder = pathlib.Path(__file__).parent
        new_script_path = program_folder / path_to_script.name

        new_script_path.write_text(path_to_script.read_text())
        invalidate_caches()
        script = import_module(path_to_script.stem)

        new_script_path.unlink()
        
        for name in dir(script):
            if isinstance(getattr(script, name), TestRunner):
                self.__testing_functions.append(getattr(script, name))

    def make_tests(self) -> None:
        self.results: dict[str: dict[str: list[TestResult]]] = {}
        for test in self.__tests:
            if self.__testing_functions != []:
                for function in self.__testing_functions:
                    self.results[test] = {function.name: [function.test() for _ in range(self.__iters)]}
            else:
                self.results[test] = {"": ["" for _ in range(self.__iters)]}

    def get_results(self) -> dict:
        return self.results




def main():
    CliManager = CLI()

    tester = Tester(CliManager.get_tests(), CliManager.iters)
    tester.import_script(CliManager.module)
    tester.make_tests()

    table: BaseResultTable = create_result_table(
        CliManager.iters,
        tester.get_results(),
        CliManager.save_to_csv,
        CliManager.path_to_csv
        )
    
    table.show()


if __name__ == "__main__":
    main()
