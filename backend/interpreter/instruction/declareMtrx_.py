from ..abstract.instruction import instruction

class DeclareMtrx_(instruction):
    def __init__(self, line, column, param1, param2, param3, param4, param5):
        super().__init__(line, column)
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.param5 = param5


    def Eject(self, env):
        pass