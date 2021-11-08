import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import hamming_loss

from skmultilearn.adapt import MLkNN

df = pd.read_csv(os.path.join(os.getcwd(), 'mpst_full_data.csv'))


# Transformar cada categoria em uma coluna
mlb = MultiLabelBinarizer()
tags = mlb.fit_transform(df["tags"].str.split(", "))
categories = mlb.classes_

# Concatenar dataframes
df = pd.concat([df, pd.DataFrame(tags, columns=mlb.classes_)], axis=1)


#### Analise Exploratoria de Dados
# Quantidade de sinopse por categoria
counts = list()
for i in categories:
    counts.append((i, df[i].sum()))
df_stats = pd.DataFrame(counts, columns=['category', 'number_of_synopsis'])

df_stats.sort_values('number_of_synopsis', ascending=False).plot(x='category', y='number_of_synopsis', kind='bar', legend=False, grid=True, figsize=(24, 6))
plt.title("Total de sinopses por categoria")
plt.ylabel('Quantidade', fontsize=12)
plt.xlabel('categoria', fontsize=12)
plt.grid(False)

# Quantidade de tags por sinopse
rowsums = df.iloc[:,6:].sum(axis=1)
x = rowsums.value_counts()

plt.figure(figsize=(12,6))
ax = sns.barplot(x.index, x.values)
plt.title("Tags por sinopse")
plt.ylabel('Quantidade', fontsize=12)
plt.xlabel('Total de categorias', fontsize=12)

# Distribuicao do tamanho do texto
plt.figure(figsize=(12,6))
sns.kdeplot(df["plot_synopsis"].str.len())
plt.show()


# Concantenando todas as categorias em uma tupla
lista_zip_tags = list(zip(df[categories[0]],df[categories[1]],df[categories[2]],df[categories[3]],df[categories[4]],df[categories[5]],df[categories[6]],df[categories[7]],df[categories[8]],
df[categories[9]],df[categories[10]],df[categories[11]],df[categories[12]],df[categories[13]],df[categories[14]],df[categories[15]],df[categories[16]],df[categories[17]],
df[categories[18]],df[categories[19]],df[categories[20]],df[categories[21]],df[categories[22]],df[categories[23]],df[categories[24]],df[categories[25]],df[categories[26]],df[categories[27]],
df[categories[28]],df[categories[29]],df[categories[30]],df[categories[31]],df[categories[32]],df[categories[33]],df[categories[34]],df[categories[35]],df[categories[36]],df[categories[37]],
df[categories[38]],df[categories[39]],df[categories[40]],df[categories[41]],df[categories[42]],df[categories[43]],df[categories[44]],df[categories[45]],df[categories[46]],df[categories[47]],
df[categories[48]],df[categories[49]],df[categories[50]],df[categories[51]],df[categories[52]],df[categories[53]],df[categories[54]],df[categories[55]],df[categories[56]],df[categories[57]],
df[categories[58]],df[categories[59]],df[categories[60]],df[categories[61]],df[categories[62]],df[categories[63]],df[categories[64]],df[categories[65]],df[categories[66]],df[categories[67]],
df[categories[68]],df[categories[69]],df[categories[70]]))

df["todas_tags"] = lista_zip_tags


#### Seperacao Treino e Teste - 80% treino
train = df[(df["split"] == "train") | (df["split"] == "val")]
test = df[df["split"] == "test"]


X_train = train['plot_synopsis']
y_train = train['todas_tags']

X_test = test['plot_synopsis']
y_test = test['todas_tags']

# Vetorizar os textos
# Tamanho do vetor de 15000 - baseado no tamanho do texto, retirar palavra com 85% de frequencia
vetorizar = TfidfVectorizer(max_features=15000, max_df=0.85)

vetorizar.fit(df.plot_synopsis)
X_train_tfidf = vetorizar.transform(X_train)
X_test_tfidf = vetorizar.transform(X_test)


### Treinamento 
# É preciso transformar os dados-labels em np.array
tags_treino_array = np.asarray(list(y_train))
tags_test_array = np.asarray(list(y_test))

# Modelo - Modelo Unico em relacao das TAGs uma contra a outra
regressao_log = LogisticRegression()
classificador_onevsrest = OneVsRestClassifier(regressao_log)

classificador_onevsrest.fit(X_train_tfidf, tags_treino_array)

#Metrica - Exact Match
resultado_onevcrest = classificador_onevsrest.score(X_test_tfidf,tags_test_array)

#Metrica - Hamming Loss
previsao_onevsrest = classificador_onevsrest.predict(X_test_tfidf)
hamming_loss_onevsrest = hamming_loss(tags_test_array, previsao_onevsrest)


### Classificador MLKNN
classificador_mlknn = MLkNN()

classificador_mlknn.fit(X_train_tfidf, tags_treino_array)

#Metrica - Exact Match
resultado_mlknn = classificador_mlknn.score(X_test_tfidf,tags_test_array)

#Metrica - Hamming Loss
previsao_mlknn = classificador_mlknn.predict(X_test_tfidf)
hamming_loss_mlknn = hamming_loss(tags_test_array, previsao_mlknn)


# Print dos resultados
print(f"Modelo OneVSRest: score: {resultado_onevcrest} & Hamming Loss: {hamming_loss_onevsrest}")
print(f"Modelo MLKNN: score: {resultado_mlknn} & Hamming Loss: {hamming_loss_mlknn}")
