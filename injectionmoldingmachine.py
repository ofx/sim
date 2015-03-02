import threading

from machine import Machine
from event import Event

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
        # TODO: We currently use 2000ms for scheduling a new InjectionMoldingFinishedEvent, this should be modelled
        # using some function
        t1 = time + 2000

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, InjectionMoldingFinishedEvent(self.productionLine, self))