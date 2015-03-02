import threading

from machine import Machine
from event import Event

class InputBufferMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(InputBufferMachine, self).__init__(productionLine)

        # Set the buffer size to 20
        self.bufferSize = 20

        # Set the elements in buffer to 0
        self.elementsInBuffer = 0

    def IsFull(self):
        # We can never overshoot
        assert self.elementsInBuffer < self.bufferSize + 1

        return self.elementsInBuffer == self.bufferSize

    def Touch(self, time):
        # We assume that this check has already been done, introducing this assert makes sure that
        # the caller is always properly calling this function
        assert not self.IsFull()

        # Increase the elements in buffer by 1
        self.elementsInBuffer += 1