from machine import Machine
from event import Event

import numpy as np
from scipy import optimize
import scipy.special as sps
import matplotlib.pyplot as plt

class DyeCoatingFinishedEvent(Event):
    def __init__(self, productionLine):
        super(DyeCoatingFinishedEvent, self).__init__('DyeCoatingFinishedEvent', productionLine)

    def Handle(self, time):
        # Dye Coating is finished, get an instance of the conveyor belt to schedule a next event
        # where the conveyor belt is done
        conveyorBelt = self.productionLine.GetConveyorBelt()

        # Touch the conveyor belt
        conveyorBelt.Touch(time)

      
class DyeCoatingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(DyeCoatingMachine, self).__init__(productionLine)

    def Touch(self, time):
        t1 = time + self.Wait()
        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, DyeCoatingFinishedEvent(self.productionLine))

    def Wait(self):
        # extracted params Gamma distribution
        shape = 2.028916
        scale = 17.804045
        s = np.random.gamma(shape, scale, 1) * 1000
        return s