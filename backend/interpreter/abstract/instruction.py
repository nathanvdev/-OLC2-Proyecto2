from abc import ABC, abstractmethod

class instruction(ABC):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    @abstractmethod
    def Eject(self, env):
        pass
        