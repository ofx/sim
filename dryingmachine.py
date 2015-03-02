from machine import Machine
from event import Event

import threading

class DryingFinishedEvent(Event):
    def __init__(self, productionLine):
        super(DryingFinishedEvent, self).__init__('DryingFinishedEvent', productionLine)

    def Handle(self, time):
        print 'Drying finished'

        # TODO: Handle whatever should happend with finishing

class DryingMachine(Machine):
    def __init__(self, productionLine):
        super(DryingMachine, self).__init__(productionLine)

        # At start, we're not busy
        self.isBusy = False

        # Batch size (please not that this should be equal to every other batch size, it might be
        # more convenient to store this at some other place)
        self.batchSize = 100

        # At start we don't have elements in our batch
        self.elementsInBatch = 0

    def GetElementsInBatch(self):
        return self.elementsInBatch

    def SetBusy(self):
        # We may assume that we're not busy
        assert not self.isBusy

        self.isBusy = True

    def SetNonBusy(self):
        # We may assume that we're busy
        assert self.isBusy

        self.isBusy = False

    def IsBusy(self):
        return self.isBusy

    def SetEmpty(self):
        assert self.elementsInBatch > 0

        self.elementsInBatch = 0

    def IsEmpty(self):
        return self.elementsInBatch == 0

    def TransferBatch(self):
        # If this assertion fails, this means that we didn't do a good enough job at some other point in the code
        assert not self.IsBusy()

        # The assertion failing means that other code is unstable
        assert self.IsEmpty()

        # Set the elements in batch to maximum
        self.elementsInBatch = self.batchSize

    def Touch(self, time):
        '''
        In case we're touched, we transfer the batch from the previous machine to the current machine,
        this means that this machine should not be busy, and that after accepting the transferred batch,
        we schedule a new event which indicates that the drying process is done.
        '''

        # Accept the batch
        self.TransferBatch()

        # TODO: We currently use 2000ms for scheduling a new DryingFinishedEvent, this should be modelled
        # using some function
        t1 = time + 2000

        # Indicate that the machine is busy
        self.SetBusy()

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, DryingFinishedEvent(self.productionLine))