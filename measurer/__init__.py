import time, sys

__version__ = "0.1.1"

def setTesting(*args, testingFunctions: list, **kwargs):
    def function_(func):
        def testMode(testMode):
            if testMode == "runtime":
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                runningTime = start - end
                return runningTime
            elif testMode == "memory":
                return sys.getsizeof(func)
        testMode.__name__ = func.__name__
        testingFunctions.append(testMode)
        return testMode
    return function_