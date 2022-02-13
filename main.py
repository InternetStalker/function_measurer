import os, sys, time

def setTesting(*args, **kwargs):
    def function_(func):
        def testMode(testMode):
            if testMode == "time":
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                runningTime = start - end
                return runningTime
        return testMode
    main.setTesting(main, function_)
    return function_

class main:
    def __init__(self) -> None:
        pass

    def setTesting(self, function) -> None:
        pass

    def showRes(self) -> None:
        pass

    def importScript(self, nameOfScript) -> None:
        pass

if __name__ == "__main__":
    os.system("python -m unittest -v test.py")