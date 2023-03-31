from __future__ import annotations
import argparse
import pathlib


class Arguments:
    def __init__(self, module: str, path_to_csv: str | None) -> None:
        self._module: pathlib.Path = pathlib.Path(module)
        self._path_to_csv: pathlib.Path | None = pathlib.Path(path_to_csv) if path_to_csv is not None else None

        if not self._module.exists():
            raise FileNotFoundError(f"File doesn't exists. Path: {self.module}")
    
    @property
    def module(self) -> pathlib.Path:
        return self._module
    
    @property
    def path_to_csv(self) -> pathlib.Path:
        if self.path_to_csv is None:
            raise TypeError("There is no csv provided")

        return self._path_to_csv # type: ignore

    @property
    def save_to_csv(self) -> bool:
        return bool(self._path_to_csv)



def parse_cli_args() -> Arguments:
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
        "--csv",
        help = "Path to csv file where results will be saved.",
        )

    arguments = argparser.parse_args()

    return Arguments(arguments.module, arguments.csv)
