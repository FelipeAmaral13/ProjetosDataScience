import gensim
import numpy as np
from gensim.models import KeyedVectors
import spacy
import os
import pandas as pd


nlp = spacy.load("pt_core_news_sm", disable=["paser", "ner", "tagger", "textcat"])

w2v_modelo_cbow = KeyedVectors.load_word2vec_format(os.path.join(os.getcwd(), 'modelo_cbow.txt'))

dados_treino = pd.read_csv(os.path.join(os.getcwd(), 'articles.csv'))
artigo_treino = dados_treino[0:116938]
artigo_teste = dados_treino[116938:]

def tokenizador(texto:str)->list():
    """
    Funcao para fazer o pre-processamento criando tokens de palavras
    param: texto é o titulo da reportagem
    return: titulo tokenizados
    """    
    doc = nlp(texto)
    tokens_validos = []

    for token in doc:
        e_valido = not token.is_stop and token.is_alpha # Apenas palavras sem stopwords e alphanumerica
        if e_valido:
            tokens_validos.append(token.text.lower())

    
    return  tokens_validos




def combinacao_de_vetores_por_soma(palavras:str, modelo:gensim.models.keyedvectors.Word2VecKeyedVectors)->list():
    """
    Funcao para combinar todos os tokens recem criados
    param palavras: tokens dos titulos
    param modelo: modelo treinado do word2vec
    """

    vetor_resultante = np.zeros((1,300))

    for pn in palavras:
        try:
            vetor_resultante += modelo.get_vector(pn)

        # Tratar palavra desconhecidas (poucas ocorrencias)
        except KeyError:
            if pn.isnumeric():
                pn = "0"*len(pn)
                vetor_resultante += modelo.get_vector(pn)
            else:
                vetor_resultante += modelo.get_vector("unknown")
                

    return vetor_resultante


def matriz_vetores(textos:str, modelo):
    """
    Funcao para criar uma matriz de todo o repositorio
    """
    x = len(textos)
    y = 300
    matriz = np.zeros((x,y))

    for i in range(x):
        palavras = tokenizador(textos.iloc[i])
        matriz[i] = combinacao_de_vetores_por_soma(palavras, modelo)

    return matriz

matriz_vetores_treino_cbow = matriz_vetores(artigo_treino.title, w2v_modelo_cbow)
matriz_vetores_teste_cbow = matriz_vetores(artigo_teste.title, w2v_modelo_cbow)


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def classificador(modelo, x_treino, y_treino, x_teste, y_teste):
    RL = LogisticRegression(max_iter=800)
    RL.fit(x_treino, y_treino)
    categorias = RL.predict(x_teste)
    resultados = classification_report(y_teste, categorias)
    print(resultados)

    return RL

RL_cbow = classificador(w2v_modelo_cbow, 
                        matriz_vetores_treino_cbow, 
                        artigo_treino.category, 
                        matriz_vetores_teste_cbow,
                        artigo_teste.category)


import pickle

with open(os.path.join(os.getcwd(), 'rl_cbow.pkl'), "wb") as f:
    pickle.dump(RL_cbow, f)

