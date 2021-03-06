import threading

from machine import Machine
from event import Event

import random
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

        # Set the time to the actual time
        time = self.productionLine.GetTime()

        # Touch the dye coating machine to trigger event generation
        dyeCoatingMachine.Touch(time)

        # Wait for non-broken down machine
        while self.injectionMoldingMachine.IsBrokenDown():
            pass

        # Set the time to the actual time
        time = self.productionLine.GetTime()

        # Touch the injection molding machine that this event is belonging to to indicate that it's ready to schedule a new
        # event indicating that it's done
        self.injectionMoldingMachine.Touch(time)

    def Handle(self, time):
        pollThread = threading.Thread(target=self.PollUnhalt, args=[time])
        pollThread.setDaemon(True)
        pollThread.start()

class InjectionMoldingBreakdownEndEvent(Event):
    def __init__(self, productionLine, injectionMoldingMachine):
        super(InjectionMoldingBreakdownEndEvent, self).__init__('InjectionMoldingBreakdownEndEvent', productionLine)

        # Keep a reference to the machine that this event belongs to
        self.injectionMoldingMachine = injectionMoldingMachine

    def Handle(self, time):
        # Indicate that the machine is not broken down
        self.injectionMoldingMachine.SetNonBrokenDown()

        # Schedule a new breakdown
        self.injectionMoldingMachine.ScheduleBreakdown()

class InjectionMoldingBreakdownStartEvent(Event):
    def __init__(self, productionLine, injectionMoldingMachine):
        super(InjectionMoldingBreakdownStartEvent, self).__init__('InjectionMoldingBreakdownStartEvent', productionLine)

        # Keep a reference to the machine that this event belongs to
        self.injectionMoldingMachine = injectionMoldingMachine

    def Handle(self, time):
        # Indicate that the machine is broken down
        self.injectionMoldingMachine.SetBrokenDown()

        # repair time
        if self.injectionMoldingMachine.isOld:
            t2 = self.injectionMoldingMachine.TimeTillRepairOldMachine()
        t2 = self.injectionMoldingMachine.TimeTillRepairNewMachine()  
        
        # Schedule a new breakdown end event
        self.productionLine.GetSimulation().AddEvent(t2, InjectionMoldingBreakdownEndEvent(self.productionLine, self.injectionMoldingMachine))

class InjectionMoldingMachine(Machine):
    batch = None
    
    def __init__(self, productionLine, isOld):
        super(InjectionMoldingMachine, self).__init__(productionLine)

        # At start we want to schedule a breakdown
        self.scheduleBreakdown = True
        self.isOld = isOld
        # At start we're not broken down
        self.brokenDown = False

    def ScheduleBreakdown(self):
        # If this check fails we've written poor code elsewhere
        assert not self.scheduleBreakdown

        self.scheduleBreakdown = True

    def SetBrokenDown(self):
        assert not self.brokenDown

        self.brokenDown = True

    def SetNonBrokenDown(self):
        assert self.brokenDown

        self.brokenDown = False

    def IsBrokenDown(self):
        return self.brokenDown




    '''
    Touch this machine, which for the injection molding machine means pushing an InjectionMoldingFinishedEvent
    into the production line's event queue.
    '''
    def Touch(self, time):
        t1 = time + self.Wait()

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, InjectionMoldingFinishedEvent(self.productionLine, self))

        # Only schedule a breakdown if the scheduleBreakdown flag indicates to do so
        if self.scheduleBreakdown:

            if self.isOld:
                t2 = self.TimeTillNextBreakdownOldMachine()
            t2 = self.TimeTillNextBreakdownNewMachine()

            # Add a breakdown event
            self.productionLine.GetSimulation().AddEvent(t2, InjectionMoldingBreakdownStartEvent(self.productionLine, self))

            # Indicate that we shouldn't yet schedule a new breakdown
            self.scheduleBreakdown = False

    def Wait(self):
        # gamma distribution (close to exponential, as shape = 1)
        shape = 0.9968
        scale = 60.1
        # * 1000 for seconds -> ms
        # do we want rounded ms?
        s = np.random.gamma(shape, scale, 1) * 1000
        return s

    def TimeTillNextBreakdownOldMachine(self):
        # weibull distribution
        shape,scale = 1.02, 482.6
        s = np.random.weibull(shape)
        # times 100 for mins -> sec, 1000 for s -> ms
        s = s * scale * 100 * 1000
        return s

    def TimeTillNextBreakdownNewMachine(self):
        #weibull distribution, but normal distribution now activated, still in doubt
        # shape, scale = 8.0067888,63.9084317
        # s = np.random.weibull(shape)
        # # times 100 for mins -> sec, 1000 for s -> ms
        # s = s * scale * 100 * 1000
        # return s

        # normal distribution
        mu,sigma = 60.1877143, 8.4852158
        s = random.normalvariate(mu, sigma)
        # # times 100 for mins -> sec, 1000 for s -> ms
        s = s * 100 * 1000
        return s

    def TimeTillRepairOldMachine(self):
        mu, sigma = 916.828507, 200
        s = random.normalvariate(mu, sigma)
        # times 100 for mins -> sec, 1000 for s -> ms
        s = s * 100 * 1000
        return s

    def TimeTillRepairNewMachine(self):
        shape, scale = 1.06432092, 115.52050746 
        s = np.random.gamma(shape, scale, 1)
        # times 100 for mins -> sec, 1000 for s -> ms
        s = s * 100 * 1000
        return s