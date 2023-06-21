from __future__ import annotations
import pathlib
import typing

from importlib import import_module, invalidate_caches
from enum import Enum

from . import TestRunner, TestResult


class Unit(typing.NamedTuple):
    name: str
    value: int

class TestModes (str, Enum):
    MEMORY = "memory"
    RUNTIME = "runtime"

class Units(Unit, Enum):
    pass

class TimeUnits(Units):
    NANOSECOND = Unit("ns", 1)
    MICROSECOND = Unit("μs", 1000)
    MILLISECOND = Unit("ms", 10**6)
    SECOND = Unit("sec", 10**9)
    MINUTE = Unit("min", 60*10**9)

class MemoryUnits(Units):
    BIT = Unit("bit", 1)
    BYTE = Unit("byte", 8)

class TestResult:
    def __init__(self, result: float, unit: Units) -> None:
        self._result = result
        self._unit = unit

    @property
    def result(self) -> float:
        return self._result
    
    @property
    def unit(self) -> Units:
        return self._unit

    def __str__(self) -> str:
        return f"{self.result}, {self.unit}"
    
    def __add__(self, res2: int | float | TestResult) -> TestResult:
        if isinstance(res2, (int, float)):
            return TestResult(self.result + res2, self.unit)

        if res2.unit != self.unit:
            raise TypeError("Tryed to add TestResults with different units")
        

        return TestResult(self.result + res2.result, self.unit)
    
    def __iadd__(self, res2: int | float | TestResult) -> TestResult:
        return self.__add__(res2)
    
    def __truediv__(self, res2:  int | float | TestResult) -> TestResult:
        if isinstance(res2, (int, float)):
            return TestResult(self.result / res2, self.unit)
        
        return TestResult(self.result / res2.result, self.unit)

class TestRunner:
    def __init__(
        self,
        function: typing.Any,
        test_mode: TestModes,
        *args: typing.Any,
        **kwds: typing.Any
        ) -> None:
        self._function = function
        self._args = args
        self._kwds = kwds
        self._name = function.__name__
        self._test_mode = test_mode
        
    def test(self) -> TestResult:
        if self.test_mode == TestModes.RUNTIME:
            return self._get_runtime()

        elif self.test_mode == TestModes.MEMORY:
            return self._get_size(self._function)
    
    def _get_size(self, obj: typing.Any, seen: set | None = None) -> TestResult:
        if seen is None:
            seen = set()
        if obj_id := id(obj) in seen:
            return TestResult(0, "b")
        seen.add(obj_id)

        size = TestResult(float(sys.getsizeof(obj)), MemoryUnits.BYTE)
        if isinstance(obj, dict):
            size += sum((self._get_size(v, seen) for v in obj.values()))
            size += sum((self._get_size(k, seen) for k in obj.keys()))
        elif hasattr(obj, '__dict__'):
            size += self._get_size(obj.__dict__, seen)

        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum((self._get_size(i, seen) for i in obj))
        
        return size

    def _get_runtime(self) -> TestResult:
        start = time.perf_counter()
        self._function(*self._args, **self._kwds)
        end = time.perf_counter()
        runtime =  end - start
        return TestResult(runtime, RuntimeUnits.SEC)

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def arguments(self) -> list[typing.Any, ...]:
        return self._args
    
    @property
    def kw_arguments(self) -> dict[str: typing.Any]:
        return self._kwds
    
    @property
    def function(self) -> typing.Any:
        return self._function
    
    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> typing.Any:
        return self.function(*args, **kwds)


class SetTesting:
    def __init__(self,
        *args: typing.Any,
        test_mode: TestModes=TestModes.RUNTIME,
        **kwds: dict[str, typing.Any]
        ) -> None:
        self._args = args
        self._test_mode = test_mode
        self._kwds = kwds

    def __call__(self, function) -> TestRunner:
        return TestRunner(function, self._test_mode *self._args, **self._kwds)


class Tester:
    def __init__(self, iters: int) -> None:
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

