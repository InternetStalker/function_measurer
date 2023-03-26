from __future__ import annotations
import argparse
import pathlib

class CLI:
    possible_tests = ["runtime", "memory"]

    def __init__(self) -> None:
        argparser = argparse.ArgumentParser(
            prog = "tester",
            description = "Program for testing python modules.",
            fromfile_prefix_chars = "@"
            )
        argparser.add_argument(
            "module",
            type = str,
            help = "Given module for testing."
            )
        argparser.add_argument(
            "iters",
            type = int,
            help = "How many times module will be tested."
            )
        
        argparser.add_argument(
            "--csv",
            help = "Path to csv file where results would be saved.",
            default = None,
            action = "store"
        )

        arguments = argparser.parse_args()

        self.module = pathlib.Path(arguments.module)
        self.iters: int = arguments.iters
        self.tests: list[str] = arguments.tests
        self.save_to_csv = bool(arguments.csv)

        if self.save_to_csv:
            self.path_to_csv = pathlib.Path(arguments.csv)
        
        else:
            self.path_to_csv = None

        if not self.module.exists():
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")
        
        if self.iters < 1:
            raise ValueError("Iters argument must be over 1")

    def get_tests(self) -> list[str] | str:
        return self.tests
