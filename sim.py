#!/usr/bin/python

from Queue import PriorityQueue
from Queue import Empty
from time import sleep

from productionline import ProductionLine

class Sim:
    '''
    Initialize the simulation by creating two production lines.
    '''
    def __init__(self):
        self.productionLines = [ProductionLine(self), ProductionLine(self)]

        # Initialize a priority queue resembling our event queue
        self.eventQueue = PriorityQueue()

        # Set time to 0
        self.time = 0

        # Set last output buffer size to 0
        self.lastOutputBufferSize = 0

    '''
    Push event onto event queue.
    '''
    def AddEvent(self, time, event):
        self.eventQueue.put((time, event))

    '''
    Step through time.
    '''
    def Step(self):
        # Check if we're out of events
        if self.eventQueue.empty():
            return False

        # Pop the next event from the event queue
        (time, event) = self.eventQueue.get()

        # Handle the event, pass a reference to this production line instance
        event.Handle(time)

        # Set last time
        self.time = time

        return True

    '''
    Start the simulation.
    '''
    def Start(self):
        # Start the simulation by starting both production lines
        for productionLine in self.productionLines:
            productionLine.Start()

    def PrintInfo(self):
        # Wipe the last information from the screen
        #for i in range(0, self.lastOutputBufferSize):
        #    print '\b'

        # Initialize empty output buffer
        outputBuffer = ''

        # Add the time
        outputBuffer += 'Time: [%i]\n' % (self.time)

        # Add information for botch production lines
        i = 1
        for productionLine in self.productionLines:
            s = """[%i]
                \tElements in buffer: %i
                \tElements in batch (s): %i
                \tIs busy (s): %r
                \tIs full (s): %r
                \tElements in batch (lc): %i
                \tIs busy (lc): %r
                \tElements in batch (d): %i
                \tIs busy (d): %r\n""" % (
                i,
                productionLine.GetInputBufferMachine().GetElementsInBuffer(),
                productionLine.GetSputteringMachine().GetElementsInBatch(),
                productionLine.GetSputteringMachine().IsBusy(),
                productionLine.GetSputteringMachine().IsFull(),
                productionLine.GetLacquerCoatingMachine().GetElementsInBatch(),
                productionLine.GetLacquerCoatingMachine().IsBusy(),
                productionLine.GetDryingMachine().GetElementsInBatch(),
                productionLine.GetDryingMachine().IsBusy()
            )

            # Add string to output buffer
            outputBuffer += s

            # Increase the production line number
            i += i

        print outputBuffer

        # Last output buffer size
        self.lastOutputBufferSize = len(outputBuffer)

    '''
    Run the simulation.
    '''
    def Run(self):
        # Run until we eventually run against an EmptyException triggered by the get-operation
        # on the priority queue, in which case we're done simulating
        try:
            while self.Step():
                # Print some information
                self.PrintInfo()

                # Sleep for a short while
                sleep(0.1)
        except Empty:
            print 'Simulation ended'

if __name__ == "__main__":
    simulation = Sim()

    print 'Starting simulation...'
    simulation.Start()
    simulation.Run()