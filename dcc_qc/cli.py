import argparse
import os

import sys
from dcc_qc import hathi_qc_runner


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory of packages to be validated")
    return parser.parse_args()


def find_arg_errors(args):
    if not os.path.exists(args.path):
        yield "Error: \"{}\" is not a valid path".format(args.path)


def main():
    args = get_args()
    arg_errors = list(find_arg_errors(args))
    if arg_errors:
        for er in arg_errors:
            print(er, file=sys.stderr)
    errors = hathi_qc_runner.run(args.path)

    # Summary
    print("\n")
    print("================")
    print("Summary:")
    print("================")
    print("Errors found: {}".format(len(errors)))
    print("================")
    if errors:
        print("Errors:")
        for error in errors:
            print(error)
    else:
        print("All tests PASSED")
    print("================")


if __name__ == '__main__':
    main()
