# Flow Log Tagger

## Overview
The Flow Log Tagger parses flow log data and maps each row to a tag based on a lookup table. The lookup table has 3 columns, dstport, protocol and tag. The dstport and protocol combination decide what tag can be applied.
Generates tag count and port protocol count as csv files.
The tagger is built in an extensible manner following SOLID principles to be able to support different kind of sources for flow logs if necessary and not limited to flow logs from a single cloud provider.

## Assumptions and Implementation
As of now, the generated insights(tag count and port-protocol count) are simply stored as csv files. But the project can be easily modified to store them in the desired data store.
Similarly, the controller component is not implemented as of now. The run.py file simulates the flow log processing and tagging using a sample flow log file and lookup table. 
The project assumes the Amazon vpc flow log input file to have only version 2 fields.

## Usage
### Prerequisites
1. setup a python virtualenv. This project was written using python 3.9.6

### Running the project
1. run tests using 
```python
python tests.py
```
2. run the project using 
```python
python run.py
```