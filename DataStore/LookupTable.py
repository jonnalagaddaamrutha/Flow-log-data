from utilities import createMapFromCsv, getProtocolToNumberMap
from typing import List

class LookupTable:
    def __init__(self, dstPortProtocolTagFilePath: str):
        self.protocolToNumbersMap = getProtocolToNumberMap()
        self.dstPortProtocolToTagMap = createMapFromCsv(dstPortProtocolTagFilePath, [0, 1], 2, 3, self.generateDstPortProtocolKey)


    def get(self, key: str) -> str:
        key = key.lower()
        return self.dstPortProtocolToTagMap[key]
    
    def generateDstPortProtocolKey(self, keyIndices: List[int], row) -> str:
        return f"{row[0].lower().strip()}_{self.protocolToNumbersMap[row[1].lower().strip()]}"
    
    
    