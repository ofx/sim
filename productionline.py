from injectionmoldingmachine import InjectionMoldingMachine
from dyecoatingmachine import DyeCoatingMachine
from conveyorbelt import ConveyorBelt
from sputteringmachine import SputteringMachine
from lacquercoatingmachine import LacquerCoatingMachine
from dryingmachine import DryingMachine
from printingmachine import PrintingMachine
from inputbuffermachine import InputBufferMachine
from outputbuffermachine import OutputBufferMachine

from event import Event

class ProductionLine:
    '''
    We initialize the machines in one production line, which are:

    2 injection molding machines
    1 dye coating machine
    1 conveyor belt
    1 sputtering machine
    1 lacquer coating machine
    1 drying machine
    1 printing machine
    '''
    def __init__(self, simulation):
        # Initialize the machine instances
        self.injectionMoldingMachines = [InjectionMoldingMachine(self), InjectionMoldingMachine(self)]
        self.dyeCoatingMachine        = DyeCoatingMachine(self)
        self.conveyorBelt             = ConveyorBelt(self)
        self.sputteringMachine        = SputteringMachine(self)
        self.lacquerCoatingMachine    = LacquerCoatingMachine(self)
        self.dryingMachine            = DryingMachine(self)
        self.printingMachine          = PrintingMachine(self)
        self.inputBufferMachine       = InputBufferMachine(self)
        self.outputBufferMachine      = OutputBufferMachine(self)

        # Store a reference to the simulation
        self.simulation = simulation

        # At launch, we're not halted
        self.isHalted = False

        # At start, the time is 0
        self.time = 0

    '''
    Set the actual time.
    '''
    def SetTime(self, time):
        self.time = time

    '''
    Get the actual time.
    '''
    def GetTime(self):
        return self.time

    '''
    Return a reference to the output buffer machine.
    '''
    def GetOutputBufferMachine(self):
        return self.outputBufferMachine

    '''
    Return a reference to the input buffer machine.
    '''
    def GetInputBufferMachine(self):
        return self.inputBufferMachine

    '''
    Return the simulation instance.
    '''
    def GetSimulation(self):
        return self.simulation

    '''
    Return a set of available injection molding machines.
    '''
    def GetInjectionMoldingMachines(self):
        return self.injectionMoldingMachines

    '''
    Return the available dye coating machine.
    '''
    def GetDyeCoatingMachine(self):
        return self.dyeCoatingMachine

    '''
    Return the available conveyor belt.
    '''
    def GetConveyorBelt(self):
        return self.conveyorBelt

    '''
    Return the available sputtering machine.
    '''
    def GetSputteringMachine(self):
        return self.sputteringMachine

    '''
    Return the available lacquer coating machine.
    '''
    def GetLacquerCoatingMachine(self):
        return self.lacquerCoatingMachine

    '''
    Return the available drying machine.
    '''
    def GetDryingMachine(self):
        return self.dryingMachine

    '''
    Return the available printing machine.
    '''
    def GetPrintingMachine(self):
        return self.printingMachine

    '''
    Halt processing of the first three machines, injection molding, dye coating and
    conveyor belt to allow the sputtering, lacquer coating and drying machines to finish.
    '''
    def HaltProcessing(self):
        assert self.isHalted == False

        self.isHalted = True

    '''
    Continue processing for the first three machines.
    '''
    def ContinueProcessing(self):
        assert self.isHalted == True

        self.isHalted = False

    '''
    Returns a flag indicating if this production line is currently halted.
    '''
    def IsHalted(self):
        return self.isHalted

    '''
    Start up this production line.
    '''
    def Start(self):
        # Touch both injection molding machines to start up this production line
        # Set the current time to zero, since we're only just starting up
        for injectionMoldingMachine in self.injectionMoldingMachines:
            injectionMoldingMachine.Touch(0)