from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType
from ..abstract.environment import Environment

class If_else(instruction):
    def __init__(self, line, column, condition, if_instructions, else_instructions):
        super().__init__(line, column)
        self.condition = condition
        self.if_instructions = if_instructions
        self.else_instructions = else_instructions

    def Eject(self, env):
        pass