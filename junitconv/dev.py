import glob
import os
from junitconv import run_convert

# this file is for development purposes only
# facilitates starting local test-examples

def start_tests():
    scan_dir = "../reports"
    #scan_dir = "../../tests"
    #scan_dir = "../../course-2023"

    dir = os.path.abspath(os.path.dirname(__file__))
    scan_dir = os.path.join(dir, scan_dir)
    flist = glob.glob("**/*.json", root_dir=scan_dir, recursive=True)
    c = 0
    for file in flist:
        c += 1
        root, ext = os.path.splitext(file)
        in_file = os.path.join(scan_dir, file)
        out_file = os.path.join(scan_dir, f"{root}.xml")
        print(f"# running # {c}")
        run_convert(in_file, out_file)

if __name__ == "__main__":
    start_tests()
