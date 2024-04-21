from ..abstract.instruction import instruction
from ..abstract.environment import Environment



class DeclareInterface_(instruction):
    def __init__(self, line, column, id_, id2_, attributes):
        super().__init__(line, column)
        self.id_ = id_
        self.id2_ = id2_
        self.attributes = attributes


    def Eject(self, env: Environment):
        pass