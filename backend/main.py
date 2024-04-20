from flask import Flask, jsonify, request
from flask_cors import CORS

from interpreter.abstract.environment import Environment
from interpreter.analyzer import grammar
from interpreter.abstract.generator import Generator


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    credenciales = {
        "Nombre": "Nathan Antonio Valdez Valdez",
        "Carnet": "202001568",
        "Curso": "Compiladores 2"
    }
    return jsonify(credenciales)


@app.route('/send_command', methods=['POST'])
def send_command():
    GlobalEnvironment = Environment(None, 'Global')
    gen = Generator()

    if not request.json or 'code_in' not in request.json:
        return jsonify({"error": "La solicitud debe ser un JSON y contener el campo 'code_in'"}), 400

    code_in = request.json['code_in']
    print("\n\n-------------------------------------New Request-------------------------------------")


    ast = grammar.parse(code_in, GlobalEnvironment.Errors)


    # try:
    for instruction in ast:
        instruction.Eject(GlobalEnvironment, gen)
    # except Exception as e:
    #     print(f"Ocurrió un error: {str(e)}")


    response = GlobalEnvironment.console
    global tmpSymbols
    global tmpErrors
    tmpSymbols = []
    tmpErrors = []
    tmpSymbols = GlobalEnvironment.Symbols
    tmpErrors = GlobalEnvironment.Errors

    result = {
        "response": gen.get_final_code(),
        "status": 200
    }
    return jsonify(result)

@app.route('/reports/all', methods=['POST'])
def reports():
    global tmpSymbols
    global tmpErrors
    result = {
        "symbols": tmpSymbols,
        "errors": tmpErrors
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)













    # input_text = '''var vec1:number[] = [10,20,30,40,50]'''

    # resultado = grammar.parse(input_text)

    # GlobalEnvironment = Environment(None, 'Global')

    # for instruction in resultado:
    #     instruction.Eject(GlobalEnvironment)
    # pass

