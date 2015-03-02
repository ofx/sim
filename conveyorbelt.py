from machine import Machine
from event import Event

class ConveryorBeltFinishedEvent(Event):
    def __init__(self, productionLine):
        super(ConveryorBeltFinishedEvent, self).__init__('ConveryorBeltFinishedEvent', productionLine)

    def Handle(self, time):
        print 'Conveyor Belt finished'

class ConveyorBelt(Machine):
    def __init__(self, productionLine):
        super(ConveyorBelt, self).__init__(productionLine)

    def Touch(self, time):
        # TODO: We currently use 2000ms for scheduling a new InjectionMoldingFinishedEvent, this should be modelled
        # using some function
        t1 = time + 2000

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, ConveryorBeltFinishedEvent(self.productionLine))