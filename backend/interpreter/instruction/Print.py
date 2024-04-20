from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType


class Print(instruction):
    def __init__(self, line, column, expression):
        super().__init__(line, column)
        self.expression = expression
        

    def Eject(self, env, gen):
        for exp in self.expression:
            val = exp.Eject(env, gen)
            if (val.Type == ExpressionType.INTEGER):
                # Imprimiendo expresion
                gen.add_br()
                if 't' in str(val.value):
                    gen.add_move('t3', str(val.value))
                else:
                    gen.add_li('t3', str(val.value))
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
                gen.add_system_call()

            elif (val.Type == ExpressionType.STRING):
                gen.add_br()
                if 't' in str(val.value) and len(str(val.value)) < 2:
                    gen.add_move('a0', str(val.value))
                else:
                    gen.add_la('a0', str(val.value))
                gen.add_li('a7', '4')
                gen.add_system_call()
        # Imprimiendo salto de linea
        gen.add_br()
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()

        return None