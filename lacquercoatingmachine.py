from machine import Machine

class LacquerCoatingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(LacquerCoatingMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'
