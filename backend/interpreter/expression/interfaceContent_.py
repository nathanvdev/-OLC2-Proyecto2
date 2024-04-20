from ..abstract.expression import expression

class interfaceContent_(expression):
    def __init__(self, line, column, id_, Type):
        super().__init__(line, column)
        self.id_ = id_
        self.Type = Type

    def Eject(self, env):
        pass