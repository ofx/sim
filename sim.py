#!/usr/bin/python

import os
import datetime
import time
import random
import numpy as np

from Queue import PriorityQueue
from Queue import Empty

from time import sleep
from configuration import Configuration

from productionline import ProductionLine

class Sim:
    '''
    Initialize the simulation by creating two production lines.
    '''
    def __init__(self, maxProduction, configuration):
        self.productionLines = [ProductionLine(self, configuration, 1), ProductionLine(self, configuration, 2)]

        # Initialize a priority queue resembling our event queue
        self.eventQueue = PriorityQueue()

        # Set time to 0
        self.time = 0

        # Set last event to ''
        self.event = ''

        # Set last output buffer size to 0
        self.lastOutputBufferSize = 0

        # Set the maximum production
        self.maxProduction = maxProduction

        # Store the historic schedule (which is empty at start)
        self.schedule = []

        # set the seed for the program.
        np.random.seed(42)


    def GetProductionLines(self):
        return self.productionLines

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

        # Store the schedule
        self.schedule.append('%i: %s' % (time, event.GetEventString()))

        # Handle the event, pass a reference to this production line instance
        event.Handle(time)

        # Set last time
        self.time = time

        # Set last event
        self.event = event

        # Tell the production line the actual time
        event.GetProductionLine().SetTime(self.time)

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
        #os.system('clear')

        # Initialize empty output buffer
        outputBuffer = ''

        # Add the time
        outputBuffer += 'Time: [%i]\n' % (self.time)

        # Add information for botch production lines
        i = 1
        for productionLine in self.productionLines:
            s = """\n[%i]
                \tEvent: %s
                \tElements in input buffer: %i
                \tElements in output buffer: %i
                \tElements in batch (sputtering): %i
                \tIs busy (sputtering): %r
                \tIs full (sputtering): %r
                \tElements in batch (lacquer coating): %i
                \tIs busy (lacquer coating): %r
                \tElements in batch (drying): %i
                \tIs busy (drying): %r
                \tIs empty (drying): %r
                \tIs busy (printing): %r
                \tDVDs produced (printing): %i\n""" % (
                i,
                self.event,
                productionLine.GetInputBufferMachine().GetElementsInBuffer(),
                productionLine.GetOutputBufferMachine().GetElementsInBuffer(),
                productionLine.GetSputteringMachine().GetElementsInBatch(),
                productionLine.GetSputteringMachine().IsBusy(),
                productionLine.GetSputteringMachine().IsFull(),
                productionLine.GetLacquerCoatingMachine().GetElementsInBatch(),
                productionLine.GetLacquerCoatingMachine().IsBusy(),
                productionLine.GetDryingMachine().GetElementsInBatch(),
                productionLine.GetDryingMachine().IsBusy(),
                productionLine.GetDryingMachine().IsEmpty(),
                productionLine.GetPrintingMachine().IsBusy(),
                productionLine.GetPrintingMachine().GetDvdsProduced()
            )

            # Display breakdown status of injection molding machines
            n = 0
            for injectionMoldingMachine in productionLine.GetInjectionMoldingMachines():
                s += """\n\tInjection molding machine [%i]
                     \tBreakdown: %r""" % (
                    n,
                    injectionMoldingMachine.IsBrokenDown()
                )

                n += 1

            # Add string to output buffer
            outputBuffer += s

            # Increase the production line number
            i += i

        print outputBuffer

        # Last output buffer size
        self.lastOutputBufferSize = len(outputBuffer)

    def ShouldStop(self):
        totalDvdsProduced = 0

        for productionLine in self.productionLines:
            totalDvdsProduced += productionLine.GetPrintingMachine().GetDvdsProduced()

        # We shouldn't overshoot
        assert totalDvdsProduced <= self.maxProduction

        return totalDvdsProduced == self.maxProduction

    def DumpSchedule(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')

        f = open('dump_%s' % st,'w')
        for line in self.schedule:
            f.write('%s\n' % line)
        f.close()

    '''
    Run the simulation.
    '''
    def Run(self):
        while self.Step():
            # Print some information
            self.PrintInfo()

            #for productionLine in self.productionLines:
            #    print productionLine.IsHalted()

            # Check if we've reached max production
            if self.ShouldStop():
                break

            #raw_input("Press enter to step...")

        print 'Done in %i milliseconds' % self.time

        return self.time

if __name__ == "__main__":
    endCondition = 2000

    configuration = Configuration(20, 100)

    simulation = Sim(endCondition, configuration)

    print 'Starting simulation...'
    simulation.Start()
    simulation.Run()
    simulation.DumpSchedule()
