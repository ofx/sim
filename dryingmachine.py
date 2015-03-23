from machine import Machine
from event import Event

import threading

class DryingFinishedEvent(Event):
    def __init__(self, productionLine, dryingMachine):
        super(DryingFinishedEvent, self).__init__('DryingFinishedEvent', productionLine)

        # Store a reference to the drying machine associated with this event
        self.dryingMachine = dryingMachine

    def Empty(self, time):
        # TODO: At this point we should cross reference the output buffer at the other production line
        outputBufferMachine = self.productionLine.GetOutputBufferMachine()

        # We keep going until we're empty
        while not self.dryingMachine.IsEmpty():
            # If the output buffer is not full, we can take a number of elements from the batch and store it in the output buffer
            if not outputBufferMachine.IsFull():
                spaceLeft = outputBufferMachine.GetSpaceLeft()

                # Take the amount of elements that is left in the output buffer from the batch (or up to the point
                # where the batch is empty, in which case we can stop)
                for i in range(0, spaceLeft):
                    # We should stop if the batch is empty
                    if not self.dryingMachine.IsEmpty():
                        # Take one from the drying machine
                        self.dryingMachine.TakeOne()

                        # Store it in the output buffer
                        # We're not actually using time here
                        outputBufferMachine.Touch(time)

            # Wait for the printing machine to be non-busy
            while outputBufferMachine.GetPrintingMachine().IsBusy():
                pass

            # Set the time to the actual time
            time = self.productionLine.GetTime()

            # Touch the printing machine that is associated with the output buffer
            outputBufferMachine.GetPrintingMachine().Touch(time)

        # Empty the output buffer
        elementsInOutputBuffer = outputBufferMachine.GetElementsInBuffer()

        # Transfer every element
        for i in range(0, elementsInOutputBuffer):
            # Wait until the printing machine is finished
            while outputBufferMachine.GetPrintingMachine().IsBusy():
                pass

            # Set the time to the actual time
            time = self.productionLine.GetTime()

            # Touch the printing machine
            outputBufferMachine.GetPrintingMachine().Touch(time)

        # Indicate that we're done drying
        self.dryingMachine.SetNonBusy()

    def Handle(self, time):
        # Empty the drying machine
        pollThread = threading.Thread(target=self.Empty, args=[time])
        pollThread.setDaemon(True)
        pollThread.start()

class DryingMachine(Machine):
    def __init__(self, productionLine):
        super(DryingMachine, self).__init__(productionLine)

        # At start, we're not busy
        self.isBusy = False

        # Batch size (please not that this should be equal to every other batch size, it might be
        # more convenient to store this at some other place)
        self.batchSize = self.productionLine.GetConfiguration().GetBatchSize()

        # At start we don't have elements in our batch
        self.elementsInBatch = 0

    def GetElementsInBatch(self):
        return self.elementsInBatch

    def SetBusy(self):
        # We may assume that we're not busy
        #assert not self.isBusy

        self.isBusy = True

    def SetNonBusy(self):
        # We may assume that we're busy
        #assert self.isBusy

        self.isBusy = False

    def IsBusy(self):
        return self.isBusy

    def SetEmpty(self):
        #assert self.elementsInBatch > 0

        self.elementsInBatch = 0

    def IsEmpty(self):
        return self.elementsInBatch == 0

    def TransferBatch(self):
        # If this assertion fails, this means that we didn't do a good enough job at some other point in the code
        #assert not self.IsBusy()

        # The assertion failing means that other code is unstable
        #assert self.IsEmpty()

        # Set the elements in batch to maximum
        self.elementsInBatch = self.batchSize

    def TakeOne(self):
        # Assume that the machine is not empty, if so, we may assume that we have written unstable code elsewhere
        assert not self.IsEmpty()

        self.elementsInBatch -= 1

    def Touch(self, time):
        '''
        In case we're touched, we transfer the batch from the previous machine to the current machine,
        this means that this machine should not be busy, and that after accepting the transferred batch,
        we schedule a new event which indicates that the drying process is done.
        '''

        # Accept the batch
        self.TransferBatch()

        # Drying takes 3 mins for the whole batch
        t1 = time + 180000

        # Indicate that the machine is busy
        self.SetBusy()

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, DryingFinishedEvent(self.productionLine, self))