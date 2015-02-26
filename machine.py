from abc import ABCMeta, abstractmethod

class Machine:
    __metaclass__ = ABCMeta

    def __init__(self, productionLine):
        self.productionLine = productionLine

    @abstractmethod
    def Touch(self, time): pass