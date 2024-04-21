from ..abstract.instruction import instruction


class while_(instruction):
    def __init__(self, line, column, condition, instructions):
        super().__init__(line, column)
        self.condition = condition
        self.instructions = instructions


    def Eject(self, env):
        pass