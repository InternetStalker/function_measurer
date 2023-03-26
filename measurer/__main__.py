from __future__ import annotations
import pathlib


from importlib import import_module, invalidate_caches

from . import TestRunner, TestResult
from .result_tables import create_result_table, BaseResultTable
from .cli import CLI


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
