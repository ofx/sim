from machine import Machine

class ConveyorBelt(Machine):
    def __init__(self, productionLine):
        super(ConveyorBelt, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'