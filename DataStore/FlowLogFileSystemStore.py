from datastore.FlowLogStore import FlowLogStore

class FlowLogFileSystemStore(FlowLogStore):

    def __init__(self, filePath):
        self.filePath = filePath
    
    def getStream(self, fileName: str):
        return open(self.filePath + fileName, 'r')
    
    
