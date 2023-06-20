from __future__ import annotations
import argparse
import pathlib
import typing


@dataclass(slots=true, frozen=true)
class Arguments:
    path: pathlib.Path
    iters: int
    path_to_csv: pathlib.Path | None

    def save_to_csv(self) -> bool:
        return bool(self.path_to_csv)


def parse_cli_args() -> Arguments:
    argparser = argparse.ArgumentParser(
        prog = "tester",
        description = "Program for testing python modules.",
        fromfile_prefix_chars = "@"
        )

    argparser.add_argument(
        "module",
        type = pathlib.Path,
        help = "Given module for testing."
        )

    argparser.add_argument(
        "iters",
        type = int,
        help = "How many times module will be tested."
        )
    
    argparser.add_argument(
        "--csv",
        help = "Path to csv file where results will be saved.",
        type = pathlib.Path 
        default = None
        )

    arguments = argparser.parse_args()

    return Arguments(arguments.module, arguments.iters, arguments.path_to_csv)
