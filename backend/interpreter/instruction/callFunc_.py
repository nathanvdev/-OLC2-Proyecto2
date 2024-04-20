from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..abstract.types import ExpressionType
from ..abstract.variables import Variables

class CallFunction_(instruction):   
    def __init__(self, line, column, id_, params):
        super().__init__(line, column)
        self.id_ = id_
        self.params = params
        
    def Eject(self, env):
        pass