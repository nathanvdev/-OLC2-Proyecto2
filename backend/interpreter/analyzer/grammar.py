import ply.lex as lex
import ply.yacc as yacc
from ..abstract.types import ExpressionType
from ..expression.primitive import Primitive
from ..instruction.Print import Print
from ..expression.aritmetic import Aritmetic
from ..expression.relational import Relational
from ..expression.logica import Logica
from ..instruction.declareVar_ import DeclareVar_
from ..instruction.assignVar_ import AssignVar_
from ..instruction.find_variable import FindVariable
from ..instruction.if_else import If_else
from ..instruction.while_ import while_
from ..instruction.for_ import for_
from ..instruction.return_ import Return_
from ..instruction.declareArr_ import DeclareArr_
from ..instruction.arrayFuncs_ import ArrayFuncs_
from ..instruction.assingArr_ import AssignArr_
# from ..instruction.declareMtrx_ import DeclareMtrx_
from ..instruction.createInterface_ import CreateInterface_
from ..instruction.declareInterface_ import DeclareInterface_
from ..instruction.modifyInterface_ import ModifyInterface_
from ..instruction.switch_ import Switch_
from ..instruction.declareFunc_ import DeclareFunction_
from ..instruction.callFunc_ import CallFunction_
from ..expression.funcEmbebidas_ import funcEmbebidas_
from ..expression.callInterface_ import callInterface_


Errors = []

#palabras reservadas
reserved = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'true': 'TRUE',
    'false': 'FALSE',
    'var': 'RVAR',
    'const': 'RCONST',
    'number': 'RNUMBER',
    'float': 'RFLOAT',
    'string': 'RSTRING',
    'boolean': 'RBOOLEAN',
    'if' : 'RIF',
    'else' : 'RELSE',
    'while' : 'RWHILE',
    'for' : 'RFOR',
    'break' : 'RBREAK',
    'continue' : 'RCONTINUE',
    'return' : 'RRETURN',
    'push' : 'RPUSH',
    'pop' : 'RPOP',
    'indexOf' : 'RINDEXOF',
    'join' : 'RJOIN',
    'length' : 'RLENGTH',
    'interface' : 'RINTERFACE',
    'keys' : 'RKEYS',
    'values' : 'RVALUES',
    'switch' : 'RSWITCH',
    'case' : 'RCASE',
    'default' : 'RDEFAULT',
    'function' : 'RFUNCTION',
    'parseInt' : 'RPARSEINT',
    'parseFloat' : 'RPARSEFLOAT',
    'toString' : 'RTOSTRING',
    'toLowerCase' : 'RTOLOWERCASE',
    'toUpperCase' : 'RTOUPPERCASE',
    'typeof' : 'RTYPEOF',
    'object' : 'ROBJECT',
}

#lista de tokens
tokens = ['PARA', 'PARC', 'DOT', 'DOUBLEDOT', 'LLAVEA', 'LLAVEC', 'SEMICOLON', 
          'QUESTIONM', 'BRACKETO', 'BRACKETC', 'COMMA',
          'NUMBER', 'FLOAT', 'STRING', 'ID',
          'PLUS', 'LESS', 'BY', 'DIVIDED', 'MODUL',
          'EQUAL','DEQUAL','DIFERENT','MINOR','MINOREQUAL','GREATER','GREATEREQUAL',
          'AND','OR','NOT'
          ] + list(reserved.values())


#-----------------------------------------------------definicion de tokens
t_PARA          = r'\('
t_PARC          = r'\)'
t_DOT           = r'\.'
t_DOUBLEDOT     = r'\:'
t_LLAVEA        = r'\{'
t_LLAVEC        = r'\}'
t_SEMICOLON     = r'\;'
t_QUESTIONM     = r'\?'
t_BRACKETO      = r'\['
t_BRACKETC      = r'\]'
t_COMMA         = r'\,'


###Aritmetica
t_PLUS = r'\+'
t_LESS = r'\-'
t_BY = r'\*'
t_DIVIDED = r'\/'
t_MODUL = r'\%'

