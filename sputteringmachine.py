from machine import Machine
from event import Event

import threading

class SputteringFinishedEvent(Event):
    def __init__(self, productionLine):
        super(SputteringFinishedEvent, self).__init__('SputteringFinishedEvent', productionLine)

    def PollNotBusy(self, time):
        lacquerCoatingMachine = productionLine.GetLacquerCoatingMachine()
        while lacquerCoatingMachine.IsBusy():
            pass

        while lacquerCoatingMachine.IsBrokenDown():
            pass

        # Set the time to the actual time
        time = productionLine.GetTime()

        # The machine is not busy anymore, transfer the batch
        lacquerCoatingMachine.Touch(time)

        # Set the sputtering machine to a non-busy state
        # (we assume that the sputtering machine is busy)
        sputteringMachine = self.GetProductionLine().GetSputteringMachine()

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

class SputteringBreakdownEndEvent(Event):
    def __init__(self, productionLine, sputteringBreakdownEndEvent):
        super(SputteringBreakdownEndEvent, self).__init__('SputteringBreakdownEndEvent', productionLine)

        # Keep a reference to the machine that this event belongs to
        self.sputteringBreakdownEndEvent = sputteringBreakdownEndEvent

    def Handle(self, time):
        # Indicate that the machine is not broken down
        self.sputteringBreakdownEndEvent.SetNonBrokenDown()

class SputteringBreakdownStartEvent(Event):
    def __init__(self, productionLine, sputteringBreakdownEndEvent):
        super(SputteringBreakdownStartEvent, self).__init__('SputteringBreakdownStartEvent', productionLine)

        # Keep a reference to the machine that this event belongs to
        self.sputteringBreakdownEndEvent = sputteringBreakdownEndEvent

    def Handle(self, time):
        # Indicate that the machine is broken down
        self.sputteringBreakdownEndEvent.SetBrokenDown()

        t2 = time + 300000

        # Schedule a new breakdown end event
        self.productionLine.GetSimulation().AddEvent(t2, InjectionMoldingBreakdownEndEvent(self.productionLine, self.injectionMoldingMachine))

class SputteringMachine(Machine):
    def __init__(self, productionLine):
        super(SputteringMachine, self).__init__(productionLine)

        # At start there are 0 elements in the batch
        self.elementsInBatch = 0

        # At start this machine is not busy
        self.isBusy = False

        # Fetch the batch size from the configuration
        self.batchSize = self.productionLine.GetConfiguration().GetBatchSize()

        # At start we're not broken down
        self.brokenDown = False

    def SetBrokenDown(self):
        assert not self.brokenDown

        self.brokenDown = True

    def SetNonBrokenDown(self):
        assert self.brokenDown

        self.brokenDown = False

    def IsBrokenDown(self):
        return self.brokenDown

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

        print 'IS IT HALTED', self.productionLine.IsHalted()

        # check if prod line was halted, if so, unhalt
        if self.productionLine.IsHalted():
            self.productionLine.ContinueProcessing()

        # Add the elements from the input buffer to the batch
        self.elementsInBatch += elementsToAdd

        # We need to check if the batch is full, if so, we schedule a new event indicating that the sputtering
        # is done
        if self.IsFull():
            batchSize = self.productionLine.GetConfiguration().GetBatchSize()
            # sputtering takes 10 seconds per DVD, all DVD's need to be processed before we move on.
            t1 = time + 10000 * batchSize

            # Add the event
            self.productionLine.GetSimulation().AddEvent(t1, SputteringFinishedEvent(self.productionLine))

            # Indicate that this machine is busy
            self.SetBusy()

    def MachineStuck(self,time):
        # 3 % of the DVD's distrupt the machine.
        if random.randint(0, 99) < 3:
            t3 = time + 300000
            self.productionLine.GetSimulation().AddEvent(t3, SputteringBreakdownStartEvent(self.productionLine))
        