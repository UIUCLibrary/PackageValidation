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
            for error in runner.errors:
                print(error)
    else:
        print("All tests PASSED")
    print("=====================")


if __name__ == '__main__':
    main()