##Relacionales
t_DEQUAL = r'\=\='
t_EQUAL = r'\='
t_DIFERENT = r'\!\='
t_MINOR = r'\<'
t_MINOREQUAL = r'\<\='
t_GREATER = r'\>'
t_GREATEREQUAL = r'\>\='

##Logicas
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'\!'




def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f'error al parsear el valor: {t.value} \n column: {t.lexpos} line: {t.lineno}')
        t.value = None
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f'error al parsear el valor: {t.value} \n column: {t.lexpos} line: {t.lineno}')
        t.value = None
    return t

def t_STRING(t):
    r'\"(.*?)\"'
    try:
        t.value = str(t.value).replace('"', '')
    except ValueError:
        print(f'error al parsear el valor: {t.value} \n column: {t.lexpos} line: {t.lineno}')
        t.value = None
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    
    return t

t_ignore = " \t"
t_ignore_COMMENTLINE = r'\/\/.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    try:
        print(f'Error lexico {t.value} \n column: {t.lexpos} line: {t.lineno}')
        newError = {
            "Tipo": "Lexico",
            "Linea": t.lineno,
            "Columna": t.lexpos,
            "Ambito": "Global",
            "Descricion": f"Error lexico {t.value}"
        }
        Errors.append(newError)
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
    t.lexer.skip(1) # recuperacion del error



#--------------------------------------------------definicion de la gramatica
    
##precedencia
precedence = (  
                ('left', 'OR'),
                ('left', 'AND'),
                ('left', 'NOT'),
                ('left', 'DEQUAL', 'DIFERENT', 'MINOR', 'MINOREQUAL', 'GREATER', 'GREATEREQUAL'),
                ('left', 'PLUS', 'LESS'), 
                ('left', 'BY','DIVIDED', 'MODUL'), 
                ('right', 'UMENOS')
            )
    


##definicion de la gramatica
def p_start(p):
    '''start    : instrucciones '''
    p[0] = p[1]
    return p[0]
    


def p_instrucciones(p):
    '''instrucciones    : instrucciones instruccion
                        | instruccion'''
    if len(p) > 2:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    
def p_instruccion(p):
    '''instruccion  : print SEMICOLON
                    | declarevar SEMICOLON
                    | declareConst SEMICOLON
                    | assignVar SEMICOLON
                    | declareArray SEMICOLON
                    | declareArrayConst SEMICOLON
                    | assingArray SEMICOLON
                    | arrayFuncs SEMICOLON
                    | if_else
                    | case_inst
                    | ternario SEMICOLON
                    | while_
                    | for_
                    | transfer SEMICOLON
                    | createInterface
                    | declareInterface SEMICOLON
                    | modifyInterface SEMICOLON
                    | declareFunction
                    | callFunction SEMICOLON'''
    p[0] = p[1]


def p_print(p):
    '''print    : CONSOLE DOT LOG PARA expression_list PARC'''
    tmp = get_params(p)
    p[0] = Print(tmp.line, tmp.column, p[5])

def p_declarevar(p):
    '''declarevar  : RVAR ID DOUBLEDOT type EQUAL expression
                | RVAR ID EQUAL expression
                | RVAR ID DOUBLEDOT type'''

    tmp = get_params(p)
    if len(p) == 7:
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], p[4], p[6], False)

    elif p[3] =="=" :
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], None, p[4], False)

    elif p[3] ==":" : 
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], p[4], None, False)

def p_declareConst(p):
    '''declareConst : RCONST ID DOUBLEDOT type EQUAL expression
                    | RCONST ID EQUAL expression
                    | RCONST ID DOUBLEDOT type'''

    tmp = get_params(p)
    if len(p) == 7:
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], p[4], p[6], True)

    elif p[3] =="=" :
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], None, p[4], True)

    elif p[3] ==":" : 
        p[0] = DeclareVar_(tmp.line, tmp.column, p[2], p[4], None, True)



