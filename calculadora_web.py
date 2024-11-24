from flask import Flask, render_template, request


app = Flask(__name__)


def suma(num1, num2):
    return num1 + num2

def resta(num1, num2):
    return num1 - num2

def multiplicacion(num1, num2):
    return num1 * num2

def division(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Error: División entre cero no permitida"


@app.route('/')
def index():
    return render_template('calculadora.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operacion = request.form['operacion']

   
    if operacion == 'suma':
        resultado = suma(num1, num2)
    elif operacion == 'resta':
        resultado = resta(num1, num2)
    elif operacion == 'multiplicacion':
        resultado = multiplicacion(num1, num2)
    elif operacion == 'division':
        resultado = division(num1, num2)
    else:
        resultado = "Operación no válida"

  
    return render_template('calculadora.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
