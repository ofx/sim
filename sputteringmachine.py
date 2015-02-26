from machine import Machine

class SputteringMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(SputteringMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch'
