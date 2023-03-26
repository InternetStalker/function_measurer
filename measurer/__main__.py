from __future__ import annotations

from .result_tables import create_result_table, BaseResultTable
from .args import parse_cli_args
from .tester import Tester




def main():
    arguments = parse_cli_args()

    tester = Tester(arguments.iters)
    tester.import_script(arguments.module)
    tester.make_tests()

    table: BaseResultTable = create_result_table(
        tester.get_results(),
        arguments
        )
    
    table.show()


if __name__ == "__main__":
    main()
