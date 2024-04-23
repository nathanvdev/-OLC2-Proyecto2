from ..abstract.instruction import instruction
from ..abstract.types import ExpressionType


class Print(instruction):
    def __init__(self, line, column, expression):
        super().__init__(line, column)
        self.expression = expression
        

    def Eject(self, env, gen):
        for exp in self.expression:
            val = exp.Eject(env, gen)
            gen.add_br()
            gen.comment('Imprimiendo expresion')

            if (val.Type == ExpressionType.INTEGER):
                if val.pos == -1:
                    gen.add_li('a0', val.value)
                else:
                    gen.add_li('t0', val.pos)
                    gen.add_lw('a0', '0(t0)')
                gen.add_li('a7', '1')
                gen.add_system_call()

            elif (val.Type == ExpressionType.STRING):
                gen.add_la('a0', val.pos)
                gen.add_li('a7', '4')
                gen.add_system_call()

            elif (val.Type == ExpressionType.BOOLEAN):
                if val.value == 1:
                    gen.add_la('a0', 'TRUExd')
                else:
                    gen.add_la('a0', 'FALSExd')
                gen.add_li('a7', '4')
                gen.add_system_call()

        gen.add_br()
        gen.comment('salto de linea')
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()
        return None