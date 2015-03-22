from machine import Machine
from event import Event

import random
import numpy as np
from scipy import optimize
import scipy.special as sps
import matplotlib.pyplot as plt

class DyeCoatingFinishedEvent(Event):
    def __init__(self, productionLine, dyeCoatingMachine):
        super(DyeCoatingFinishedEvent, self).__init__('DyeCoatingFinishedEvent', productionLine)

        self.dyeCoatingMachine = dyeCoatingMachine

    def Handle(self, time):
        # Check if the production failed
        failed = False
        if self.dyeCoatingMachine.IsOld():
            if random.randint(0, 99) < 5:
                failed = True
        else:
            if random.randint(0, 99) < 1:
                failed = True

        # If the production has failed, we don't transfer the item
        if failed:
            return

        # Dye Coating is finished, get an instance of the conveyor belt to schedule a next event
        # where the conveyor belt is done
        conveyorBelt = self.productionLine.GetConveyorBelt()

        # Touch the conveyor belt
        conveyorBelt.Touch(time)


class DyeCoatingMachine(Machine):
    batch = None

    def __init__(self, productionLine, old):
        super(DyeCoatingMachine, self).__init__(productionLine)

        # Indicate if this is an old or new machine
        self.old = old

    def IsOld(self):
        return self.old

    def Touch(self, time):
        t1 = time + self.Wait()
        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, DyeCoatingFinishedEvent(self.productionLine, self))

    def Wait(self):
        # extracted params Gamma distribution
        shape = 2.028916
        scale = 17.804045
        s = np.random.gamma(shape, scale, 1) * 1000
        return s
