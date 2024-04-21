from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..abstract.symbol import Symbol



class DeclareVar_(instruction):
    def __init__(self, line, column, id, type, expression, const):
        super().__init__(line, column)
        self.id = id 
        self.Type = type
        self.value = expression
        self.const = const

    def Eject(self, env: Environment, gen):
        # Generar simbolo
        result = self.value.Eject(env, gen)
        sym = Symbol(self.line, self.column, self.id, self.Type, result.value)
        # Validar tipo
        if result.Type != self.Type:
            # ast.setErrors("Los tipos de dato son incorrectos")
            return
        # Agregar al entorno
        env.saveVariable(self.id, sym)
        return None