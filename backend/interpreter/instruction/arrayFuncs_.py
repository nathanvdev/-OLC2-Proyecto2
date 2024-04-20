from ..abstract.instruction import instruction

class ArrayFuncs_(instruction):
    def __init__(self, line, column, id_, FuncType, expression):
        super().__init__(line, column)
        self.id_ = id_
        self.FuncType = FuncType
        self.expression = expression

    def Eject(self, env):
        pass
            