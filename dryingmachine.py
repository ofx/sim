from machine import Machine

class DryingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(DryingMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'
