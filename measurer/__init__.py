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
            self.__get_runtime(self.__function)

        elif mode == "memory":
            self.__get_size
    
    def __get_size(self, obj: typing.Any) -> int:
        size = sys.getsizeof(obj)
        if isinstance(obj, typing.Iterable):
            return size + sum(self.__get_size(el) for el in obj)
        
        else:
            if hasattr(obj, "__dict__"):
                return size + sum(self.__get_size(val) for val in obj.__dict__.values)
            
            else:
                return size

    def __get_runtime(self) -> float:
        start = time.perf_counter()
        self.__function(*self.__args, **self.__kwds)
        end = time.perf_counter()
        runtime =  end - start
        return runtime

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
