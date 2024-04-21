from ..abstract.instruction import instruction


class Return_(instruction):
    def __init__(self, line, column, expression):
        super().__init__(line, column)
        self.expression = expression

    def Eject(self, env):
        pass