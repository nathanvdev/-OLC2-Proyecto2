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
        if(self.tmpType == ExpressionType.INTEGER):
            return  Value(self.value, -1, self.tmpType, False)
        
        elif (self.tmpType == ExpressionType.STRING):
            temp = gen.new_temp()
            nameId = 'str_'+str(temp)
            gen.variable_data(nameId, 'string', '\"'+str(self.value)+'\"')
            return  Value(self.value, nameId, self.tmpType, False)
        
        elif (self.tmpType == ExpressionType.BOOLEAN):
            if self.value == True:
                return  Value(1, -1, self.tmpType, True)
            
            elif self.value == False:
                return  Value(0, -1, self.tmpType, True)
 