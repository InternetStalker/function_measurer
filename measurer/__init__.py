from __future__ import annotations
import sys
import time
import typing


from abc import ABC, abstractmethod
from functools import wraps


class TestResult:
    def __init__(self, results: typing.Iterable[int | float | None], unit: str, tested_name: str, test_mode: str) -> None:        
        self._results: tuple[int | float | None] = tuple(results)
        self._unit: str = unit
        self._tested_name: str = tested_name
        self._test_mode: str = test_mode

        if not all(map(results, lambda item: isinstance(item, (int, float, None)))): # type: ignore
            raise TypeError("Results should be int, float or None")

        if not isinstance(unit, str):
            raise TypeError("Unit should be str")
        
        if not isinstance(tested_name, str):
            raise TypeError("Tested_name should be str")
        
        if not isinstance(test_mode, str):
            raise TypeError("Test_mode should be str")

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def average(self) -> int | float:
        if None in self._results:
            raise Exception("Can't count average for containing None results")
        
        return sum(self._results)/len(self._results) # type: ignore
    
    @property
    def tested_name(self) -> str:
        return self._tested_name

    @property
    def test_mode(self) -> str:
        return self._test_mode
    
    @property
    def iters(self) -> int:
        return len(self._results)
    
    def __getitem__(self, key: int | slice) -> int | float | list[int | float]:
        return self._results[key] # type: ignore


class AbstactTestInterface(ABC):
    @abstractmethod
    def test(self) -> TestResult:
        pass


class MeasureTime(AbstactTestInterface):
    """
    A decorator using for measuring the time perfomance of callable objects.
    Gives the result in fractional seconds. Uses time.perf_counter for measuring.
    Doesn't have any side effects on measuring callable. The callable is able for common use.
    """
    def __init__(self, iters: int, *args, **kwds) -> None:
        self._iters = iters
        self._args: typing.Any = args
        self._kwds: dict[str, typing.Any] = kwds
        self._function = None

    def __call__(self, function: typing.Callable) -> MeasureTime:
        self._function = function
        self.__call__ = wraps(function)(lambda *args, **kwds: function(*args, **kwds))
        return self
    
    def test(self) -> TestResult:
        return TestResult(
            (self._measure_perfomance() for _ in range(self._iters)),
            "sec",
            self._function.__name__, #type: ignore
            "runtime"
            )
    
    def _measure_perfomance(self) -> float:
        start = time.perf_counter()
        self._function() #type: ignore
        end = time.perf_counter()
        return end - start


class MeasureContextTime(AbstactTestInterface):
    def __enter__(self) -> None:
        self._start = time.perf_counter()

    def __exit__(self, _, __, ___):
        self._end = time.perf_counter()
        return super().__exit__(_, __, ___) # type: ignore
    
    def test(self) -> TestResult:
        return TestResult((self._end - self._start,), "sec", "context", "runtime")


class MeasureSize(AbstactTestInterface):
    def __init__(self, obj: typing.Any) -> None:
        self._obj = obj
    
    def test(self) -> TestResult:
        return TestResult((self._get_size(self._obj),), "bytes", self._obj.__name__, "memory ")

    def _get_size(self, obj: typing.Any, seen: set | None = None) -> int:
        if seen is None:
            seen = set()
        if obj_id := id(obj) in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(obj)
        if isinstance(obj, dict):
            size += sum((self._get_size(v, seen) for v in obj.values()))
            size += sum((self._get_size(k, seen) for k in obj.keys()))
        elif hasattr(obj, '__dict__'):
            size += self._get_size(obj.__dict__, seen)

        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum((self._get_size(i, seen) for i in obj))

        return size