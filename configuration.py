class Configuration:
    def __init__(self, bufferSize, batchSize):
        self.bufferSize = bufferSize
        self.batchSize  = batchSize

    def GetBufferSize(self):
        return self.bufferSize

    def GetBatchSize(self):
        return self.batchSize