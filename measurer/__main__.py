# -*- coding: utf-8 -*-
import os
import argparse
import pathlib
from importlib import import_module, invalidate_caches
from . import testRunner

class CLI:
    possibleTests = ["runtime", "memory"]

    def __init__(self) -> None:
        argparser = argparse.ArgumentParser("tester", description="Program for testing python modules.", fromfile_prefix_chars="-@")
        argparser.add_argument("module", type_=str, description="Given module for testing.")
        argparser.add_argument("iters", type_=int, description="How many times module will be tested.")
        argparser.add_argument("tests", choices=CLI.possibleTests, description="Tests those measurer should do with given module.", nargs="+")
        arguments = argparser.parse_args()

        self.module = os.path.abspath(arguments["module"])
        self.iters = arguments["iters"]
        self.tests = arguments["tests"]

        if not os.access(self.module, os.F_OK):
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")

    def getTests(self) -> list:
        return self.tests

    def showTable(self, table) -> None:
        buildenTable = table.build()
        print(buildenTable)

class Tester:
    def __init__(self, tests: list) -> None:
        if not isinstance(tests, list):
            tests = [tests]
        self.tests = tests
        self.testingFunctions = []

    def importScript(self, pathToScript: str) -> None:
        programFolder = os.path.split(__file__)[0]

        scriptName = os.path.split(pathToScript)[1]

        if not scriptName in os.listdir(programFolder) and scriptName.endswith(".py"):
            script = import_module(os.path.splitext(scriptName)[0])

        else:
            scriptContent = pathlib.Path(pathToScript).read_text()
            pathlib.Path(os.path.join(programFolder, scriptName)).write_text(scriptContent)
            invalidate_caches()
            script = import_module(os.path.splitext(scriptName))
        
        for name in dir(script):
            if isinstance(getattr(script, name), testRunner):
                self.testingFunctions.append(getattr(script, name))

    def makeTests(self, iters: int) -> None:
        self.results = {}
        for test in self.tests:
            if not self.testingFunctions == []:
                results = {}
                for function in self.testingFunctions:
                    if test == "memory":
                        result = function(test)
                    else:
                        result = [function(test) for iter in range(iters)]
                    results.update({function.name: result})
                self.results.update({test: results})
            else:
                if test == "memory":
                    self.results.update({test: {"": ""}})
                else:
                    self.results.update({test: {"": ["" for i in range(iters)]}})

    def getResults(self) -> dict:
        return self.results

class Table:
    def __init__(self, results: dict, iters: int) -> None:
        tests = ["Tests."]
        funcNames = ["Functions."]
        iters_ = [[f"Iteration {i + 1}."] for i in range(iters)]
        for test, functionNames in results.items():
            tests.append(test)
            for functionName, results_ in functionNames.items():
                funcNames.append(functionName)
                if not test == "memory":
                    for iteration, result in enumerate(results_):
                        iters_[iteration].append(str(result))


        testLen = max([len(test) for test in tests])
        namesLen = max([len(name) for name in funcNames])
        itersLens = [max([len(res) for res in iter]) for iter in iters_]
        tableLen = testLen + namesLen + sum(itersLens) + 3 + iters


        self.table = ["-" * tableLen + "\n",
        f"|%{testLen}s|%{namesLen}s|" % ("Tests.", "Functions.") + "".join([f"%{len}s|" % iters_[i][0] for i, len in enumerate(itersLens)]) + "\n"
        , "-" * tableLen + "\n"]

        for test, functionNames in results.items():
            self.table.append(f"|%{testLen}s|" % test)
            for row, functionName, results in zip(range(iters), functionNames, functionNames.values()):
                if row:
                    self.table.append(f"|{' ' * testLen}|")
                self.table.append(f"%{namesLen}s|" % functionName)
                if test == "memory":
                    self.table.append(f"%{sum(itersLens) + iters - 1}s|" % results)
                else:
                    for i, result in enumerate(results):
                        self.table.append(f"%{itersLens[i]}s|" % result)

                self.table.append("\n")
            self.table.append("-" * tableLen + "\n")



    def build(self) -> str:
        return "".join(self.table)

def main():
    cliManager = CLI()

    tester = Tester(cliManager.getTests())
    tester.importScript(cliManager.module)
    tester.makeTests(cliManager.iters)

    table = Table(tester.getResults(), cliManager.iters)

    cliManager.showTable(table)

if __name__ == "__main__":
    main()
