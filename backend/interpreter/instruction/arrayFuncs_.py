from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType
from ..abstract.value import Value

class ArrayFuncs_(instruction):
    def __init__(self, line, column, id_, FuncType, expression):
        super().__init__(line, column)
        self.id_ = id_
        self.FuncType = FuncType
        self.expression = expression

    def Eject(self, env, gen):
        # Traer el arreglo
        sym = env.getVariable(self.id_)
        if(sym.Type == ExpressionType.NULL):
            # ast.setErrors(f"El arreglo {self.array} no ha sido encontrado")
            return None
        # Validar tipo principal
        if self.expression != None:
            expression = self.expression.Eject(env, gen)
            if expression.Type != ExpressionType.INTEGER:
                # ast.setErrors('El indice contiene un valor incorrecto')
                return None

        if self.FuncType == "Find":
           
            # Agregar llamada
            gen.add_br()
            gen.comment('Acceso a un arreglo')

            for i in range(len(sym.pos)):
                if i == expression.value:
                    return Value(sym.value[i], sym.pos[i], ExpressionType.INTEGER, False)
                
        elif self.FuncType == 'push':
            tmp = gen.new_temp()
            gen.add_li('t0', str(expression.value))
            gen.add_li('t3', str(tmp))
            gen.add_sw('t0', '0(t3)')
            sym.value.append(expression.value)
            sym.pos.append(tmp)
            return None
            
        elif self.FuncType == 'pop':
            tmpval = sym.value.pop()
            tmppos = sym.pos.pop()
            return Value(tmpval, tmppos, ExpressionType.INTEGER, False)
        
        elif self.FuncType == 'indexOf':
            for i in range(len(sym.value)):
                if sym.value[i] == expression.value:
                    return Value(i, -1, ExpressionType.INTEGER, False)

            return Value(-1, -1, ExpressionType.INTEGER, False)
        
        elif self.FuncType == 'length':
            return Value(len(sym.value), -1, ExpressionType.INTEGER, False)
