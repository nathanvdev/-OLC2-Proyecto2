from ..abstract.instruction import instruction

class ModifyInterface_(instruction):
    def __init__(self, line, column, id_, id2_, expression):
        super().__init__(line, column)
        self.id_ = id_
        self.id2_ = id2_
        self.expression = expression

    def Eject(self, env):
        pass