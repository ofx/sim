from machine import Machine

class PrintingMachine(Machine):
    batch = None

    def __init__(self, productionLine):
        super(PrintingMachine, self).__init__(productionLine)

    def Touch(self, time):
        print 'Touch PrintingMachine'
        t1 = time + self.Wait()
    def Wait(self):
	# this data is generated from R
	mu = 24.81055
	sigma = 2.867319
	# compute the random variable with a normal distribution
	s = random.normalvariate(mu, sigma)
    return s