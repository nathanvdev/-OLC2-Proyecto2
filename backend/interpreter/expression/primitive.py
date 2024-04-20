from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..abstract.value import Value

class Primitive(expression):
    def __init__(self, line, column, value, Type):
        super().__init__(line, column)
        self.value = value
        self.Type = Type
        self.tmpType = Type

    def Eject(self, env, gen):
        temp = gen.new_temp()
        if(self.tmpType == ExpressionType.INTEGER):
            gen.add_br()
            gen.comment('Agregando un primitivo numerico')
            gen.add_li('t0', str(self.value))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, self.tmpType, [], [], [])
        
        elif (self.tmpType == ExpressionType.STRING):
            nameId = 'str_'+str(temp)
            gen.variable_data(nameId, 'string', '\"'+str(self.value)+'\"')
            return  Value(nameId, False, self.tmpType, [], [], [])
 