# -*- coding: utf-8 -*-
import os
import argparse
import pathlib

from rich.console import Console
from rich.table import Table
from importlib import import_module, invalidate_caches

from . import testRunner

class CLI:
    possibleTests = ["runtime", "memory"]

    def __init__(self) -> None:
        argparser = argparse.ArgumentParser("tester", description="Program for testing python modules.", fromfile_prefix_chars="@")
        argparser.add_argument("module", type=str, help="Given module for testing.")
        argparser.add_argument("iters", type=int, help="How many times module will be tested.")
        argparser.add_argument("tests", choices=CLI.possibleTests, help="Tests those measurer should do with given module.", nargs="+")
        arguments = argparser.parse_args()

        self.module = os.path.abspath(arguments.module)
        self.iters = arguments.iters
        self.tests = arguments.tests

        if not os.access(self.module, os.F_OK):
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")

    def getTests(self) -> list[str] | str:
        return self.tests

    def showTable(self, table: Table) -> None:
        console = Console()
        console.print(table)

class Tester:
    def __init__(self, tests: list[str] | str) -> None:
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
        self.results: dict[str: dict[str: list]] = {}
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

    def create_table(self, iters: int) -> Table:
        table = Table()
        table.add_column("Tests.")
        table.add_column("Functions.")
        for i in range(1, iters+1):
            table.add_column(f"Iteration {i}.")

        for test, function_names in self.results.items():
            for name in function_names:
                table.add_row(test, name, *[str(value) for value in function_names.values()])

        return table

def main():
    cliManager = CLI()

    tester = Tester(cliManager.getTests())
    tester.importScript(cliManager.module)
    tester.makeTests(cliManager.iters)

    table = tester.create_table(cliManager.iters)

    cliManager.showTable(table)

if __name__ == "__main__":
    main()
