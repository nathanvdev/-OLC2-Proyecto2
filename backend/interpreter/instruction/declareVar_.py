from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..abstract.variables import Variables


class DeclareVar_(instruction):
    def __init__(self, line, column, id, type, expression, const):
        super().__init__(line, column)
        self.id = id 
        self.type = type
        self.value = expression
        self.const = const

    def Eject(self, env: Environment):
        pass