from machine import Machine
from event import Event

import threading

class LacquerCoatingFinishedEvent(Event):
    def __init__(self, productionLine):
        super(LacquerCoatingFinishedEvent, self).__init__('LacquerCoatingFinishedEvent', productionLine)

    def PollNotBusy(self, time):
        # TODO: At this point we should check the machines from other production lines
        dryingMachine = self.productionLine.GetDryingMachine()
        while dryingMachine.IsBusy():
            pass

        # Set the time to the actual time
        time = self.productionLine.GetTime()

        # The machine is not busy anymore, transfer the batch
        dryingMachine.Touch(time)

        # Set the sputtering machine to a non-busy state
        # (we assume that the sputtering machine is busy)
        lacquerCoatingMachine = self.productionLine.GetLacquerCoatingMachine()

        assert lacquerCoatingMachine.IsBusy()

        # Indicate that the machine is not busy
        lacquerCoatingMachine.SetNonBusy()

        # Indicate that the machine now is empty
        lacquerCoatingMachine.SetEmpty()

    def Handle(self, time):
        # Start polling the drying machine for non-busy state
        pollThread = threading.Thread(target=self.PollNotBusy, args=[time])
        pollThread.start()

class LacquerCoatingMachine(Machine):
    def __init__(self, productionLine):
        super(LacquerCoatingMachine, self).__init__(productionLine)

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
        we schedule a new event which indicates that the lacquer coating process is done.
        '''

        # Accept the batch
        self.TransferBatch()

        # TODO: We currently use 2000ms for scheduling a new LacquerCoatingFinishedEvent, this should be modelled
        # using some function
        t1 = time + 2000

        # Indicate that the machine is busy
        self.SetBusy()

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, LacquerCoatingFinishedEvent(self.productionLine))