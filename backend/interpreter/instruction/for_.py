from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..expression.primitive import Primitive



class for_(instruction):
    def __init__(self, line, column, assignment, condition, evalue, op, instructions):
        super().__init__(line, column)
        self.assignment = assignment
        self.condition = condition
        self.evalue = evalue
        self.op = op
        self.instructions = instructions


    def Eject(self, env:Environment, gen):
        newEnv = Environment(env, f'{env.envsCount}-for')
        tmp = gen.new_temp()
        assing = self.assignment.Eject(newEnv, gen)
        
        gen.add_br()
        gen.comment('For Sentence')
        gen.add_funcName('startFor_'+str(tmp))

        result = self.condition.Eject(newEnv, gen)
        if result.pos == -1:
            gen.add_li("t1", result.value)
        else:
            gen.add_li('t0', result.pos)
            gen.add_lw("t1", '0(t0)')
        
        gen.add_operation('beq', 't1', 'x0', "finFor_"+str(tmp))

        for inst in self.instructions:
            inst.Eject(newEnv, gen)

        if assing.pos == -1:
            gen.add_li("t1", assing.value)
        else:
            gen.add_li('t0', assing.pos)
            gen.add_lw("t1", '0(t0)')

        gen.add_li('t2', 1)
        if self.op == '+':
            gen.add_operation('add', 't1', 't1', 't1')
        elif self.op == '-':
            gen.add_operation('sub', 't1', 't1', 't1')
        gen.add_sw('t1', '0(t0)')
        gen.add_jump('startFor_'+str(tmp))
        gen.add_br()
        gen.add_funcName('finFor_'+str(tmp))
        return None