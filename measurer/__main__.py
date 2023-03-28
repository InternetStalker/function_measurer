from __future__ import annotations

from .result_tables import create_result_table, BaseResultTable
from .args import parse_cli_args
from .tester import Tester




def main():
    arguments = parse_cli_args()

    tester = Tester()
    tester.import_script(arguments.module)
    results = tester.do_tests()

    table: BaseResultTable = create_result_table(
        results,
        arguments
        )
    
    table.show()


if __name__ == "__main__":
    main()
