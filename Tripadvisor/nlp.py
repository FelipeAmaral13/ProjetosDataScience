import pandas as pd
import re
import swifter
import string
from leia import SentimentIntensityAnalyzer 
from collections import Counter
from nltk.corpus import stopwords

# remover stopwords
STOPWORDS = list(set(stopwords.words('portuguese'))) 

# Lendo o banco de dados
df = pd.read_csv('TripAdvisor.csv', sep=';')

# remover pontuacao
def data_clean(text):
    no_punctuation = "".join(c for c in text if c not in string.punctuation)
    str_lower = "".join(text.lower() for text in no_punctuation )
    no_brackets = "".join(re.sub(r'\[[0-9]*\]', ' ', text) for text in str_lower)
    no_special_char = "".join(re.sub(r'\s+', ' ', text) for text in no_brackets)
    remove_stopwords = " ".join([word for word in str(no_special_char).split() if word not in STOPWORDS])


    return remove_stopwords	

df['OS_CLEAN'] = df['REVIEW'].swifter.apply(lambda x: data_clean(x))

#----> Verificar as palavras "Comuns" e "Raras"
# remover palavras mais frequentes
cnt = Counter()
for text in df["OS_CLEAN"].values:
    for word in text.split():
        cnt[word] += 1
        
cnt.most_common(10)


### --------------------------- Analises dos RAVIEWS
# Limpando as mensagens
msgm = []
for i in range(len(df)):
    try:
        texto  = df['OS_CLEAN'][i]
        # limpando a conversa
        texto = texto.replace('\t', '')
        texto = texto.replace('\n', '')
        texto = texto.replace('\r', '')
        texto = texto.replace('\xa0', '')

        # Dividindo as linhas dos texto
        texto = texto.split('<\\br>')
        msgm.append(texto)
    except :
        print(i)


### -------------------------- Limpeza de dados

# Analise de sentimentos das conversas
s = SentimentIntensityAnalyzer()

for j in range(len(msgm))[:5]:

    # Análise de texto simples
    for i in range(len(msgm[j])):
        print(f'Mensagem: {msgm[j][i]}')
        s.polarity_scores(msgm[j][i])
    print('-----------------------------------------------')

# Coluna de Scores calculados da analise de sentimentos
df['SCORES'] = df['OS_CLEAN'].apply(lambda review: s.polarity_scores(review))

# Coluna do Scores normalizado (-1 a +1)
df['COMPOUND']  = df['SCORES'].apply(lambda score_dict: score_dict['compound'])

# Coluna para a classificacao Pos ou Neg da menssagem
df['COMP_SCORES'] = df['COMPOUND'].apply(lambda c: 'pos' if c >=0 else 'neg')

# CALCULAR A PROPORCAO DE MENSAGENS POS E NEG
df['COMP_SCORES'].value_counts()


df['SCORES'] = df['RATING'].astype('int')
df['RATING/10'] = df['RATING']/ 10


# Analise das mensagens negativas e com Rating menor/igual que 4
df_negativa = df[(df['COMP_SCORES'] == 'neg') & (df['COMPOUND'] <= -0.405)]



# Classificacao dos reviews com MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


#Tokenizar e  remover elementos desnecessario (simbolos)
token = RegexpTokenizer(r'[a-zA-Z0-9]+')

# CountVectorizer 
cv = CountVectorizer(ngram_range = (1,1), tokenizer = token.tokenize)

text_counts= cv.fit_transform(df['OS_CLEAN'])


# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(text_counts, df['COMP_SCORES'] , test_size=0.3, random_state=1)


# Model Generativo usando Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)

predicted= clf.predict(X_test)

print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))