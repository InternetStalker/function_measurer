from __future__ import annotations
import pathlib

from importlib import import_module, invalidate_caches

from . import TestResult, AbstactTestInterface
class Tester:
    def __init__(self) -> None:
        if not isinstance(tests, list):
            tests = [tests]

        self.__testing_functions: list = []

    def import_script(self, path_to_script: pathlib.Path) -> None:
        program_folder = pathlib.Path(__file__).parent
        new_script_path = program_folder / path_to_script.name

        new_script_path.write_text(path_to_script.read_text())
        invalidate_caches()
        script = import_module(path_to_script.stem)

        new_script_path.unlink()
        
        for name in dir(script):
            if isinstance(getattr(script, name), AbstactTestInterface):
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

