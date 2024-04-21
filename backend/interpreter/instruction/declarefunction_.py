from ..abstract.instruction import instruction

class DeclareFunction_(instruction):
    def __init__(self,line, column, id_, params, returnType, instructions):
        super().__init__(line, column)
        self.id_ = id_
        self.params = params
        self.returnType = returnType
        self.instructions = instructions

    def Eject(self, env):
        pass