import threading

from machine import Machine
from event import Event

import numpy as np
from scipy import optimize
import scipy.special as sps
import matplotlib.pyplot as plt

class InjectionMoldingFinishedEvent(Event):
    def __init__(self, productionLine, injectionMoldingMachine):
        super(InjectionMoldingFinishedEvent, self).__init__('InjectionMoldingFinishedEvent', productionLine)

        # Keep a reference to the machine that this event belongs to
        self.injectionMoldingMachine = injectionMoldingMachine

    def PollUnhalt(self, time):
        # Wait for unhalted production line
        while self.productionLine.IsHalted():
            pass

        # After handling the event, we trigger the next machine (dye coating)
        dyeCoatingMachine = self.productionLine.GetDyeCoatingMachine()

        # Touch the dye coating machine to trigger event generation
        dyeCoatingMachine.Touch(time)

        # Touch the injection molding machine that this event is belonging to to indicate that it's ready to schedule a new
        # event indicating that it's done
        self.injectionMoldingMachine.Touch(time)

    def Handle(self, time):
        pollThread = threading.Thread(target=self.PollUnhalt, args=[time])
        pollThread.start()

class InjectionMoldingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(InjectionMoldingMachine, self).__init__(productionLine)

    '''
    Touch this machine, which for the injection molding machine means pushing an InjectionMoldingFinishedEvent
    into the production line's event queue.
    '''
    def Touch(self, time):

        t1 = time + self.Wait()
        
        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, InjectionMoldingFinishedEvent(self.productionLine, self))

    def Wait(self):

        # this data is generated from R, on injection molding.
        shape = 0.9968
        scale = 60.1

        # * 1000 for seconds -> ms
        # do we want rounded ms?

        s = np.random.gamma(shape, scale, 1) * 1000

        return s
        
    # shows plot of distribution, set third param of np.random.gamma to higher number.    

    #     count, bins, ignored = plt.hist(s, 50, normed=True)
    #     y = bins**(shape-1)*(np.exp(-bins/scale) / (sps.gamma(shape)*scale**shape))
    #     plt.plot(bins, y, linewidth=2, color='r')
    #     plt.show()
    # 