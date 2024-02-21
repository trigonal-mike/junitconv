import argparse
import os
from convert import convert_now

DEFAULT_INPUT = "testSummary.json"
DEFAULT_OUTPUT = "testSummary-junit.xml"

def run_convert(input_file, output_file):
    try:
        convert_now(input_file, output_file)
    except Exception as e:
        print(e)
        print("An error occurred")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT, help="abs/rel path to json report input")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="abs/rel path to junit xml output")
    args = parser.parse_args()
    run_convert(args.input, args.output)
