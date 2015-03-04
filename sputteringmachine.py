from machine import Machine
from event import Event

import threading

class SputteringFinishedEvent(Event):
    def __init__(self, productionLine):
        super(SputteringFinishedEvent, self).__init__('SputteringFinishedEvent', productionLine)

    def PollNotBusy(self, time):
        # TODO: At this point we should check the machines from other production lines
        lacquerCoatingMachine = self.productionLine.GetLacquerCoatingMachine()
        while lacquerCoatingMachine.IsBusy():
            pass

        # Set the time to the actual time
        time = self.productionLine.GetTime()

        # The machine is not busy anymore, transfer the batch
        lacquerCoatingMachine.Touch(time)

        # Set the sputtering machine to a non-busy state
        # (we assume that the sputtering machine is busy)
        sputteringMachine = self.productionLine.GetSputteringMachine()

        assert sputteringMachine.IsBusy()

        # Indicate that the machine is not busy
        sputteringMachine.SetNonBusy()

        # Indicate that the machine now is empty
        sputteringMachine.SetEmpty()

    def Handle(self, time):
        # Start polling the lacquer coating machine for non-busy state
        pollThread = threading.Thread(target=self.PollNotBusy, args=[time])
        pollThread.setDaemon(True)
        pollThread.start()

class SputteringMachine(Machine):
    def __init__(self, productionLine):
        super(SputteringMachine, self).__init__(productionLine)

        # At start there are 0 elements in the batch
        self.elementsInBatch = 0

        # At start this machine is not busy
        self.isBusy = False

        # Fetch the batch size from the configuration
        self.batchSize = self.productionLine.GetConfiguration().GetBatchSize()

    def SetEmpty(self):
        assert self.elementsInBatch > 0

        self.elementsInBatch = 0

    def SetNonBusy(self):
        # This should always hold
        assert self.IsBusy()

        self.isBusy = False

    def SetBusy(self):
        # This should always hold
        assert not self.IsBusy()

        self.isBusy = True

    def IsFull(self):
        assert self.elementsInBatch <= self.batchSize

        return self.elementsInBatch == self.batchSize

    def IsBusy(self):
        return self.isBusy

    def GetElementsInBatch(self):
        return self.elementsInBatch

    def Touch(self, time):
        # We can immediately transfer every element from the input buffer into the batch
        inputBufferMachine = self.productionLine.GetInputBufferMachine()

        # Set the elements in batch
        elementsInBuffer = inputBufferMachine.GetElementsInBuffer()

        # Check if we're not overshooting, in which case we only add up to the batch size allows
        if self.elementsInBatch + elementsInBuffer > self.batchSize:
            elementsToAdd  = self.batchSize - self.elementsInBatch
            elementsToTake = (self.elementsInBatch + elementsInBuffer) - self.batchSize
        else:
            elementsToAdd  = elementsInBuffer
            elementsToTake = elementsInBuffer

        # Take a number of elements from the input buffer
        inputBufferMachine.Take(elementsToTake)

        # Add the elements from the input buffer to the batch
        self.elementsInBatch += elementsToAdd

        # We need to check if the batch is full, if so, we schedule a new event indicating that the sputtering
        # is done
        if self.IsFull():
            # TODO: We currently use 2000ms for scheduling a new InjectionMoldingFinishedEvent, this should be modelled
            # using some function
            t1 = time + 2000

            # Add the event
            self.productionLine.GetSimulation().AddEvent(t1, SputteringFinishedEvent(self.productionLine))

            # Indicate that this machine is busy
            self.SetBusy()