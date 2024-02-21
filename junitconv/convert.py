import json
import os
from junit_xml import TestSuite, TestCase

def normalize_path(path):
    cwd = os.getcwd()
    if path is not None and not os.path.isabs(path):
        path = os.path.join(cwd, path)
    path = os.path.abspath(path)
    return path

def convert_now(input_file: str, output_file: str):
    pretty_print = True
    input_file = normalize_path(input_file)
    output_file = normalize_path(output_file)

    if not os.path.exists(input_file):
        raise Exception(f"ERROR: input file does not exist: {input_file}")
    
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        print(f"Creating directory: {output_dir}")
        os.makedirs(output_dir)

    with open(input_file) as file:
        data = json.load(file)

    _name = data["name"]
    _timestamp = data["timestamp"]
    _duration = data["duration"]

    c = 0
    _test_cases = list()
    for test in data["tests"]:
        for subtest in test["tests"]:
            c += 1
            result = subtest["result"]
            tc = TestCase(
                name=subtest["name"],
                timestamp=subtest["debug"]["timestamp"],
            )
            if result == "FAILED":
                tc.add_error_info(subtest["debug"]["longrepr"])
            elif result == "SKIPPED":
                tc.add_skipped_info(subtest["debug"]["longrepr"])
            _test_cases.append(tc)

    ts = TestSuite(
        name=_name,
        timestamp=_timestamp,
        test_cases=_test_cases,
    )
    xml = TestSuite.to_xml_string([ts], prettyprint=pretty_print)
    print(f"Writing: {output_file}")
    with open(output_file, "w") as file:
        file.write(xml)
    print(f"{c} TestCases converted!")
