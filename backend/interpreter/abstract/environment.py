from ..abstract.variables import Variables
from ..expression.primitive import Primitive
from ..abstract.types import ExpressionType


class Environment():
    def __init__(self, previus, name):  
        self.previus = previus
        self.name = name
        self.varibles = {}
        self.functions = {}
        self.arrays = {}
        self.interfaces = {}
        self.console = ""
        self.envsCount = 0
        self.Errors = []
        self.Symbols = []

    def SaveVariable(self, newVar: Variables):
        globalenv = self.GetGlobal()
        if newVar.id_ in self.varibles:
            if self.varibles[newVar.id_].Type != newVar.Type:
                print(f'Error: Type mismatch \n column: {newVar.column} line: {newVar.line}')
                return None
            self.varibles[newVar.id_] = newVar
            newVarSymbol = {
                "id": newVar.id_,
                "symbol_type": "variable",
                "ambito": self.name,
                "line": newVar.line,
                "column": newVar.column
            }
            globalenv.Symbols.append(newVarSymbol)
            print(f'Variable updated: {newVar.id_}')
        else:
            newVarSymbol = {
                "id": newVar.id_,
                "symbol_type": "variable",
                "ambito": self.name,
                "line": newVar.line,
                "column": newVar.column
            }
            globalenv.Symbols.append(newVarSymbol)

            self.varibles[newVar.id_] = newVar
            print(f'Variable saved: {newVar.id_}')

    def AssignVariable(self, line, column, name, op, value):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.varibles:
                if env.varibles[name].const:
                    newError = {
                        "Tipo": "Semantico",
                        "Linea": line,
                        "Columna": column,
                        "Ambito": env.name,
                        "Descricion": "Error en la asignacion de variable"
                    }
                    globalenv.Errors.append(newError)
                    print(f'Error: Variable {name} is constant \n column: {column} line: {line}')
                    return
                if env.varibles[name].Type != value.Type:
                    newError = {
                        "Tipo": "Semantico",
                        "Linea": line,
                        "Columna": column,
                        "Ambito": env.name,
                        "Descricion": "Error de tipo en la asignacion de variable"
                    }
                    globalenv.Errors.append(newError)
                    print(f'Error: Type mismatch \n column: {column} line: {line}')
                    return
                if op == '=':
                    env.varibles[name].value = value
                    return
                elif op == '+=':
                    env.varibles[name].value.value += value.value
                    return
                elif op == '-=':
                    env.varibles[name].value.value -= value.value
                    return
                elif op == '*=':
                    env.varibles[name].value.value *= value.value
                    return
                elif op == '/=':
                    env.varibles[name].value.value /= value.value
                    return
            env = env.previus
        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la asignacion de variable"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Variable {name} not found \n column: {column} line: {line}')

    def ForceAssignVariable(self, line, column, name, op, value):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.varibles:
                if env.varibles[name].Type != value.Type:
                    newError = {
                        "Tipo": "Semantico",
                        "Linea": line,
                        "Columna": column,
                        "Ambito": env.name,
                        "Descricion": "Error de tipo en la asignacion de variable"
                    }
                    globalenv.Errors.append(newError)
                    print(f'Error: Type mismatch \n column: {column} line: {line}')
                    return
                if op == '=':
                    env.varibles[name].value = value
                    return
                elif op == '+=':
                    env.varibles[name].value.value += value.value
                    return
                elif op == '-=':
                    env.varibles[name].value.value -= value.value
                    return
                elif op == '*=':
                    env.varibles[name].value.value *= value.value
                    return
                elif op == '/=':
                    env.varibles[name].value.value /= value.value
                    return
            env = env.previus
        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la asignacion de variable"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Variable {name} not found \n column: {column} line: {line}')


    def Get_Variable(self, line, column, name):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.varibles:
                return env.varibles[name]
            env = env.previus

        env = self
        while env is not None:
            if name in env.arrays:
                return env.arrays[name]
            env = env.previus

        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la obtencion de variable"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Variable {name} not found \n column: {column} line: {line}')
        return None
    
    def SaveArray(self, line, column, newArray):
        globalenv = self.GetGlobal()
        if newArray.id in self.arrays:
            newError = {
                "Tipo": "Semantico",
                "Linea": line,
                "Columna": column,
                "Ambito": self.name,
                "Descricion": "Error en la declaracion de array"
            }
            globalenv.Errors.append(newError)
            print(f'Error: Array {newArray.id} already exists \n column: {column} line: {line}')
            return
        self.arrays[newArray.id] = newArray
        newvarSymbol = {
            "id": newArray.id,
            "symbol_type": "array",
            "ambito": self.name,
            "line": line,
            "column": column
        }
        globalenv.Symbols.append(newvarSymbol)
        print(f'Array saved: {newArray.id}')

    def GetArray(self, line, column, name):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.arrays:
                return env.arrays[name]
            env = env.previus
        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la obtencion de array"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Array {name} not found \n column: {column} line: {line}')
        return None
    
    def SaveInterface(self, newInterface):
        globalenv = self.GetGlobal()
        if newInterface.id_ in self.interfaces:
            newError = {
                "Tipo": "Semantico",
                "Linea": newInterface.line,
                "Columna": newInterface.column,
                "Ambito": self.name,
                "Descricion": "Error en la declaracion de interfaz"
            }
            globalenv.Errors.append(newError)
            print(f'Error: Interface {newInterface.id_} already exists \n column: {newInterface.column} line: {newInterface.line}')
            return
        self.interfaces[newInterface.id_] = newInterface
        newvarSymbol = {
            "id": newInterface.id_,
            "symbol_type": "interface",
            "data-type": "interface",
            "ambito": self.name,
            "line": newInterface.line,
            "column": newInterface.column
        }
        globalenv.Symbols.append(newvarSymbol)
        print(f'Interface saved: {newInterface.id_}')

    def GetInterface(self, line, column, name):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.interfaces:
                return env.interfaces[name]
            env = env.previus
        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la obtencion de interfaz"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Interface {name} not found \n column: {column} line: {line}')
        return None

    def GetGlobal(self):
        env = self
        while env.previus != None:
            env = env.previus
        return env
    
    def SaveFunction(self, id_, function):
        globalenv = self.GetGlobal()
        if id_ in self.functions:
            newError = {
                "Tipo": "Semantico",
                "Linea": function.line,
                "Columna": function.column,
                "Ambito": self.name,
                "Descricion": "Error en la declaracion de funcion"
            }
            globalenv.Errors.append(newError)
            print(f'Error: Function {id_} already exists \n column: {function.column} line: {function.line}')
            return
        self.functions[id_] = function
        newvarSymbol = {
            "id": id_,
            "symbol_type": "function",
            "data-type": "function",
            "ambito": self.name,
            "line": function.line,
            "column": function.column
        }
        globalenv.Symbols.append(newvarSymbol)
        print(f'Function saved: {id_}')

    def GetFunction(self, id_):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if id_ in env.functions:
                return env.functions[id_]
            env = env.previus
        newError = {
            "Tipo": "Semantico",
            "Linea": 0,
            "Columna": 0,
            "Ambito": self.name,
            "Descricion": "Error en la obtencion de funcion"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Function {id_} not found')
