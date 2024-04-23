from .symbol import Symbol
from .types import ExpressionType 

class Environment():
    def __init__(self, previous, name):  
        self.previous = previous
        self.name = name
        self.variables = {}
        self.functions = {}
        self.arrays = {}
        self.interfaces = {}
        self.console = ""
        self.envsCount = 0
        self.Errors = []
        self.Symbols = []

    def saveVariable(self, id, symbol):
        if id in self.variables:
            # ast.setErrors(f"La variable {id} ya existe.")
            return
        self.variables[id] = symbol

    def setVariable(self, id, symbol):
        tmpEnv = self
        while True:
            if id in tmpEnv.variables:
                tmpEnv.variables[id] = symbol
                return symbol
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        # ast.setErrors(f"La variable {id} no existe.")
        return Symbol(0, 0, None, ExpressionType.NULL)

    def AssignVariable(self, line, column, name, op, value):
        globalenv = self.GetGlobal()
        env = self
        while env != None:
            if name in env.variables:
                if env.variables[name].const:
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
                if env.variables[name].Type != value.Type:
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
                    env.variables[name].value = value
                    return
                elif op == '+=':
                    env.variables[name].value.value += value.value
                    return
                elif op == '-=':
                    env.variables[name].value.value -= value.value
                    return
                elif op == '*=':
                    env.variables[name].value.value *= value.value
                    return
                elif op == '/=':
                    env.variables[name].value.value /= value.value
                    return
            env = env.previous
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
            if name in env.variables:
                if env.variables[name].Type != value.Type:
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
                    env.variables[name].value = value
                    return
                elif op == '+=':
                    env.variables[name].value.value += value.value
                    return
                elif op == '-=':
                    env.variables[name].value.value -= value.value
                    return
                elif op == '*=':
                    env.variables[name].value.value *= value.value
                    return
                elif op == '/=':
                    env.variables[name].value.value /= value.value
                    return
            env = env.previous
        newError = {
            "Tipo": "Semantico",
            "Linea": line,
            "Columna": column,
            "Ambito": self.name,
            "Descricion": "Error en la asignacion de variable"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Variable {name} not found \n column: {column} line: {line}')


    def getVariable(self, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.variables:
                return tmpEnv.variables[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        # ast.setErrors(f"La variable {id} no existe.")
        return Symbol(-1, -1, '', 0, '', ExpressionType.NULL)
    
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
            env = env.previous
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
            env = env.previous
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
        while env.previous != None:
            env = env.previous
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
            env = env.previous
        newError = {
            "Tipo": "Semantico",
            "Linea": 0,
            "Columna": 0,
            "Ambito": self.name,
            "Descricion": "Error en la obtencion de funcion"
        }
        globalenv.Errors.append(newError)
        print(f'Error: Function {id_} not found')