def p_assignVar(p):
    '''assignVar    : ID EQUAL expression
                    | ID PLUS EQUAL expression
                    | ID LESS EQUAL expression'''
    
    tmp = get_params(p)
    if p[2] == '=':
        p[0] = AssignVar_(tmp.line, tmp.column, p[1], '=', p[3])
    elif p[2] == '+':
        p[0] = AssignVar_(tmp.line, tmp.column, p[1], '+=', p[4])
    elif p[2] == '-':
        p[0] = AssignVar_(tmp.line, tmp.column, p[1], '-=', p[4])

def p_declareArray(p):
    '''declareArray : RVAR ID DOUBLEDOT type BRACKETO BRACKETC EQUAL BRACKETO expression_list BRACKETC
                    | RVAR ID DOUBLEDOT type BRACKETO BRACKETC EQUAL expression
                    | RVAR ID DOUBLEDOT type BRACKETO BRACKETC EQUAL BRACKETO BRACKETC'''
    
    tmp = get_params(p)

    if len(p) == 11:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], p[9], False)
    elif len(p) == 9:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], [p[8]], False)
    elif len(p) == 10:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], [], False)

def p_declareArrayConst(p):
    '''declareArrayConst : RCONST ID DOUBLEDOT type BRACKETO BRACKETC EQUAL BRACKETO expression_list BRACKETC
                    | RCONST ID DOUBLEDOT type BRACKETO BRACKETC EQUAL expression
                    | RCONST ID DOUBLEDOT type BRACKETO BRACKETC EQUAL BRACKETO BRACKETC'''
    
    tmp = get_params(p)

    if len(p) == 11:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], p[9], True)
    elif len(p) == 9:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], [p[8]], True)
    elif len(p) == 10:
        p[0] = DeclareArr_(tmp.line, tmp.column, p[2], p[4], [], True)

def p_assingArray(p):
    '''assingArray : ID BRACKETO expression BRACKETC EQUAL expression'''

    tmp = get_params(p)
    p[0] = AssignArr_(tmp.line, tmp.column, p[1], p[3], p[6])

def p_arrayFuncs(p):
    '''arrayFuncs   : ID DOT RPUSH PARA expression PARC'''
    
    tmp = get_params(p)
    p[0] = ArrayFuncs_(tmp.line, tmp.column, p[1], p[3], p[5])


# def p_declareMatrix(p):
#     '''declareMatrix    : declaration_type ID DOUBLEDOT type matrix_dimension EQUAL matrix_values''' 

#     tmp = get_params(p)
#     p[0] = DeclareMtrx_(tmp.line, tmp.column, p[1], p[2], p[4], p[5], p[7])


# def p_matrix_dimension(p):
#     '''matrix_dimension : matrix_dimension BRACKETO expression BRACKETC
#                         | BRACKETO expression BRACKETC'''
#     tmp = get_params(p)
#     if len(p) == 5:
#         p[0] = [p[2]] + p[1]
#     elif len(p) == 4:
#         p[0] = [p[2]]
    
# def p_matrix_values(p):
#     '''matrix_values : BRACKETO matrix_valuesList2 BRACKETC'''

#     tmp = get_params(p)
#     p[0] = p[2]


# def p_matrix_valuesList2(p):
#     '''matrix_valuesList2 : matrix_valuesList2 COMMA BRACKETO args BRACKETC
#                           | BRACKETO args BRACKETC'''
    
#     if len(p) > 4:
#         p[1].append(p[4])
#         p[0] = p[1]
#     else:
#         p[0] = [p[2]]

    
# def p_args(p):
#     '''args : matrix_valuesList2
#             | expression_list'''
    
#     p[0] = p[1]



def p_if_else(p):
    '''if_else  : RIF PARA expression PARC LLAVEA instrucciones LLAVEC else'''

    tmp = get_params(p)
    p[0] = If_else(tmp.line, tmp.column, p[3], p[6], p[8])
    
def p_else(p):
    '''else : RELSE LLAVEA instrucciones LLAVEC
            | RELSE if_else
            |'''
    
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 3:
        p[0] = [p[2]]
    else:
        p[0] = None

