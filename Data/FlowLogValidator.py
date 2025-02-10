from typing import List

def validateAmazonVpcFlowLogRecord(values: List[str])-> bool:
    
    if len(values) != 14:
        print("Incorrect number of columns")
        return False
    
    try:
        version = int(values[0])
        dstPort = int(values[6])
        protocolNumber = int(values[7])
    except ValueError as e:
        print("Error: ", e)
        return False
    
    if version != 2:
        print("Invalid version number")
        return False
    
    if dstPort < 1 or dstPort > 65535:
        print("Invalid dst port number: ", dstPort)
        return False
    
    if protocolNumber < 0 or protocolNumber > 255:
        print("Invalid protocol number: ", protocolNumber)
        return False
    
    return True
