from __future__ import annotations
from copy import copy
import sys
import time
import typing


from abc import ABC, abstractmethod

class TestResult:
    def __init__(self, results: typing.Iterable[int | float], unit: str) -> None:        
        self._results: tuple[int | float] = tuple(results)
        self._unit: str = unit

        if not all(map(results, lambda item: isinstance(item, (int, float)))):
            raise TypeError("Results should be int or float")

        if not isinstance(unit, str):
            raise TypeError("Unit should be str")

    @property
    def results(self) -> int | float:
        return copy(self._results)
    
    @property
    def unit(self) -> str:
        return self._unit

    @property
    def average(self) -> int | float:
        return sum(self._results)/len(self._results)


class AbstartTestInterface(ABC):
    @abstractmethod
    def test(self) -> TestResult:
        pass


class MeasureTime(AbstartTestInterface):
    def __init__(self, iters: int, *args, **kwds) -> None:
        self._iters = iters
        self._args: typing.Any = args
        self._kwds: dict[str, typing.Any] = kwds
        self._function = None

    def __call__(self, function: typing.Callable) -> MeasureTime:
        self._function = function
        self.__call__ = lambda *args, **kwds: function(*args, **kwds)
        return self
    
    def test(self) -> TestResult:
        return TestResult(())


class MeasureContextTime(AbstartTestInterface):
    def __init__(self) -> None:
        pass

    def __enter__(self) -> None:
        pass

    def __exit__(self, _, __, ___) -> None:
        pass


class MeasureSize(AbstartTestInterface):
    def __init__(self, obj: typing.Any) -> None:
        pass