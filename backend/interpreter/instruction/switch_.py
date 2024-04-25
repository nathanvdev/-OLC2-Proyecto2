from ..abstract.instruction import instruction

class Switch_(instruction):
    def __init__(self, line, column, expression_, cases_, default_):
        super().__init__(line, column)
        self.expression = expression_
        self.cases = cases_
        self.default = default_


    def Eject(self, env, gen):
        
        
        return None