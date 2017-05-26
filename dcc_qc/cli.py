import argparse
import os
import logging
import sys

import itertools

from dcc_qc import hathi_qc_runner
from dcc_qc import configure_logging


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory of packages to be validated")
    parser.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")

    return parser.parse_args()


def find_arg_errors(args):
    if not os.path.exists(args.path):
        yield "Error: \"{}\" is not a valid path".format(args.path)


def main():
    logger = logging.getLogger(__name__)
    args = get_args()

    arg_errors = list(find_arg_errors(args))
    if arg_errors:
        for er in arg_errors:
            print(er, file=sys.stderr)
        sys.exit(1)
    configure_logging.configure_logger(debug_mode=args.debug)
    logger.debug("Loading HathiQCRunner() with {}".format(args.path))
    runner = hathi_qc_runner.HathiQCRunner(args.path)
    logger.debug("Running HathiQCRunner()")
    runner.run()

    # Summary
    print("\n")
    print("=====================")
    print("Summary:")
    print("=====================")
    print("Errors found: {}".format(len(runner.errors)))
    print("=====================")
    if not runner.valid:
        print("Validation Failed")
        if runner.errors:
            print("Errors:")
            sorted_groups = sorted(runner.errors, key=lambda x: x.group)
            for i, (error_source, error_group) in enumerate(itertools.groupby(sorted_groups, key=lambda y: y.group)):

                print("{}) {}".format(i + 1, error_source))
                sorter_source = sorted(error_group, key=lambda x: x.source)
                foo = itertools.groupby(sorter_source, key=lambda y: y.source)
                for ia, source in enumerate(foo):
                    source_name, errors = source
                    print("   > {}".format(source_name))
                    for errors in errors:
                        print("         * {}".format(errors.message))
                    # for msg in msgs:
                    #     print(" *  {}".format(msg.message))
                    print()
                print()
    else:
        print("All tests PASSED")
    print("=====================")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()
