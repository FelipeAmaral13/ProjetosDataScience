# !C:\Program Files\Python38\python.exe

# Biblioteca
import pandas as pd
import flair
import string
import spacy
import re
import swifter

pln = spacy.load('en_core_web_sm')
stop_words = spacy.lang.en.stop_words.STOP_WORDS


# Banco de dados
df = pd.read_csv('covid19_tweets.csv')

# Analise basicas
df.head()
df.info()

# Col Datas
df['date'] =  pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S.%f')

# Colunas de ano, mes e dia
df['year']= df['date'].dt.year
df['month']= df['date'].dt.month
df['day']= df['date'].dt.day

# Coluna de dias da semana
dw_mapping={
    0: 'Segunda', 
    1: 'Terca', 
    2: 'Quarta', 
    3: 'Quinta', 
    4: 'Sexta',
    5: 'Sabado', 
    6: 'Domingo'
} 
df['day_of_week_name']=df['date'].dt.weekday.map(dw_mapping)

# Quais dias da semana tem mais tweet?
df['day_of_week_name'].value_counts()


# Analise da coluna user_location
df['user_location'].nunique()
df['user_location'].value_counts()[:10]



# Limpando os tweets
def preprocessamento(texto):
    
    texto = texto.lower() # Texto em letras minusculas
    texto = re.sub(r"@[A-Za-z0-9$-_@.&+]+", ' ', texto) # Remover os "@"
    texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto) # Remover links
    texto = re.sub(r" +", ' ', texto)   # Remover mais de uma espaco faltante

    documento = pln(texto) # Criar doc. para Spacy
    
    # Criar tokens
    lista = []
    for token in documento:
      lista.append(token.lemma_)

    # Remover stopwords e pontuacao
    lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in string.punctuation]
    
    # Juntar as frases
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

    return lista

# Aplicar a funcao na coluna de tweets
df['text'] = df['text'].swifter.apply(preprocessamento)


# Criar o modelo para o Flair
modelo = flair.models.TextClassifier.load('en-sentiment')

# Quantidade de tokens 
df['Qntd_tokens'] = [flair.data.Sentence(df['text'][i]) for i in range(len(df['text']))]

# Criar coluna de classficiacao dos tweets
classifications = []
for i in range(len(df['text'])):
    sentence = flair.data.Sentence(df['text'][i])
    modelo.predict(sentence)
    classifications.append(sentence.labels)

df['Class'] = pd.DataFrame(classifications)