def p_case_inst(p):
    '''case_inst : RSWITCH PARA expression PARC LLAVEA cases RDEFAULT DOUBLEDOT instrucciones LLAVEC'''

    tmp = get_params(p)
    p[0] = Switch_(tmp.line, tmp.column, p[3], p[6], p[9])
    

def p_cases(p):
    '''cases : cases case 
             | case'''

    if len(p) > 2:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]
    
def p_case(p):
    '''case : RCASE expression DOUBLEDOT instrucciones'''

    tmp = get_params(p)

    p[0] = {
        'line': tmp.line,
        'column': tmp.column,
        'expression': p[2],
        'instructions': p[4],
    }
    


def p_ternario(p):
    '''ternario : expression QUESTIONM expression DOUBLEDOT expression'''

    tmp = get_params(p)
    p[0] = If_else(tmp.line, tmp.column, p[1], p[3], p[5])

def p_while(p):
    '''while_   : RWHILE PARA expression PARC LLAVEA instrucciones LLAVEC'''
    
    tmp = get_params(p)
    p[0] = while_(tmp.line, tmp.column, p[3], p[6])

def p_for(p):
    '''for_ : RFOR PARA declarevar SEMICOLON relacional SEMICOLON id_ PLUS PLUS PARC LLAVEA instrucciones LLAVEC
            | RFOR PARA declarevar SEMICOLON relacional SEMICOLON id_ LESS LESS PARC LLAVEA instrucciones LLAVEC'''
    #                    [3]                 [5]                  [7]  [8]                        [12]
    
    tmp = get_params(p)
    p[0] = for_(tmp.line, tmp.column, p[3], p[5], p[7], p[8], p[12])

def p_transfer(p):
    '''transfer : RBREAK
                | RCONTINUE
                | RRETURN
                | RRETURN expression'''
    
    tmp = get_params(p)

    if len(p) == 3:
        p[0] = Return_(tmp.line, tmp.column, p[2])
        
    else:
        if p[1] == 'break':
            
            p[0] = Primitive(tmp.line, tmp.column, None, ExpressionType.BREAK)

        elif p[1] == 'continue':
            p[0] = Primitive(tmp.line, tmp.column, None, ExpressionType.CONTINUE)

        elif p[1] == 'return':
            p[0] = Primitive(tmp.line, tmp.column, None, ExpressionType.RETURN)

def p_createInterface(p):
    '''createInterface : RINTERFACE ID LLAVEA attributesList LLAVEC'''

    tmp = get_params(p)
    p[0] = CreateInterface_(tmp.line, tmp.column, p[2], p[4])
    

def p_attributesList(p):
    '''attributesList : attributesList ID DOUBLEDOT type SEMICOLON
                      | ID DOUBLEDOT type SEMICOLON'''

    if len(p) > 5:
        param = {p[2] : p[4]}
        p[1].append(param)
        p[0] = p[1]
    else:
        param = {p[1] : p[3]}
        p[0] = [param]



def p_declareInterface(p):
    '''declareInterface : RVAR ID DOUBLEDOT ID EQUAL LLAVEA interfaceContent LLAVEC
                        | RCONST ID DOUBLEDOT ID EQUAL LLAVEA interfaceContent LLAVEC'''

    tmp = get_params(p)
    p[0] = DeclareInterface_(tmp.line, tmp.column, p[2], p[4], p[7])
    
def p_interface_content(t):
    '''interfaceContent : interfaceContent COMMA ID DOUBLEDOT expression
                        | ID DOUBLEDOT expression'''
    
    arr = []
    if len(t) > 5:
        param = {t[3] : t[5]}
        arr = t[1] + [param]
    else:
        param = {t[1] : t[3]}
        arr.append(param)
    t[0] = arr

def p_modifyInterface(p):
    '''modifyInterface  : ID DOT ID EQUAL expression'''

    tmp = get_params(p)
    p[0] = ModifyInterface_(tmp.line, tmp.column, p[1], p[3], p[5])
        
def p_declareFunction(p):
    '''declareFunction : RFUNCTION ID PARA funcparams PARC returntype LLAVEA instrucciones LLAVEC'''

    tmp = get_params(p)
    p[0] = DeclareFunction_(tmp.line, tmp.column, p[2], p[4], p[6], p[8])

