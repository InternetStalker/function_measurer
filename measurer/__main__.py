from __future__ import annotations
import sys

from .result_tables import create_result_table, BaseResultTable
from .args import parse_cli_args
from .tester import Tester




def main():
    try:
        arguments = parse_cli_args()
    
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)

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
