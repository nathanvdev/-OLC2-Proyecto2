from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..expression.primitive import Primitive



class for_(instruction):
    def __init__(self, line, column, assignment, condition, evalue, op, instructions):
        super().__init__(line, column)
        self.assignment = assignment
        self.condition = condition
        self.evalue = evalue
        self.op = op
        self.instructions = instructions


    def Eject(self, env:Environment):
        pass