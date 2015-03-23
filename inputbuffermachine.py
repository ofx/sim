import threading

from machine import Machine
from event import Event

class InputBufferMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(InputBufferMachine, self).__init__(productionLine)

        # Set the buffer size to 20
        self.bufferSize = self.productionLine.GetConfiguration().GetBufferSize()

        # Set the elements in buffer to 0
        self.elementsInBuffer = 0

    def IsFull(self):
        # We can never overshoot
        assert self.elementsInBuffer < self.bufferSize + 1

        return self.elementsInBuffer == self.bufferSize

    def GetElementsInBuffer(self):
        return self.elementsInBuffer

    def IsEmpty(self):
        # We can never undershoot
        assert self.elementsInBuffer >= 0

        return self.elementsInBuffer == 0

    def Fetch(self):
        # Assume that this check if already done
        #assert self.elementsInBuffer > 0

        if self.elementsInBuffer == 0:
            return

        # Decrease the number of elements in the buffer
        self.elementsInBuffer -= 1

    def FetchAll(self):
        # Assume that this check if already done
        assert self.elementsInBuffer > 0

        # Set the number of elements in buffer to 0
        self.elementsInBuffer = 0

    def Take(self, n):
        # Assume that this check if already done
        #assert self.elementsInBuffer > 0

        if self.elementsInBuffer == 0:
            return

        # Take n from the input buffer
        self.elementsInBuffer -= n

        # If we have reached some < 0 value here, this means we have non-valid logic at some other point
        assert self.elementsInBuffer >= 0

    def Touch(self, time):
        # We assume that this check has already been done, introducing this assert makes sure that
        # the caller is always properly calling this function
        assert not self.IsFull()

        # Increase the elements in buffer by 1
        self.elementsInBuffer += 1