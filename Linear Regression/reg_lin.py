import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import linear_model

# Dataframe
df = pd.read_csv('Dummy Data HSS.csv', sep=',')

# Informacoes Basicas
df.info()
df.describe()

# Dados Faltantes
df.isnull().mean().round(4).mul(100).sort_values(ascending=False)

# Preencher os dados
df['TV'].fillna(df['TV'].mean(),inplace=True)
df['Radio'].fillna(df['Radio'].mean(),inplace=True)
df['Social Media'].fillna(df['Social Media'].mean(),inplace=True)
df['Sales'].fillna(df['Sales'].mean(),inplace=True)


# Canais de comunicação
tipo_canal = df[["TV", "Radio", "Social Media"]]
tipo_canal.sum()

x = [i for i, _ in enumerate(tipo_canal)]
y = tipo_canal.sum()
plt.bar(x, y)
plt.xticks(x, tipo_canal)
plt.show()

# Correlação entre os canais e as vendas
corr = df.corr()
sns.heatmap(corr, annot=True)
plt.show()


sns.pairplot(data = df,
            x_vars = ['TV', 'Radio', 'Social Media'],
            y_vars = 'Sales',
            size = 5,
            kind = 'reg')
plt.show()


# Distribuição de cada canal

def distplot_canal(text):
    sns.distplot(df[text])
    plt.title(text)
    plt.show()

distplot_canal('TV')
distplot_canal('Radio')
distplot_canal('Social Media')


# Coluna Influencer
df['Influencer'].unique()

# Analisar quantidade de cada tipo de Influencer
def qntd_influencer(text):

    print(f"O influencer do tipo {text} possui um total de {len(df[df['Influencer'] == text])} e representa um total de {len(df[df['Influencer'] == text])/len(df) * 100} ")

qntd_influencer('Macro')
qntd_influencer('Micro')
qntd_influencer('Nano')
qntd_influencer('Mega')

# One-hot Encoding para o Influencer (Categorical)
df_onehot = pd.get_dummies(df, columns=['Influencer'], prefix=['Influencer'])


#divide into training and testing
X = np.asarray(df_onehot[['TV', 'Radio', 'Social Media', 'Influencer_Macro', 'Influencer_Micro', 'Influencer_Mega', 'Influencer_Nano']])
Y = np.asarray(df_onehot['Sales'])

# Treino e teste split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, shuffle= True)

# Modelo
lineReg = LinearRegression()

# Treinamento
lineReg.fit(X_train, y_train)

# Predição
lr_predict = lineReg.predict(X_test)

# Analise
print('Score: ', lineReg.score(X_test, y_test))
print('Weights: ', lineReg.coef_)
print("Mean Squarred Error:", mean_squared_error(y_test, lr_predict))


# Teste
lineReg.predict([[42,  15.96,  5,  148.20, 0, 0, 0]])


