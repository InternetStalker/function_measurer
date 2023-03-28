from __future__ import annotations
import pathlib

from importlib import import_module, invalidate_caches

from . import TestResult, AbstactTestInterface
class Tester:
    def __init__(self) -> None:
        self._testing_functions: list[AbstactTestInterface] = []

    def import_script(self, path_to_script: pathlib.Path) -> None:
        program_folder = pathlib.Path(__file__).parent
        new_script_path = program_folder / path_to_script.name

        new_script_path.write_text(path_to_script.read_text())
        invalidate_caches()
        script = import_module(path_to_script.stem)

        new_script_path.unlink()
        
        for name in dir(script):
            if isinstance(getattr(script, name), AbstactTestInterface):
                self._testing_functions.append(getattr(script, name))

    def do_tests(self) -> list[TestResult]:
        return [func.test() for func in self._testing_functions]

    def get_results(self) -> dict:
        return self.results

