from __future__ import annotations

from .result_tables import create_result_table, BaseResultTable
from .cli import CLI
from .tester import Tester




def main():
    CliManager = CLI()

    tester = Tester(CliManager.get_tests(), CliManager.iters)
    tester.import_script(CliManager.module)
    tester.make_tests()

    table: BaseResultTable = create_result_table(
        CliManager.iters,
        tester.get_results(),
        CliManager.save_to_csv,
        CliManager.path_to_csv
        )
    
    table.show()


if __name__ == "__main__":
    main()
