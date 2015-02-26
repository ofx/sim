from machine import Machine

class PrintingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(PrintingMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'
