from ..abstract.instruction import instruction
from ..abstract.array_ import Array_

class DeclareArr_(instruction):
    def __init__(self, line, column, id_, Type, expression_list, const):
        super().__init__(line, column)
        self.id_ = id_
        self.Type = Type
        self.expression_list = expression_list
        self.const = const

    def Eject(self, env):
        pass