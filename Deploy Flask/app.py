from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import pickle
import numpy as np


# Colunas do modelo
colunas = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
           'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']

# Ler o modelo treinado
modelo = pickle.load(open('modelo.pkl','rb'))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'teste'
app.config['BASIC_AUTH_PASSWORD'] = 'teste_post'

basic_auth = BasicAuth(app)


@app.route('/api/', methods=['POST'])
@basic_auth.required
def api():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    predicao = modelo.predict(np.array(dados_input).reshape(1, -1))
    return jsonify(predicao=predicao[0])

app.run(debug=True)