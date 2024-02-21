import os
from junitconv import run_convert

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    input_file = "../reports/testSummary.json"
    output_file = "../reports/testSummary-junit.xml"

    dir = os.path.abspath(os.path.dirname(__file__))
    in_file = os.path.join(dir, input_file)
    out_file = os.path.join(dir, output_file)
    run_convert(in_file, out_file)

if __name__ == "__main__":
    start_tests()
