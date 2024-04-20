from ..expression.primitive import Primitive
from ..abstract.types import ExpressionType

class Array_():
    def __init__(self, id, Type, value, const):
        self.id = id
        self.Type = Type
        self.value = value
        self.const = const
        self.size = 0

    def Push(self, expression):
        if expression.Type != self.Type:
            print(f'Error: Type mismatch \n column: {self.column} line: {self.line}')
            return
        self.value.append(expression)
    
    def Pop(self):
        return self.value.pop()

    def IndexOf(self, expression):

        for i in range(len(self.value)):
            if self.value[i].value == expression.value:
                return Primitive(0, 0, i, ExpressionType.INTEGER)
            
        return Primitive(0, 0, -1, ExpressionType.INTEGER)
    
    def Join(self):
        result = ''
        for value in self.value:
            result += str(value.value) + ','

        result = result[:-1]
        return Primitive(0, 0, result, ExpressionType.STRING)
    
    def Length(self):
        return Primitive(0, 0, len(self.value), ExpressionType.INTEGER)
    
    def Find(self, expression):
        if expression.Type != ExpressionType.INTEGER:
            print(f'Error: Type mismatch \n column: {self.column} line: {self.line}')
            return None
        
        if self.value[expression.value]:
            return self.value[expression.value]

        print(f'Error: Value not found \n column: {self.column} line: {self.line}')
        return None
    
    def Assign(self, index, value):
        self.value[index.value] = value
        return
    