def p_funcparams(p):
    '''funcparams : funcparams COMMA param
                  | param
                  |'''  
    
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_param(p):
    '''param : ID DOUBLEDOT type'''

    tmp = get_params(p)
    p[0] = {
        'line': tmp.line,
        'column': tmp.column,
        'id_': p[1],
        'Type': p[3]
    }

def p_returntype(p):
    '''returntype : DOUBLEDOT type
                  |'''

    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_callFunction(p):
    '''callFunction : ID PARA expression_list PARC
                    | ID PARA PARC'''

    tmp = get_params(p)
    if len(p) == 5:
        p[0] = CallFunction_(tmp.line, tmp.column, p[1], p[3])
    elif len(p) == 4:
        p[0] = CallFunction_(tmp.line, tmp.column, p[1], [])


def p_expression(p):
    '''expression   : primitivo 
                    | aritmetica
                    | relacional
                    | logica
                    | expression_group
                    | id_
                    | arraysExpression
                    | callInterface
                    | boolean
                    | callFunction
                    | funcEmbebida'''
    
    p[0] = p[1]

def p_funcEmbebida(p):
    '''funcEmbebida : RPARSEINT PARA expression PARC
                    | RPARSEFLOAT PARA expression PARC
                    | ID DOT RTOSTRING PARA PARC
                    | FALSE DOT RTOSTRING PARA PARC
                    | ID DOT RTOLOWERCASE PARA PARC
                    | ID DOT RTOUPPERCASE PARA PARC
                    | RTYPEOF expression'''

    tmp = get_params(p)
    if p[1] == 'false':
        tmp45 = Primitive(tmp.line, tmp.column, False, ExpressionType.BOOLEAN)
        p[0] = funcEmbebidas_(tmp.line, tmp.column, p[3], tmp45)
    elif len(p) == 5:
        p[0] = funcEmbebidas_(tmp.line, tmp.column, p[1], p[3])
    elif len(p) == 6:
        tmp43 = FindVariable(tmp.line, tmp.column, p[1])
        p[0] = funcEmbebidas_(tmp.line, tmp.column, p[3], tmp43)
    elif len(p) == 3:
        p[0] = funcEmbebidas_(tmp.line, tmp.column, p[1], p[2])

def p_expression_group(p):
    '''expression_group   : PARA expression PARC'''
    p[0] = p[2]

def p_interfaceContent(p):
    '''callInterface    : ID DOT ID
                        | ROBJECT DOT RKEYS PARA ID PARC
                        | ROBJECT DOT RVALUES PARA ID PARC'''

    tmp = get_params(p)
    if len(p) == 4:
        p[0] = callInterface_(tmp.line, tmp.column, p[1], p[3])
    elif len(p) == 7:
        p[0] = callInterface_(tmp.line, tmp.column, p[5], p[3])



def p_expression_list(p):
    '''expression_list  : expression_list COMMA expression
                         | expression'''
    
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_id_(p):
    '''id_  : ID
            | ID BRACKETO expression BRACKETC'''

    tmp = get_params(p)
    if len(p) == 2:
        p[0] = FindVariable(tmp.line, tmp.column, p[1])
    elif len(p) == 5:
        p[0] = ArrayFuncs_(tmp.line, tmp.column, p[1], 'Find', p[3])


