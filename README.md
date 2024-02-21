# junit converter
Python Python JUnit Converter Engine

## command line arguments for junitconv.py
junitconv.py uses following command line arguments:

| Argument | Default | Description |
| --- | --- | --- |
| --input | testSummary.json | abs/rel path to json report input |
| --output | testSummary-junit.xml | abs/rel path to junit xml output |

if no input is given, junitconv tries to find testSummary.json in the current working directory.
