from enum import Enum

class ExpressionType(Enum):
    INTEGER = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3
    CHAR = 4
    NULL = 5
    BREAK = 6
    CONTINUE = 7
    RETURN = 8
    ARRAY = 9