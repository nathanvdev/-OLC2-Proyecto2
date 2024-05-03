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
        tmpValues = []
        gen.add_br()
        for var in self.expression_list:
            value = var.Eject(env, gen)
            tmp = gen.new_temp()
            gen.add_li('t0', str(value.value))
            gen.add_li('t3', str(tmp))
            gen.add_sw('t0', '0(t3)')
            newArr.append(str(tmp))
            tmpValues.append(value.value)
        tmpValue = Value(0, newArr, ExpressionType.ARRAY, False)
    
        temp = gen.new_temp()

        # Validar tipo
        if tmpValue.Type != ExpressionType.ARRAY:
            # ast.setErrors("La expresion no es un arreglo")
            return None
        
        # Generar simbolo
        sym = Symbol(self.line, self.column, self.id_, tmpValues, newArr, ExpressionType.ARRAY)
        # Agregar al entorno
        env.saveVariable(self.id_, sym)
        return None