from abc import ABCMeta, abstractmethod

class Event:
    __metaclass__ = ABCMeta

    def __init__(self, name, productionLine):
        self.name           = name
        self.productionLine = productionLine

    @abstractmethod
    def Handle(self, time): pass

    def GetEventString(self):
        return '%s on production line number %i' % (self.name, self.productionLine.GetProductionLineNumber())

    def GetProductionLine(self):
        return self.productionLine