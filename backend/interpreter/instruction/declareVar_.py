from ..abstract.instruction import instruction
from ..abstract.environment import Environment
from ..abstract.symbol import Symbol
from ..abstract.types import ExpressionType
from ..abstract.value import Value



class DeclareVar_(instruction):
    def __init__(self, line, column, id, type, expression, const):
        super().__init__(line, column)
        self.id = id 
        self.Type = type
        self.value = expression
        self.const = const

    def Eject(self, env: Environment, gen):
        result = self.value.Eject(env, gen)

        if self.Type is None and self.value is not None:
            self.Type = result.Type

        if self.Type is not None and self.value is not None and self.Type != result.Type:
            print(f'Error: Type mismatch \n column: {self.column} line: {self.line}')
            return

        temp = gen.new_temp()
        gen.add_br()

        if result.Type in [ExpressionType.INTEGER, ExpressionType.BOOLEAN]:
            gen.comment(f'Agregando un primitivo {"numerico" if result.Type == ExpressionType.INTEGER else "booleano"}')
            if result.pos == -1:
                    gen.add_li('t0', str(result.value))
            else:
                gen.add_li('t0', result.pos)
                gen.add_lw('t0', '0(t0)')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
        elif result.Type == ExpressionType.STRING:
            gen.comment('Agregando un primitivo string')
            nameId = 'str_'+str(temp)
            gen.variable_data(nameId, 'string', '\"'+str(result.value)+'\"')
            temp = nameId

        sym = Symbol(self.line, self.column, self.id, result.value, str(temp), result.Type)
        env.saveVariable(self.id, sym)
        return Value(result.value if result.Type == ExpressionType.BOOLEAN else 0, str(temp), result.Type, result.Type != ExpressionType.STRING)