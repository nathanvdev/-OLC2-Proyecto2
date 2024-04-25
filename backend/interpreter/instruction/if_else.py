from ..abstract.instruction import instruction
from ..abstract.environment import Environment


class If_else(instruction):
    def __init__(self, line, column, condition, if_instructions, else_instructions):
        super().__init__(line, column)
        self.condition = condition
        self.if_instructions = if_instructions
        self.else_instructions = else_instructions

    def Eject(self, env, gen):
        tmp = gen.new_temp()
        result = self.condition.Eject(env, gen)
        env.envsCount += 1
        gen.comment('IF Sentence')

        if result.pos == -1:
            gen.add_li("t1", result.value)
        else:
            gen.add_li('t0', result.pos)
            gen.add_lw("t1", '0(t0)')

        
        gen.add_operation('beq', 't1', 'x0', "else_inst"+str(tmp))
        newEnv = Environment(env, f'{env.envsCount}-if')

        for inst in self.if_instructions:
            inst.Eject(newEnv, gen)
        gen.add_jump('fin_if'+str(tmp))
        gen.add_br()

        gen.add_funcName('else_inst'+str(tmp))
        if self.else_instructions != None:
            newEnv2 = Environment(env, f'{env.envsCount}-else')
            for inst in self.else_instructions:
                inst.Eject(newEnv2, gen)
            gen.add_jump('fin_if'+str(tmp))
            gen.add_br()

        gen.add_funcName('fin_if'+str(tmp))
        gen.add_br()
        return None
