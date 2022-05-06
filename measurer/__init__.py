import time, sys

class testRunner:
    def __init__(self, function, *args, **kwargs) -> None:
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.name = function.__name__

    def __call__(self, mode: str):
        if mode == "runtime":
            start = time.time()
            self.function(*self.args, **self.kwargs)
            end = time.time()
            runningTime = start - end
            return runningTime
        elif mode == "memory":
            return sys.getsizeof(self.function)


class setTesting:
    def __init__(self, *args, **kwargs) -> None:
        from measurer import testRunner
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function) -> testRunner:
        return testRunner(function, *self.args, **self.kwargs)