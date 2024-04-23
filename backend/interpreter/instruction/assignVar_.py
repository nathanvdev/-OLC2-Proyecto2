from ..abstract.instruction import instruction
from ..abstract.symbol import Symbol

class AssignVar_(instruction):
    def __init__(self, line, column, name, op, expression):
        super().__init__(line, column)
        self.name = name
        self.op = op
        self.expression = expression

    def Eject(self, env, gen):

        var = env.getVariable(self.name)
        result = self.expression.Eject(env, gen)

        gen.add_br()
        gen.comment('Asignando valor a variable')
        gen.add_li('t0', str(var.pos))

        if self.op == '=':
            gen.add_li('t1', str(result.value))

        elif self.op == '+=':
            gen.add_lw('t1', '0(t0)')
            gen.add_li('t2', str(result.value))
            gen.add_operation('add', 't1', 't1', 't2')

        elif self.op == '-=':
            gen.add_lw('t1', '0(t0)')
            gen.add_li('t2', str(result.value))
            gen.add_operation('sub', 't1', 't1', 't2')

        gen.add_sw('t1', '0(t0)')

        sym = Symbol(self.line, self.column, self.name, result.value, var.pos, result.Type)
        env.setVariable(self.name, sym)
        return None
