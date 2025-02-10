class FlowLogRecord:
    def __init__(self, dstPort, protocol):
        self.dstPort = dstPort
        self.protocol = protocol

    def __repr__(self):
        return f"dstPort: {self.dstPort}, protocol: {self.protocol}"