import threading

from machine import Machine
from event import Event

class ConveryorBeltFinishedEvent(Event):
    def __init__(self, productionLine):
        super(ConveryorBeltFinishedEvent, self).__init__('ConveryorBeltFinishedEvent', productionLine)

    def PollNotBusy(self, time):
        # Wait for non-busy sputtering machine
        # TODO: At this point we should check the machines from other production lines
        while self.productionLine.GetSputteringMachine().IsBusy():
            pass

        # Sputtering machine is not busy anymore, unhalt processing and...
        self.productionLine.ContinueProcessing()

        # Touch the sputtering machine
        self.productionLine.GetSputteringMachine().Touch(time)

    def Handle(self, time):
        # Fetch an instance of the input buffer "machine"
        inputBufferMachine = self.productionLine.GetInputBufferMachine()

        # Check if the input buffer is not full, if so we need to halt the production line up to the conveyor belt
        if not inputBufferMachine.IsFull():
            '''
            We have reached a situation where the input buffer is not full, so we indicate to the input buffer
            that a new element is added and we check if we can indicate to the sputtering machine that the element
            can be fetched from the input buffer. In case the sputtering machine is busy, we wait and we slowly fill
            the input buffer until we're full, in which case we end up in the situation below.
            '''
            inputBufferMachine.Touch(time)

            # Touch the sputtering machine if the machine is not busy
            sputteringMachine = self.productionLine.GetSputteringMachine()
            if not sputteringMachine.IsBusy():
                sputteringMachine.Touch(time)
        else:
            '''
            We have reached a situation where the input buffer machine is full, meaning that the
            production line should not stop processing (to make sure that we're not flooding) the machines,
            and that we need to wait for the sputtering machine to finish (indicated by the machine not being)
            busy anymore. We do this by polling the machine, in case the machine is finished, we indicate that
            we can continue processing, we touch the sputtering machine, so that the machine can fetch everything
            from the input buffer. We wait until the machine is ready full again, such that this will repeat.
            '''
            self.productionLine.HaltProcessing()

            # Start polling the sputtering machine for non-busy state
            pollThread = threading.Thread(target=self.PollNotBusy, args=[time])
            pollThread.start()

class ConveyorBelt(Machine):
    def __init__(self, productionLine):
        super(ConveyorBelt, self).__init__(productionLine)

    def Touch(self, time):
        # every DVD spends 5 mins on the conveyor belt
        t1 = time + 50000

        # Add the event
        self.productionLine.GetSimulation().AddEvent(t1, ConveryorBeltFinishedEvent(self.productionLine))