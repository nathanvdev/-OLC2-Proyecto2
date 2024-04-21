from ..abstract.instruction import instruction
from ..abstract.value import Value
from ..abstract.types import ExpressionType
from ..abstract.symbol import Symbol

class DeclareArr_(instruction):
    def __init__(self, line, column, id_, Type, expression_list, const):
        super().__init__(line, column)
        self.id_ = id_
        self.Type = Type
        self.expression_list = expression_list
        self.const = const

    def Eject(self, env, gen):
        newArr = []
        for var in self.expression_list:
            value = var.Eject(env, gen)
            newArr.append(value.value)
        tmpValue = Value(newArr, False, ExpressionType.ARRAY, [], [], [])
    
        temp = gen.new_temp()

        # Validar tipo
        if tmpValue.Type != ExpressionType.ARRAY:
            # ast.setErrors("La expresion no es un arreglo")
            return None
        nameId = 'arr_'+str(temp)
        gen.variable_data(nameId, 'word', ', '.join(tmpValue.value) )
        # Generar simbolo
        sym = Symbol(self.line, self.column, self.id_, self.Type, nameId)
        # Agregar al entorno
        env.saveVariable(self.id_, sym)
        return None