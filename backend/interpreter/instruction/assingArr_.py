from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType

class AssignArr_(instruction):
    def __init__(self, line, column, id_, expression, expression2):
        super().__init__(line, column)
        self.id_ = id_
        self.expression = expression
        self.expression2 = expression2

    def Eject(self, env):
        pass