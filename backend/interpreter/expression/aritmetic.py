from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..abstract.value import Value


class Aritmetic(expression):
    def __init__(self, line, column, left, right, operator):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator

    def Eject(self, env, gen):
         
        op1, op2 = self.left.Eject(env, gen), self.right.Eject(env, gen)
        temp = gen.new_temp()

        gen.add_br()
        gen.comment("Aritmetic operation")

        for op, reg in zip([op1, op2], ['t1', 't2']):
            if op.pos == -1:
                gen.add_li(reg, op.value)
            else:
                gen.add_li('t0', op.pos)
                gen.add_lw(reg, '0(t0)')

        operations = {
            "+": 'add',
            "-": 'sub',
            "*": 'mul',
            "/": 'div',
            "%": 'rem',
            'UMINUS': 'neg'
        }

        if self.operator in operations:
            if self.operator == 'UMINUS':
                gen.add_operation('neg', 't0', 't1','')
            else:
                gen.add_operation(operations[self.operator], 't0', 't1', 't2')

        

        gen.add_li('t3', temp)
        gen.add_sw('t0', '0(t3)')

        return Value(0, str(temp), ExpressionType.INTEGER, False)
            