from typing import Type, List
from models.FlowLogRecord import FlowLogRecord
from datastore.LookupTable import LookupTable
from datastore.FlowLogStore import FlowLogStore
from dataparser.FlowLogParser import FlowLogParser
from utilities import createCsvFromMap , getNumberToProtocolMap, createCsvFromList

class FlowLogTagger: # have vanilla functions instead of a class?
    def __init__(self, flowLogStore: Type[FlowLogStore], flowLogParser: Type[FlowLogParser], lookupTable: Type[LookupTable]):
        self.logStore = flowLogStore
        self.parser = flowLogParser
        self.lookup = lookupTable
        self.tagCountMap = {"untagged": 0}
        self.dstPortProtocolCountMap = {}
        self.numberToProtocolMap = getNumberToProtocolMap()

    def process(self, fileName: str):
        stream = self.logStore.getStream(fileName)
        try:
            for line in stream:
                self.processLine(line)
        finally:
            if hasattr(stream, 'close'):
                stream.close()
        
    def processLine(self, line): 
        try:
            # print("line: ", line)
            flowLogRecord = self.parser.parse(line)
            # print("flowLogRecord: ", flowLogRecord)
            self.tagRecord(flowLogRecord)
        except Exception as e:
            print("error: ", e)

    
    def tagRecord(self, record: Type[FlowLogRecord]):
        dstPortProtocolKey = self.getKey(record.dstPort, record.protocol)
        
        if dstPortProtocolKey not in self.dstPortProtocolCountMap:
            self.dstPortProtocolCountMap[dstPortProtocolKey] = 0
        self.dstPortProtocolCountMap[dstPortProtocolKey] += 1
        
        try:
            tag = self.lookup.get(dstPortProtocolKey)
            if tag not in self.tagCountMap:
                self.tagCountMap[tag] = 0
            self.tagCountMap[tag] += 1
        except KeyError as ke:
            self.tagCountMap["untagged"] += 1
        
        


    def getKey(self, dstPort: str, protocol: str)-> str:
        return str(dstPort) + "_" + str(protocol)
    
    def getTagCountFile(self, outputFileName: str, fieldNames: List[str]):
        createCsvFromMap(self.tagCountMap, outputFileName, fieldNames)

    def getDstPortProtocolCountFile(self, outputFileName: str, fieldNames: List[str]):
        dstPortProtocolTagList = []
        for key in self.dstPortProtocolCountMap:
            row = []
            port, protocol = key.split('_')
            row.append(port)
            row.append(self.numberToProtocolMap[protocol])
            row.append(self.dstPortProtocolCountMap[key])
            dstPortProtocolTagList.append(row)

        createCsvFromList(dstPortProtocolTagList, outputFileName, fieldNames)

    