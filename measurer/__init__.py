import sys
import time
import typing

class TestRunner:
    def __init__(self, function, *args: typing.Any, **kwds: typing.Any) -> None:
        self.__function = function
        self.__args = args
        self.__kwds = kwds
        self.__name = function.__name__

    def test(self, mode: str):
        if mode == "runtime":
            start = time.perf_counter()
            self.function(*self.__args, **self.__kwds)
            end = time.perf_counter()
            runningTime =  end - start
            return runningTime

        elif mode == "memory":
            return sys.getsizeof(self.function)
    
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
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function) -> TestRunner:
        return TestRunner(function, *self.args, **self.kwargs)

#def setTesting(*args, **kwargs):
#    def wrapper(function):
#        def caller(test: str):
#            global testingFunctions
#            if test == "runtime":
#                start = time.time()
#                function()
#                end = time.time()
#                return end - start
#
#            elif test == "memory":
#                return sys.getsizeof(function)
#
#            else:
#                raise ValueError("Unknown test")