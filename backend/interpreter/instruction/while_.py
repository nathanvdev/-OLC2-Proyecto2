from ..abstract.instruction import instruction
from ..abstract.environment import Environment


class while_(instruction):
    def __init__(self, line, column, condition, instructions):
        super().__init__(line, column)
        self.condition = condition
        self.instructions = instructions


    def Eject(self, env, gen):
        tmp = gen.new_temp()
        gen.add_br()
        gen.comment('While Sentence')
        gen.add_funcName('startWhile_'+str(tmp))
        result = self.condition.Eject(env, gen)
        
        
        if result.pos == -1:
            gen.add_li("t1", result.value)
        else:
            gen.add_li('t0', result.pos)
            gen.add_lw("t1", '0(t0)')

        gen.add_operation('beq', 't1', 'x0', "finWhile_"+str(tmp))
        env.envsCount += 1
        newEnv = Environment(env, f'{env.envsCount}-while')

        for inst in self.instructions:
            inst.Eject(newEnv, gen)
        gen.add_jump('startWhile_'+str(tmp))
        gen.add_br()
        gen.add_funcName("finWhile_"+str(tmp))
        gen.add_br()

        return None

