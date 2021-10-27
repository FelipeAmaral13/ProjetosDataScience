import pandas as pd
import spacy
import os
import numpy as np
import gensim
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import logging
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


nlp = spacy.load("pt_core_news_sm")

# Separando os dados de treino
dados_treino = pd.read_csv(os.path.join(os.getcwd(), 'articles.csv'))
dados_treino = dados_treino[0:116938]

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
# Gerar log - tempo e interacao
logging.basicConfig(format="%(asctime)s : - %(message)s", level = logging.INFO)

# Usar o CBOW para treinamento, considerando 2 palavras antes e depois, tamanho do vetor do w2v, considerar palavras raras, tx aprendizado (alpha)
w2v_modelo = Word2Vec(sg=0, window=2, size=300, min_count=5, alpha = 0.03, min_alpha=0.007)

# Lista de lista dos tokens
lista_lista_tokens = [titulo.split(" ") for titulo in titulos_tratados.titulo]

# Construir vocabulario e informar com log a cada 5000 interacoes
w2v_modelo.build_vocab(lista_lista_tokens,  progress_per=5000)

# Modelo - lista_lista_tokens, total de amostras e epocas
w2v_modelo.train(lista_lista_tokens, total_examples=w2v_modelo.corpus_count, epochs=100)

# Visualizacao das palavras próximas 

def display_closestwords_tsnescatterplot(model:gensim.models.word2vec.Word2Vec, word:str, size:int):

    """
    Funcao para plotar as palavras proximas de uma especifica palavra.
    param model: modelo treinado do gensim.Word2Vec
    param word: palavra-alvo
    param size: tamanho que modelo gensim.Word2Vec foi treinado
    """
    
    arr = np.empty((0,size), dtype='f')
    word_labels = [word]

    close_words = model.wv.similar_by_word(word)
    
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    tsne = TSNE(n_components=2)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)
    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    plt.scatter(x_coords, y_coords)
    
    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    # plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    # plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()

display_closestwords_tsnescatterplot(w2v_modelo, 'usp', 300) 

# Simlaridade entre as palavras
w2v_modelo.wv.most_similar("vasco")

# Salvar o modelo
w2v_modelo.wv.save_word2vec_format(os.path.join(os.getcwd(), 'modelo_cbow.txt'), binary=False)

