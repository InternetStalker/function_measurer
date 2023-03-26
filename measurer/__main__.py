from __future__ import annotations

from .result_tables import create_result_table, BaseResultTable
from .args import parse_cli_args
from .tester import Tester




def main():
    argumets = parse_cli_args()

    tester = Tester(argumets.iters)
    tester.import_script(argumets.module)
    tester.make_tests()

    table: BaseResultTable = create_result_table(
        argumets.iters,
        tester.get_results(),
        argumets.save_to_csv,
        argumets.path_to_csv
        )
    
    table.show()


if __name__ == "__main__":
    main()
