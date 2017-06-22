import argparse
import os
import logging
import sys

import itertools

from dcc_qc import hathi_qc_runner
from dcc_qc import configure_logging, reports


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory of packages to be validated")
    parser.add_argument("--save_report", dest="report_name", help="Save report to a file")
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", help="Save debug information to a file")

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
    configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)
    logger.debug("Loading HathiQCRunner() with {}".format(args.path))
    runner = hathi_qc_runner.HathiQCRunner(args.path)
    logger.debug("Running HathiQCRunner()")
    runner.run()
    report_results(runner, file=args.report_name)


def report_results(runner, file=None):
    manager = reports.ReportManager()

    console_reporter = reports.ConsoleHandler()
    manager.add_handler(console_reporter)

    if file:
        file_reporter = reports.FileHandler(file, overwrite=True)
        manager.add_handler(file_reporter)

    # Summary
    manager.write_line("=====================")
    manager.write_line("Summary:")
    manager.write_line("=====================")
    manager.write_line("Errors found: {}".format(len(runner.errors)))
    manager.write_line("=====================")
    if not runner.valid:
        manager.write_line("Validation Failed")
        if runner.errors:
            manager.write_line("Errors:")
            sorted_groups = sorted(runner.errors, key=lambda x: x.group)
            for i, (error_source, error_group) in enumerate(itertools.groupby(sorted_groups, key=lambda y: y.group)):

                manager.write_line("{}) {}".format(i + 1, error_source))
                sorter_source = sorted(error_group, key=lambda x: x.source)
                foo = itertools.groupby(sorter_source, key=lambda y: y.source)
                for ia, source in enumerate(foo):
                    source_name, errors = source
                    manager.write_line("   > {}".format(source_name))
                    for errors in errors:
                        manager.write_line("         * {}".format(errors.message))
                    # for msg in msgs:
                    #     print(" *  {}".format(msg.message))
                    manager.write_line()
                manager.write_line()
    else:
        manager.write_line("All tests PASSED")
    manager.write_line("=====================")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()
