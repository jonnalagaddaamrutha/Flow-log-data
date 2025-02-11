from datastore.FlowLogFileSystemStore import FlowLogFileSystemStore
from datastore.LookupTable import LookupTable
from tagger.FlowLogTagger import FlowLogTagger
from dataparser.AmazonVpcFlowLogParser import AmazonVpcFlowLogParser

if __name__ == "__main__":
    fileDatastore = FlowLogFileSystemStore("./data/")
    parser = AmazonVpcFlowLogParser()
    lookup = LookupTable("./data/dstport_protocol_to_tag.csv")
    flowLogTagger = FlowLogTagger(fileDatastore, parser, lookup)
    flowLogTagger.process("flow_log_sample_1.txt")
    flowLogTagger.getTagCountFile("./output/tag_count.csv", ["Tag", "Count"])
    flowLogTagger.getDstPortProtocolCountFile("./output/dstport_protocol_count.csv", ["Port", "Protocol", "Count"])