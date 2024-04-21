from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType
from ..abstract.value import Value

class Access(instruction):
    def __init__(self, line, column, name):
        super().__init__(line, column)
        self.name = name

    def Eject(self, env, gen):
        # Realizar busqueda en entorno
        sym = env.getVariable(self.name)
        if(sym.Type != ExpressionType.NULL):
            # Reconstrucción de Value
            return Value(sym.position, False, sym.Type, [], [], [])
        return Value('', False, ExpressionType.NULL, [], [], [])