#!usr/bin/env python
# -*- coding: utf-8 -*-
import os, argparse, time, sys
from simple_file_user.File import File
from importlib import import_module, invalidate_caches

def setTesting(*args, testingFunctions: list, **kwargs):
    def function_(func):
        def testMode(testMode):
            if testMode == "time":
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

class Lens:
    def __init__(self, testNames: list, functionsNames: list, resultsAndIterations: list) -> None:
        self.testLen = max([len(name) for name in testNames])
        self.functionLen = max([len(name) for name in functionsNames])
        self.coloumnLens = [max(iter) for iter in resultsAndIterations]
        self.tableLen = self.testLen + self.functionLen + self.coloumnLens + 3

class main:
    possibleTests = ["time", "memory"]
    testingFunctions = []

    def __init__(self, tests: list, iters: int) -> None:
        if not isinstance(tests, list):
            raise TypeError("Invalid test given.")

        for test in tests:
            if not test in self.possibleTests:
                raise ValueError(f"Invalid test given: {test}")

        self.tests = tests
        self.iters = iters

    def showRes(self) -> None:
        self.__createHTable()
        self.__showHTable()

    def importScript(self, pathToScript: str) -> None:
        programFolder = os.path.abspath(os.path.dirname(__file__))
        pathToScript = os.path.abspath(pathToScript)

        script = File(pathToScript)
        scriptContent = script.read()
        scriptName = script.getName()

        if scriptName in os.listdir(programFolder) and scriptName.endswith(".py"):
            invalidate_caches()
            self.script = import_module(os.path.splitext(scriptName)[0])
        else:

            newScriptName = self.__makeNewScriptName(scriptName)
            newScript = File(os.path.join(programFolder, newScriptName), new = True)
            newScript.rewrite(scriptContent)

            moduleName = os.path.splitext(os.path.split(newScriptName)[1])[0]

            invalidate_caches()
            self.script = import_module(moduleName)
            
        self.testingFunctions.extend(self.script.testingFunctions)


    def startTesting(self) -> None:
        self.res = {test: [[func(test) for i in range(self.iters)] for func in self.testingFunctions] for test in self.tests}
        self.showRes()

    def __makeNewScriptName(self, scriptName: str) -> str:
        scriptName = os.path.splitext(scriptName)[0]
        return scriptName + ".py"

    def __createHTable(self) -> None:
        self.functionNames = [func.__name__ for func in self.testingFunctions]
        self.iters_ = [f"итерация {i}|" for i in range(1, self.iters + 1)]

        lens = self.__setLens()

        heading = f"|%+{lens.testLen}s|%+{lens.functionLen}s|" % ("Тесты.", "Функции.") + ''.join(
            [f"%+{lens.coloumnLens[i]}s" % self.iters_[i] for i in range(self.iters)]
            )

        content = self.__createContentForHTable(lens.testLen, lens.functionLen, lens.coloumnLens, lens.tableLen)

        self.hTable = ["-" * lens.tableLen + "\n", *heading, "\n" + "-" * lens.tableLen + "\n", *content]

    def __showHTable(self) -> None:
        print("".join(self.hTable))

    def __setLens(self) -> Lens:
        tests = ["Тесты.", *[test for test in self.tests]]
        functions = ["Функции.", *[name for name in self.functionNames]]

        resultColumns = []

        for iterIndex in range(self.iters):
            column = [len(self.iters_[iterIndex])]

            for funcs in self.res.values():
                for results in funcs:
                    column.append(len(str(results[iterIndex])))
        
            resultColumns.append(column)
        
        lens = Lens(tests, functions)

        return lens

    def __createContentForHTable(self, test_len, func_len, res_lens: list, tableLen: int) -> list:
        strs = []

        for test, funcs in self.res.items():
            strs.append( f"|%+{test_len}s|" % test)

            i = 0
            for func, name in zip(funcs, [func.__name__ for func in self.testingFunctions]):
                if i:
                    strs.append(f"|{' ' * test_len}|")

                strs.append(f"%+{func_len}s|" % name)

                for iter, iter_res in enumerate(func):
                    strs.append(f"%+{res_lens[iter] - 1}s|" % str(iter_res))

                i += 1
                strs.append("\n")

            if not i:
                strs.extend (
                    [
                    " " * func_len + "|",
                    *[" " * (len_ - 1) + "|" for len_ in res_lens], 
                    "\n"
                    ]
                )
            strs.append("-" * tableLen + "\n")

        return strs

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description = "Program for testing python modules.")
    argparser.add_argument("module", type = str, help = "Given module for testing.")
    argparser.add_argument("iters", type = int, help = "How many times module will be tested.")
    argparser.add_argument("tests", nargs = "+", choices = ["time", "memory"], help = "Tests that program should do with given module.")
    args = argparser.parse_args()

    tester = main(args.tests, args.iters)
    tester.importScript(args.module)
    tester.startTesting()