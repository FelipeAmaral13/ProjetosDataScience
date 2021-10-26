import pandas as pd
import spacy
import os
import numpy as np
from gensim.models import KeyedVectors

dados_treino = pd.read_csv(os.path.join(os.getcwd(), 'treino.csv'))

nlp = spacy.load("pt_core_news_sm")

# Pre-processamento
textos_treinamento = (titulos.lower() for titulos in dados_treino['title'])


def trata_textos(doc:str)->str:
    """
    Funcao para selecionar os tokens do texto
    param doc: texto a ser tratado
    """
    tokens_validos = list()
    for token in doc:
        e_valido = not token.is_stop and token.is_alpha # Token nao é stopwords e caracter valido
        if e_valido:
            tokens_validos.append(token.text)

        if len(tokens_validos) > 2: # Se token possui mais de 3 palavras
            return " ".join(tokens_validos)

# Otimizacao para criaçao dos textos tratados
textos_tratdados = [trata_textos(doc) for doc in nlp.pipe(textos_treinamento, batch_size=1000, n_process=-1)]


# Dataframe dos textos tratados
titulos_tratados = pd.DataFrame({"titulo": textos_tratdados})

# Removendo linhas vazias e duplicatas
titulos_tratados = titulos_tratados.dropna().drop_duplicates()

# Treinamento 
from gensim.models import Word2Vec
import logging

# Gerar log - tempo e interacao
logging.basicConfig(format="%(asctime)s : - %(message)s", level = logging.INFO)

# Usar o CBOW para treinamento, considerando 2 palavras antes e depois, tamanho do vetor do w2v, considerar palavras raras, tx aprendizado (alpha)
w2v_modelo = Word2Vec(sg=0, window=2, size=300, min_count=5, alpha = 0.03, min_alpha=0.007)

# Lista de lista dos tokens
lista_lista_tokens = [titulo.split(" ") for titulo in titulos_tratados.titulo]

# Construir vocabulario e informar com log a cada 5000 interacoes
w2v_modelo.build_vocab(lista_lista_tokens,  progress_per=5000)

# Modelo - lista_lista_tokens, total de amostras e epocas
w2v_modelo.train(lista_lista_tokens, total_examples=w2v_modelo.corpus_count, epochs=30)

# Simlaridade entre as palavras
w2v_modelo.wv.most_similar("amazon")


# Salvar o modelo
w2v_modelo.wv.save_word2vec_format(os.path.join(os.getcwd(), 'modelo_cbow_new.txt'), binary=False)


