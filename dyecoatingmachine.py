from machine import Machine

class DyeCoatingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(DyeCoatingMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'