from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..abstract.value import Value

class Logica(expression):
    def __init__(self, line, column, left, right, operator):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator

    def Eject(self, env, gen):
        op1, op2 = self.left.Eject(env, gen), self.right.Eject(env, gen)
        temp = gen.new_temp()
        gen.add_br()
        gen.comment("Logical Operation")

        for op, reg in zip([op1, op2], ['t1', 't2']):
            if op.pos == -1:
                gen.add_li(reg, op.value)
            else:
                gen.add_li('t0', op.pos)
                gen.add_lw(reg, '0(t0)')

        if self.operator == '&&':
            gen.add_operation('and', 't3', 't1', 't2')
        elif self.operator == '||':
            gen.add_operation('or', 't3', 't1', 't2')
        elif self.operator == '!':
            gen.add_li('t1', 1)
            gen.add_operation('xor', 't3', 't1', 't2')

        gen.add_li('t0', temp)
        gen.add_sw('t3', '0(t0)')

        return Value(0, str(temp), ExpressionType.BOOLEAN, False)

        
