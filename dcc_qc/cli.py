import argparse
import os
import logging
import sys
from dcc_qc import hathi_qc_runner

logger = logging.getLogger(__package__)


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
    def configure_logger(debug_mode=False, log_file=None):
        logger.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        std_handler = logging.StreamHandler(sys.stdout)
        if log_file:
            file_handler = logging.FileHandler(filename=log_file)
            logger.addHandler(file_handler)
        if debug_mode:
            std_handler.setLevel(logging.DEBUG)
            std_handler.setFormatter(debug_formatter)
        else:
            std_handler.setLevel(logging.INFO)

        # std_handler.setFormatter(debug_formatter)

        logger.addHandler(std_handler)

    args = get_args()

    arg_errors = list(find_arg_errors(args))
    if arg_errors:
        for er in arg_errors:
            print(er, file=sys.stderr)
        sys.exit(1)
    configure_logger(debug_mode=args.debug)
    logger.debug("Loading HathiQCRunner() with {}".format(args.path))
    runner = hathi_qc_runner.HathiQCRunner(args.path)
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
            for i, error in enumerate(sorted(runner.errors)):
                print("{}) {}".format(i+1, error))
    else:
        print("All tests PASSED")
    print("=====================")


if __name__ == '__main__':
    main()
