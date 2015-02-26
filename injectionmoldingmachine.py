from machine import Machine
from event import Event

class InjectionMoldingFinishedEvent(Event):
    def __init__(self):
        super(InjectionMoldingFinishedEvent, self).__init__('InjectionMoldingFinishedEvent')

    def Handle(self, productionLine):
        print 'Handling'

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
        self.productionLine.GetSimulation().AddEvent(t1, InjectionMoldingFinishedEvent())