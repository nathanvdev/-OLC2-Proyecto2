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
                tmp = gen.new_temp()

                if val.pos == -1:
                    gen.add_li('t1', val.value)
                else:
                    gen.add_li('t0', val.pos)
                    gen.add_lw('t1', '0(t0)')

                gen.add_operation('beq', 't1', 'x0', "prntF"+str(tmp))
                gen.add_la('a0', 'TRUExd')
                gen.add_li('a7', '4')
                gen.add_system_call()
                gen.add_jump('fin'+str(tmp))
                gen.add_br()

                gen.add_funcName("prntF"+str(tmp))
                gen.add_la('a0', 'FALSExd')
                gen.add_li('a7', '4')
                gen.add_system_call()
                gen.add_jump('fin'+str(tmp))
                gen.add_br()

                gen.add_funcName('fin'+str(tmp))
                gen.add_br()

        gen.add_br()
        gen.comment('salto de linea')
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()
        return None