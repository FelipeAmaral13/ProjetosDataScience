# Lab - Deploy na Prática - App Web Para Previsão de Preço de Produtos
# app flask

# Imprts
from flask import Flask, request
from flask import render_template
from tools.heart import Heart

# Cria a app
app = Flask(__name__)

# Página de entrada
@app.route("/")
def index():
    result = None
    return render_template("index.html", result = result)

# Página com resultado da previsão
@app.route("/estimate", methods = ["POST"])
def estimate():
    values = request.form.getlist('new_car')
    print(values)
    car = Heart(values)
    value_to_predict = car.prepare()
    result = car.predict(value_to_predict)
    result = "%.0f" % result
    return render_template('index.html', result = result)

# Executa a app
if __name__ == "__main__":
    app.run(host = 'localhost', port = 8080, debug = True)
