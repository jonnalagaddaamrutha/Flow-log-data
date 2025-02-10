from models.FlowLogRecord import FlowLogRecord

class AmazonVpcFlowLogRecord(FlowLogRecord):
    def __init__(self, dstPort, protocol):
        super().__init__(dstPort, protocol)

