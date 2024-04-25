from ..abstract.instruction import instruction

class Switch_(instruction):
    def __init__(self, line, column, expression_, cases_, default_):
        super().__init__(line, column)
        self.expression = expression_
        self.cases = cases_
        self.default = default_


    def Eject(self, env, gen):
        result = self.expression.Eject(env, gen)
        tmp = gen.new_temp()

        gen.add_br()
        gen.comment('Switch Sentence')

        if result.pos == -1:
            gen.add_li("t1", result.value)
        else:
            gen.add_li('t0', result.pos)
            gen.add_lw("t1", '0(t0)')

        caseCount = 0
        for case in self.cases:
            expr = case['expression'].Eject(env, gen)
            if expr.pos == -1:
                gen.add_li("t2", expr.value)
            else:
                gen.add_li('t0', expr.pos)
                gen.add_lw("t2", '0(t0)')
                
            gen.add_operation('beq', 't1', 't2', f'case_{caseCount}_{tmp}')
            caseCount += 1

        for default in self.default:
            default.Eject(env, gen) 
        gen.add_jump(f'fin_switch_{tmp}')
        gen.add_br()

        caseCount = 0
        for case in self.cases:
            gen.add_funcName(f'case_{caseCount}_{tmp}')
            caseCount += 1
            for inst in case['instructions']:
                inst.Eject(env, gen)
            gen.add_jump(f'fin_switch_{tmp}')
            gen.add_br()

        gen.add_funcName(f'fin_switch_{tmp}')
        gen.add_br()


        return None