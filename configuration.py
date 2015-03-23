class Configuration:
    def __init__(self, bufferSize, batchSize, injectionMoldingMachineOneOld, injectionMoldingMachineTwoOld, dyeCoatingMachineOld):
        self.bufferSize = bufferSize
        self.batchSize  = batchSize
        self.injectionMoldingMachineOneOld = injectionMoldingMachineOneOld
        self.injectionMoldingMachineTwoOld = injectionMoldingMachineTwoOld
        self.dyeCoatingMachineOld = dyeCoatingMachineOld

    def GetDyeCoatingMachineOld(self):
        return self.dyeCoatingMachineOld

    def GetInjectionMoldingMachineOneOld(self):
        return self.injectionMoldingMachineOneOld

    def GetInjectionMoldingMachineTwoOld(self):
        return self.injectionMoldingMachineTwoOld

    def GetBufferSize(self):
        return self.bufferSize

    def GetBatchSize(self):
        return self.batchSize
