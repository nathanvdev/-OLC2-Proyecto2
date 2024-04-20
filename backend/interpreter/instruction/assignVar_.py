from ..abstract.instruction import instruction

class AssignVar_(instruction):
    def __init__(self, line, column, name, op, expression):
        super().__init__(line, column)
        self.name = name
        self.op = op
        self.expression = expression

    def Eject(self, env):
        pass
