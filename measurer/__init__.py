from __future__ import annotations
import sys
import time
import typing


class PossibleTests (str, typing.Enum):
    MEMORY = "memory"
    RUNTIME = "runtime"

class TestResult:
    def __init__(self, result: int | float, unit: str) -> None:
        if not isinstance(result, (int, float)):
            raise Exception("Result should be int or float")
        
        if not isinstance(unit, str):
            raise Exception("Unit should be str")
        
        self.__result = result
        self.__unit = unit

    @property
    def result(self) -> int | float:
        return self.__result
    
    @property
    def unit(self) -> str:
        return self.__unit

    def __str__(self) -> str:
        return f"{self.__result}, {self.unit}"
    
    def __add__(self, res2) -> int:
        if isinstance(res2, int):
            return TestResult(self.__result + res2, self.unit)

        if res2.unit != self.__unit:
            raise TypeError("Tryed to add TestResults with different units")
        

        return TestResult(self.__result + res2.result, self.__unit)
    
    def __iadd__(self, res2):
        return self.__add__(res2)
    
    def __truediv__(self, res2):
        if isinstance(res2, (int, float)):
            return TestResult(self.__result / res2, self.__unit)
        
        return TestResult(self.__result / res2.result, self.__unit)

class TestRunner:
    def __init__(self, function, *args: typing.Any, **kwds: typing.Any) -> None:
        self.__function = function
        self.__args = args
        self.__kwds = kwds
        self.__name = function.__name__
        self.__test_mode: str = kwds.pop("test_mode")
        
    def test(self):
        if self.__test_mode == "runtime":
            return self.__get_runtime()

        elif self.__test_mode == "memory":
            return self.__get_size(self.__function)
    
    def __get_size(self, obj: typing.Any, seen: set | None = None) -> TestResult:
        if seen is None:
            seen = set()
        if obj_id := id(obj) in seen:
            return TestResult(0, "b")
        seen.add(obj_id)

        size = TestResult(sys.getsizeof(obj), "b")
        if isinstance(obj, dict):
            size += sum((self.__get_size(v, seen) for v in obj.values()))
            size += sum((self.__get_size(k, seen) for k in obj.keys()))
        elif hasattr(obj, '__dict__'):
            size += self.__get_size(obj.__dict__, seen)

        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum([self.__get_size(i, seen) for i in obj])
        
        return size

    def __get_runtime(self) -> float:
        start = time.perf_counter()
        self.__function(*self.__args, **self.__kwds)
        end = time.perf_counter()
        runtime =  end - start
        return TestResult(runtime, "sec")

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def arguments(self) -> list[typing.Any]:
        return self.__args
    
    @property
    def kw_arguments(self) -> dict[str: typing.Any]:
        return self.__kwds
    
    @property
    def function(self) -> typing.Any:
        return self.__function
    
    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> typing.Any:
        return self.function(*args, **kwds)


class SetTesting:
    def __init__(self, *args, **kwds) -> None:
        self.__args = args
        self.__kwds = kwds

    def __call__(self, function) -> TestRunner:
        return TestRunner(function, *self.__args, **self.__kwds)
