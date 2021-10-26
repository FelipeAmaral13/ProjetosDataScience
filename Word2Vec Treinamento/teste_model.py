import os
import pickle
from model_cbow import *

with open(os.path.join(os.getcwd(), 'rl_cbow.pkl'), "rb") as f:
    classificador = pickle.load(f)


texto_teste = "Uninove cria técnica de classificação de OS"

teste_tokens = tokenizador(texto_teste)
teste_vetor = combinacao_de_vetores_por_soma(teste_tokens, w2v_modelo_cbow)
teste_categoria = classificador.predict(teste_vetor)

categoria = teste_categoria[0].capitalize()