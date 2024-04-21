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
        if self.FuncType == "Find":
           # Traer el arreglo
            sym = env.getVariable(self.id_)
            if(sym.Type == ExpressionType.NULL):
                # ast.setErrors(f"El arreglo {self.array} no ha sido encontrado")
                return None
            # Validar tipo principal
            expression = self.expression.Eject(env, gen)
            if expression.Type != ExpressionType.INTEGER:
                # ast.setErrors('El indice contiene un valor incorrecto')
                return None
            # Agregar llamada
            gen.add_br()
            gen.comment('Acceso a un arreglo')
            if 't' in str(expression.value):
                gen.add_move('t3', str(expression.value))
            else:
                gen.add_li('t3', str(expression.value))
            gen.add_lw('t1', '0(t3)')
            gen.add_move('t0', 't1')
            gen.add_slli('t0', 't0', '2')
            gen.add_la('t1', str(sym.position))

            gen.add_lw('t1', '0(t1)')

            gen.add_operation('add', 't2', 't1', 't0')
            return Value('t2', True, sym.Type, [], [], [])