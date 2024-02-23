import json
import os
from junit_xml import TestSuite, TestCase, to_xml_report_string

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
    test_suites = dict_to_testsuites(data)
    xml = to_xml_report_string(test_suites, prettyprint=pretty_print)
    print(f"Writing: {output_file}")
    with open(output_file, "w", encoding="UTF-8") as file:
        file.write(xml)

def dict_to_testsuites(data: dict) -> list[TestSuite]:
    def get_error_info(data: dict) -> str:
        if "resultMessage" in data:
            return data["resultMessage"]    
        if "debug" in data:
            if "longrepr" in data["debug"]:
                return data["debug"]["longrepr"]    
        return "Not available"

    test_suites: list[TestSuite] = list()
    for test in data["tests"]:
        test_cases = list()
        # following three fields are always defined
        name = test["name"]
        type = test["type"]
        result = test["result"]
        if result == "SKIPPED":
            # if result is SKIPPED
            # subtests are not available (in winfrieds testSummary.json)
            # append only one skipped testcase
            tc = TestCase(name)
            tc.add_skipped_info()
            test_cases.append(tc)
        else:
            # if result is FAILED or PASSED
            # subtests are available
            for subtest in test["tests"]:
                sub_name = subtest["name"]
                sub_result = subtest["result"]
                tc = TestCase(sub_name)
                tc.classname = type
                if sub_result == "FAILED":
                    tc.add_error_info(get_error_info(subtest))
                test_cases.append(tc)
        ts = TestSuite(name)
        ts.test_cases = test_cases
        test_suites.append(ts)
    return test_suites
