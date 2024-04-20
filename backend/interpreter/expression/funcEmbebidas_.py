from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..expression.primitive import Primitive

class funcEmbebidas_(expression):
    def __init__(self, line, column, operator, expression):
        super().__init__(line, column)
        self.expression = expression
        self.operator = operator

        
    def Eject(self, env):
        pass