from ..abstract.instruction import instruction

class CallFunction_(instruction):   
    def __init__(self, line, column, id_, params):
        super().__init__(line, column)
        self.id_ = id_
        self.params = params
        
    def Eject(self, env):
        pass