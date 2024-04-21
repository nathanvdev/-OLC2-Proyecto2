from ..abstract.instruction import instruction
from ..abstract.symbol import Symbol

class AssignVar_(instruction):
    def __init__(self, line, column, name, op, expression):
        super().__init__(line, column)
        self.name = name
        self.op = op
        self.expression = expression

    def Eject(self, env, gen):
         # Obtener valor
        result = self.expression.Eject(env, gen)
        sym = Symbol(self.line, self.column, self.name, result.Type, result.value)
        # Editar simbolo
        env.setVariable(self.name, sym)
        return None
