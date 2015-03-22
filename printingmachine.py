from machine import Machine
from event import Event

import random

import numpy as np
from scipy import optimize
import scipy.special as sps
import matplotlib.pyplot as plt

class PrintingFinishedEvent(Event):
    def __init__(self, productionLine, printingMachine):
        super(PrintingFinishedEvent, self).__init__('PrintingFinishedEvent', productionLine)

        # Store a reference to the printing machine
        self.printingMachine = printingMachine

    def Handle(self, time):
        # Indicate that we're not busy anymore
        self.printingMachine.SetNonBusy()

        # We're done, we've created a DVD
        self.printingMachine.IncrementDvdsProduced()

class PrintingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(PrintingMachine, self).__init__(productionLine)

        # At start, we're not busy
        self.isBusy = False

        # At start, we've created 0 DVDs
        self.dvdsProduced = 0

    def GetDvdsProduced(self):
        return self.dvdsProduced

    def IncrementDvdsProduced(self):
        self.dvdsProduced += 1

    def SetNonBusy(self):
        assert self.isBusy

        self.isBusy = False

    def SetBusy(self):
        assert not self.isBusy

        self.isBusy = True

    def IsBusy(self):
        return self.isBusy

    def Touch(self, time):
        # Assume that we're not busy, in case we are, we have some error elsewhere
        assert not self.IsBusy()

        # Determine end time for event
        t1 = time + self.Wait()

        # Just a check that should always hold here
        assert self.productionLine.GetOutputBufferMachine().GetPrintingMachine() == self

        # Take one from the output buffer
        self.productionLine.GetOutputBufferMachine().TakeOne()

        # Indicate that we're busy
        self.SetBusy()

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, PrintingFinishedEvent(self.productionLine, self))

    def Wait(self):
        # this data is generated from R
        mu = 24.81055
        sigma = 2.867319
        # compute the random variable with a normal distribution
        s = random.normalvariate(mu, sigma)
        return s
