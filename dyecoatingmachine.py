from machine import Machine
from event import Event

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
        # TODO: We currently use 2000ms for scheduling a new InjectionMoldingFinishedEvent, this should be modelled
        # using some function
        t1 = time + 2000

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, DyeCoatingFinishedEvent(self.productionLine))