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

    '''
    Push event onto event queue.
    '''
    def AddEvent(self, time, event):
        self.eventQueue.put((time, event))

    '''
    Step through time.
    '''
    def Step(self):
        # Pop the next event from the event queue
        (time, event) = self.eventQueue.get()

        # Provide some output
        print '[%i] %s' % (time, event.name)

        # Handle the event, pass a reference to this production line instance
        event.Handle(self)

    '''
    Start the simulation.
    '''
    def Start(self):
        # Start the simulation by starting both production lines
        for productionLine in self.productionLines:
            productionLine.Start()

    '''
    Run the simulation.
    '''
    def Run(self):
        # Run until we eventually run against an EmptyException triggered by the get-operation
        # on the priority queue, in which case we're done simulating
        try:
            while True:
                self.Step()

                # Sleep for a short while
                sleep(0.1)
        except Empty:
            print 'Simulation ended'

if __name__ == "__main__":
    simulation = Sim()

    print 'Starting simulation...'
    simulation.Start()
    simulation.Run()