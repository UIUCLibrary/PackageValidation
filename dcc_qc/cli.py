import argparse
import os
import logging
import sys

import itertools
import dcc_qc
from dcc_qc import hathi_qc_runner
from dcc_qc.runner import Runner
from dcc_qc import configure_logging, reports, profiles


def get_parser():
    parser = argparse.ArgumentParser()

    command_group = parser.add_mutually_exclusive_group()

    command_group.add_argument("--list-profiles", dest="list_profiles", action="store_true", help="List available package profiles")
    command_group.add_argument("--version", action="version", version=dcc_qc.__version__)

    process_group = command_group.add_argument_group()
    # process_group = command_group.add_argument_group()
    process_group.add_argument("profile", nargs="?", help="Type of package to validate")
    process_group.add_argument("path", nargs="?", help="Directory of packages to be validated")
    process_group.add_argument("--save-report", dest="report_name", help="Save report to a file")
    debug_group = process_group.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")
    return parser

def get_args(parser):

    args = parser.parse_args()

    return args


def find_arg_errors(args):
    if args.path:
        if not os.path.exists(args.path):
            yield "Error: \"{}\" is not a valid path".format(args.path)

    if args.profile and not args.path:
        yield "Error missing path"


def list_profiles():
    profiles = dcc_qc.profiles.get_available()
    for profile in profiles:
        print(profile)


def main():
    logger = logging.getLogger(__name__)
    parser = get_parser()
    args = get_args(parser)

    arg_errors = list(find_arg_errors(args))
    if arg_errors:
        for er in arg_errors:
            print(er, file=sys.stderr)
        sys.exit(1)
    if args.list_profiles:
        list_profiles()
        sys.exit()
    configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)
    logger.debug("Using args: {}".format(args))

    ###################################################
    if args.profile:
        try:
            profile = profiles.get_profile(args.profile)
        except KeyError as e:
            logger.error("Invalid profile {}".format(e))
            sys.exit(1)

        runner = Runner(args.path, profile)
        logger.debug("Running HathiQCRunner()")
        runner.run()
        report_results(runner, file=args.report_name)
    else:
        parser.print_help()


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
