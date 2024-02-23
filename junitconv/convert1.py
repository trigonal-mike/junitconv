import json
import os
from junitparser import TestCase, TestSuite, JUnitXml, Skipped, Error

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
    print(f"Writing: {output_file}")
    xml = JUnitXml()
    for suite in test_suites:
        xml.add_testsuite(suite)
    xml.write(output_file, pretty=pretty_print)

def dict_to_testsuites(data: dict) -> list[TestSuite]:
    def get_debug_info(data: dict) -> str:
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
            tc.result = [Skipped(get_debug_info(test))]
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
                    tc.result = [Error(get_debug_info(subtest))]
                test_cases.append(tc)
        ts = TestSuite(name)
        for case in test_cases:
            ts.add_testcase(case)
        test_suites.append(ts)
    return test_suites
