from dataparser.FlowLogParser import FlowLogParser
from typing import Type
from models.FlowLogRecord import FlowLogRecord
from models.AmazonVpcFlowLogRecord import AmazonVpcFlowLogRecord
import dataparser.FlowLogValidator as flv

class AmazonVpcFlowLogParser(FlowLogParser):
    
    def parse(self, line: str) -> Type[FlowLogRecord]:
        columns = list(map(lambda x: x.strip(), line.strip().split(' ')))
        if not flv.validateAmazonVpcFlowLogRecord(columns):
            raise Exception(f"invalid format: {columns}")
        flowLogRecordObject = AmazonVpcFlowLogRecord(int(columns[6]), int(columns[7]))
        return flowLogRecordObject
