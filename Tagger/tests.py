import random
import csv
from datastore.LookupTable import LookupTable
from datastore.FlowLogFileSystemStore import FlowLogFileSystemStore
from dataparser.AmazonVpcFlowLogParser import AmazonVpcFlowLogParser
from tagger.FlowLogTagger import FlowLogTagger
from utilities import getNumberToProtocolMap

def testLookupTableCreation():
    lookup = LookupTable("./data/dstport_protocol_to_tag.csv")
    print(lookup.dstPortProtocolToTagMap)


def testParseInvalidFlowLog():
    parser = AmazonVpcFlowLogParser()
    fileDatastore = FlowLogFileSystemStore("./data/")
    stream = fileDatastore.getStream("test_invalid_flow_log.txt")
    try:
        for line in stream:
            parser.parse(line)
    except Exception as e:
        print(f"Exception {e} raised as expected")
    finally:
        if hasattr(stream, 'close'):
            stream.close()


def testFlowLogTagger():
    fileDatastore = FlowLogFileSystemStore("./data/")
    parser = AmazonVpcFlowLogParser()
    lookup = LookupTable("./data/dstport_protocol_to_tag.csv")
    flowLogTagger = FlowLogTagger(fileDatastore, parser, lookup)
    flowLogTagger.process("flow_log_sample_1.txt")
    flowLogTagger.getTagCountFile("./output/tag_count.csv", ["Tag", "Count"])
    flowLogTagger.getDstPortProtocolCountFile("./output/dstport_protocol_count.csv", ["Port", "Protocol", "Count"])


def testLargeFlowLogFile():
    createLargeFlowLogsFile("./data/test_large_log_file.txt")

    fileDatastore = FlowLogFileSystemStore("./data/")
    parser = AmazonVpcFlowLogParser()
    lookup = LookupTable("./data/dstport_protocol_to_tag.csv")
    flowLogTagger = FlowLogTagger(fileDatastore, parser, lookup)
    flowLogTagger.process("test_large_log_file.txt")
    flowLogTagger.getTagCountFile("./output/large_tag_count.csv", ["Tag", "Count"])
    flowLogTagger.getDstPortProtocolCountFile("./output/large_dstport_protocol_count.csv", ["Port", "Protocol", "Count"])

def testLargeFlowLogFileAndLargeLookup():
    createLargeFlowLogsFile("./data/test_large_log_file.txt")
    createLargeLookupTable("./data/test_large_lookup_table.csv")

    fileDatastore = FlowLogFileSystemStore("./data/")
    parser = AmazonVpcFlowLogParser()
    lookup = LookupTable("./data/test_large_lookup_table.csv")
    flowLogTagger = FlowLogTagger(fileDatastore, parser, lookup)
    flowLogTagger.process("test_large_log_file.txt")
    flowLogTagger.getTagCountFile("./output/large_tag_count.csv", ["Tag", "Count"])
    flowLogTagger.getDstPortProtocolCountFile("./output/large_dstport_protocol_count.csv", ["Port", "Protocol", "Count"])

    

def createLargeLookupTable(lookupTablePath: str) -> None:
    tags = ["sv_P1", "sv_P2", "SV_P3", "sv_P4", "sv_P5", "email"]
    numberToProtocolMap = getNumberToProtocolMap()
    with open(lookupTablePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["dstport","protocol","tag"])
        for i in range(10000):
            dstPort = random.randint(1, 65535)
            protocol = str(random.randint(0, 146))
            tag = random.choice(tags)
            row = [dstPort, numberToProtocolMap[protocol], tag]
            writer.writerow(row)
    print(f"CSV file '{lookupTablePath}' has been created.")


def createLargeFlowLogsFile(flowLogFilePath: str) -> None:
    sampleLogs = [
        "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK ",
        "2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK ",
        "2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK ",
        "2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK ",
        "2 123456789012 eni-7i8j9k0l 172.16.0.101 192.0.2.203 993 49157 6 8 5000 1620140761 1620140821 ACCEPT OK ",
        "2 123456789012 eni-6m7n8o9p 10.0.2.200 198.51.100.4 143 49158 6 18 14000 1620140761 1620140821 ACCEPT OK ",
        "2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 80 6 10 5000 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-1a2b3c4d 203.0.113.12 192.168.0.1 80 1024 6 12 6000 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-1a2b3c4d 10.0.1.102 172.217.7.228 1030 443 6 8 4000 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK ",
        "2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-1a2b3c4d 192.168.1.6 87.250.250.242 49152 110 6 5 2500 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-2d2e2f3g 192.168.2.7 77.88.55.80 49153 993 6 7 3500 1620140661 1620140721 ACCEPT OK ",
        "2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 143 6 9 4500 1620140661 1620140721 ACCEPT OK"
    ]

    # Write to the text file
    with open(flowLogFilePath, mode="w") as file:
        for i in range(10000):
            # Add a newline character after each string and write to file
            file.writelines(line + "\n" for line in sampleLogs)

    print(f"Text file '{flowLogFilePath}' has been created.")


if __name__ == "__main__":
    print("\nTest 1: testLookupTableCreation\n")
    testLookupTableCreation()
    
    print("\nTest 2: testFlowLogTagger\n")
    testFlowLogTagger()
    
    print("\nTest 3: testParseInvalidFlowLog\n")
    testParseInvalidFlowLog()
    
    print("\nTest 4: testLargeFlowLogFile\n")
    testLargeFlowLogFile()
    
    print("\nTest 5: testLargeFlowLogFileAndLargeLookup\n")
    testLargeFlowLogFileAndLargeLookup()
