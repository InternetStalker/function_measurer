from __future__ import annotations
import csv
import pathlib

from rich.table import Table
from rich.console import Console
from abc import ABC, abstractmethod

from . import TestResult
from .args import Arguments


class AbstractResultTable(ABC):
    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def show(self) -> None:
        pass


class BaseResultTable(AbstractResultTable):
    def __init__(self, results: list[TestResult]) -> None:
        self._iters: int = max((res.iters for res in results))
        self._results = results
    
    def create_table(self) -> None:
        return super().create_table()
    
    def show(self) -> None:
        return super().show()


class ConsoleResultTable(BaseResultTable):
    def create_table(self) -> None:
        self.__table = Table()
        self.__table.add_column("Tests.")
        self.__table.add_column("Functions.")
        for i in range(1, self._iters+1):
            self.__table.add_column(f"Iteration {i}.")
        
        if self._iters > 1:
            self.__table.add_column("Average.")
        for result in self._results:
            res = []
            for i in range(self._iters):
                try:
                    res.append(result[i])
                except IndexError:
                    res.append("No data.")
            row = [
                result.test_mode,
                result.tested_name,
                res,
            ]

            if self._iters > 1:
                row.append(str(result.average))

            self.__table.add_row(*row)

    
    def show(self) -> None:
        console = Console()
        console.print(self.__table)


class CsvResultTable(BaseResultTable):
    def __init__(
        self,
        results: list[TestResult],
        path_to_csv: pathlib.Path
        ) -> None:
        super().__init__(results)
        self._path_to_csv = path_to_csv

    def create_table(self) -> None:
        self._fieldnames = (
            "Tests.",
            "Functions.",
            *(f"Iteration {i}." for i in range(1, self._iters+1))
        )
        if self._iters > 1:
            self._fieldnames = (
                *self._fieldnames,
                "Average."
            )

        for result in self._results:
            self._rows = []
            res = []
            for i in range(self._iters):
                try:
                    res.append(result[i])
                except IndexError:
                    res.append("No data.")
            row = {
                "Tests.": result.test_mode,
                "Functions.": result.tested_name,
                **{f"Iteration {i}.": str(value) for i, value in enumerate(res, start=1)},
            }

            if self._iters > 1:
                row["Average."] = str(result.average)

            self._rows.append(row)


    def show(self) -> None:
        with self._path_to_csv.open("w", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(file, self._fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(self._rows)


def create_result_table(
        results: list[TestResult],
        arguments: Arguments
    ) -> BaseResultTable:
    if arguments.save_to_csv:
        table = CsvResultTable(results, arguments.path_to_csv)
        table.create_table()

    else:
        table = ConsoleResultTable(results)
        table.create_table()
    
    return table

