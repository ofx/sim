from abc import ABCMeta, abstractmethod

class Event:
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def Handle(self, productionLine): pass