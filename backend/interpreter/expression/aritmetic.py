from ..abstract.expression import expression
from ..abstract.types import ExpressionType
from ..abstract.value import Value

dominant_table = [
    [ExpressionType.INTEGER,    ExpressionType.FLOAT,   ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.FLOAT,      ExpressionType.FLOAT,   ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,       ExpressionType.NULL,    ExpressionType.STRING,  ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,       ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,       ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL,    ExpressionType.NULL],
]


class Aritmetic(expression):
    def __init__(self, line, column, left, right, operator):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator

    def Eject(self, env, gen):
         # Ejecución de operandos
        op1 = self.left.Eject(env, gen)
        op2 = self.right.Eject(env, gen)

        gen.add_br()
        gen.comment('Realizando operacion')
        if 't' in str(op1.value):
            gen.add_move('t3', str(op1.value))
        else:
            gen.add_li('t3', str(op1.value))
        #gen.add_li('t3', str(op1.value))
        gen.add_lw('t1', '0(t3)')
        if 't' in str(op2.value):
            gen.add_move('t3', str(op2.value))
        else:
            gen.add_li('t3', str(op2.value)) 
        #gen.add_li('t3', str(op2.value))
        gen.add_lw('t2', '0(t3)')
        temp = gen.new_temp()

        if self.operator == "+":
            gen.add_operation('add', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.INTEGER, [], [], [])
    
        if self.operator == "-":
            gen.add_operation('sub', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.INTEGER, [], [], [])
        
        if self.operator == "*":
            gen.add_operation('mul', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.INTEGER, [], [], [])
        
        if self.operator == "/":
            gen.add_operation('div', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.INTEGER, [], [], [])
        
        return None