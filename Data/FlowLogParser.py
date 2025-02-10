from typing import Type
from models.FlowLogRecord import FlowLogRecord

class FlowLogParser:

    def parse(self, record: str) -> Type[FlowLogRecord]:
        pass