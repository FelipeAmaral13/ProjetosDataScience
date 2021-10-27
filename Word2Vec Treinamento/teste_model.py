import os
import pickle
from model_cbow import tokenizador, combinacao_de_vetores_por_soma
from gensim.models import KeyedVectors

with open(os.path.join(os.getcwd(), 'rl_cbow.pkl'), "rb") as f:
    model = pickle.load(f)
    
w2v_modelo_cbow = KeyedVectors.load_word2vec_format(os.path.join(os.getcwd(), 'modelo_cbow.txt'))


texto_teste = "Museu abre no feirado"

teste_tokens = tokenizador(texto_teste)
teste_vetor = combinacao_de_vetores_por_soma(teste_tokens, w2v_modelo_cbow)
teste_categoria = model.predict(texto_teste)

categoria = teste_categoria[0].capitalize()