def p_aritmetica(p):
    '''aritmetica   : expression PLUS expression
                    | expression BY expression
                    | expression DIVIDED expression
                    | expression LESS expression
                    | expression MODUL expression
                    | LESS expression %prec UMENOS'''
    

    tmp = get_params(p)
    if p.slice[1].type == 'LESS':
        p[0] = Aritmetic(tmp.line, tmp.column, p[2], p[2], 'UMINUS')

    elif p.slice[2].type == 'PLUS':
        p[0] = Aritmetic(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'LESS':
        p[0] = Aritmetic(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'BY':
        p[0] = Aritmetic(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'DIVIDED':
        p[0] = Aritmetic(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'MODUL':
        p[0] = Aritmetic(tmp.line, tmp.column, p[1], p[3], p[2])


def p_relacional(p):
    '''relacional   : expression DEQUAL expression
                    | expression DIFERENT expression
                    | expression MINOR expression
                    | expression MINOREQUAL expression
                    | expression GREATER expression
                    | expression GREATEREQUAL expression'''
    
    tmp = get_params(p)

    if p.slice[2].type == 'DEQUAL':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'DIFERENT':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'MINOR':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'MINOREQUAL':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'GREATER':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'GREATEREQUAL':
        p[0] = Relational(tmp.line, tmp.column, p[1], p[3], p[2])


def p_logica(p):
    '''logica   : expression AND expression
                | expression OR expression
                | NOT expression'''
    tmp = get_params(p)

    if p.slice[2].type == 'AND':
        p[0] = Logica(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[2].type == 'OR':
        p[0] = Logica(tmp.line, tmp.column, p[1], p[3], p[2])

    elif p.slice[1].type == 'NOT':
        p[0] = Logica(tmp.line, tmp.column, p[2], p[2], p[1])

def p_primitivo(p):
    '''primitivo    : NUMBER
                    | FLOAT
                    | STRING'''

    tmp = get_params(p)

    if p.slice[1].type == 'NUMBER':
        p[0] = Primitive(tmp.line, tmp.column, p[1], ExpressionType.INTEGER)
    elif p.slice[1].type == 'FLOAT':
        p[0] = Primitive(tmp.line, tmp.column, p[1], ExpressionType.FLOAT)
    elif p.slice[1].type == 'STRING':
        p[0] = Primitive(tmp.line, tmp.column, p[1], ExpressionType.STRING)
    else:
        p[0] = p[1]

def p_arraysExpression(p):
    '''arraysExpression : ID DOT RPOP PARA PARC
                        | ID DOT RINDEXOF PARA expression PARC
                        | ID DOT RJOIN PARA PARC
                        | ID DOT RLENGTH'''
    
    tmp = get_params(p)
    if len(p) == 4:
        p[0] = ArrayFuncs_(tmp.line, tmp.column, p[1], p[3], None)
    else:
        p[0] = ArrayFuncs_(tmp.line, tmp.column, p[1], p[3], p[5])



def p_boolean(p):
    '''boolean  : TRUE
                | FALSE'''

    tmp = get_params(p)

    if p[1] == 'true':
        p[0] = Primitive(tmp.line, tmp.column, True, ExpressionType.BOOLEAN)
    elif p[1] == 'false':
        p[0] = Primitive(tmp.line, tmp.column, False, ExpressionType.BOOLEAN)

def p_type(p):
    '''type     : RNUMBER
                | RFLOAT
                | RSTRING
                | RBOOLEAN
                | type BRACKETO BRACKETC'''
    
    if p[1] == 'number':
        p[0] = ExpressionType.INTEGER
    elif p[1] == 'float':
        p[0] = ExpressionType.FLOAT
    elif p[1] == 'string':
        p[0] = ExpressionType.STRING
    elif p[1] == 'boolean':
        p[0] = ExpressionType.BOOLEAN
    else:
        p[0] = p[1]



def p_error(p):
    try:
        if p:
            newError = {
                "Tipo": "Sintactico",
                "Linea": p.lineno,
                "Columna": p.lexpos,
                "Ambito": "Global",
                "Descricion": f"Error sintactico linea:{p.lineno}, col:{p.lexpos} Token: {p.value}"
            }
            Errors.append(newError)
            print(f'Error sintactico linea:{p.lineno}, col:{p.lexpos} Token: {p.value}')
        else:
            print(f'Error de sintaxis  \n column: {p.lexpos} line: {p.lineno}')
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column
        
def get_params(t):
    line = t.lexer.lineno  # Obtener la línea actual desde el lexer
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0  # Verificar si lexpos es un entero
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)


def parse(input_text, GlobalErrors):
    lexer = lex.lex() #lexico
    parser = yacc.yacc() #sintactico
    result = parser.parse(input_text)
    GlobalErrors.extend(Errors)
    
    return result


