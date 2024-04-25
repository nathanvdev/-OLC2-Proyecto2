from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..abstract.value import Value


class Relational(expression):
    def __init__(self, line, column, left, right, operator):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator

    def Eject(self, env, gen):
        op1, op2 = self.left.Eject(env, gen), self.right.Eject(env, gen)
        temp = gen.new_temp()
        gen.add_br()
        gen.comment("Relational operation")

        for op, reg in zip([op1, op2], ['t1', 't2']):
            if op.pos == -1:
                gen.add_li(reg, op.value)
            else:
                gen.add_li('t0', op.pos)
                gen.add_lw(reg, '0(t0)')

        if self.operator == '==':
            gen.add_operation('beq', 't1', 't2', 'true_'+str(temp))
        elif self.operator == '!=':
            gen.add_operation('bne', 't1', 't2', 'true_'+str(temp))
        elif self.operator == '>':
            gen.add_operation('bgt', 't1', 't2', 'true_'+str(temp))
        elif self.operator == '<':
            gen.add_operation('bgt', 't2', 't1', 'true_'+str(temp))
        elif self.operator == '>=':
            gen.add_operation('bge', 't1', 't2', 'true_'+str(temp))
        elif self.operator == '<=':
            gen.add_operation('bge', 't2', 't1', 'true_'+str(temp))


        gen.add_li('t0', temp)
        gen.add_li('t1', 0)
        gen.add_sw('t1', '0(t0)')
        gen.add_jump('fin_'+str(temp))
        gen.add_br()

        gen.add_funcName('true_'+str(temp))
        gen.add_li('t0', temp)
        gen.add_li('t1', 1)
        gen.add_sw('t1', '0(t0)')
        gen.add_jump('fin_'+str(temp))
        gen.add_br()

        gen.add_funcName('fin_'+str(temp))

        return Value(0, str(temp), ExpressionType.BOOLEAN, False)
    