from ..abstract.expression import expression
from ..expression.primitive import Primitive
from ..abstract.types import ExpressionType


class callInterface_(expression):
    def __init__(self, line, column, id, params):
        super().__init__(line, column)
        self.id = id
        self.params = params

    def Eject(self, env):
        pass