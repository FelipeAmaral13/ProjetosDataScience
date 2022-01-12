import pandas as pd
import matplotlib.pyplot as plt
import re
import os

# Lendo o banco de dados
df = pd.read_csv(os.path.join('data', 'TripAdvisor.csv'), sep=';')

# Informacoes basicas
df.info()
df.isnull().sum()

# Analise das datas dos reviews
# Regex para troca de "de" para "/"
df['DATA'] = df['DATA'].apply(lambda x: re.sub(r" de ", '/', x))

# Substiuir nome dos meses por seu respecitvo numero
df['DATA'] = df['DATA'].str.replace('janeiro', '01', regex=True)
df['DATA'] = df['DATA'].str.replace('fevereiro', '02', regex=True)
df['DATA'] = df['DATA'].str.replace('março', '03', regex=True)
df['DATA'] = df['DATA'].str.replace('abril', '04', regex=True)
df['DATA'] = df['DATA'].str.replace('maio', '05', regex=True)
df['DATA'] = df['DATA'].str.replace('junho', '06', regex=True)
df['DATA'] = df['DATA'].str.replace('julho', '07', regex=True)
df['DATA'] = df['DATA'].str.replace('agosto', '08', regex=True)
df['DATA'] = df['DATA'].str.replace('setembro', '09', regex=True)
df['DATA'] = df['DATA'].str.replace('outubro', '10', regex=True)
df['DATA'] = df['DATA'].str.replace('novembro', '11', regex=True)
df['DATA'] = df['DATA'].str.replace('dezembro', '12', regex=True)

# Transformar em tipo datetime
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')

# Colunas de ano, mes, dia e dia da semana
df['ANO'] = df['DATA'].dt.year
df['MES'] = df['DATA'].dt.month
df['DIA'] = df['DATA'].dt.day
df['DIA_SEMANA'] = df['DATA'].dt.day_name()

# 1) Qual dia da semana tem mais reviews?
df['DIA_SEMANA'].value_counts()

# 2) Qual mes tem mais reviews?
df['MES'].value_counts()


tlen = pd.Series(df['DATA'].value_counts(), index=df['DATA'])
tlen.plot(figsize=(16, 4), color='r')
plt.show()


#  Analise do RATING
df['RATING/10'] = df['RATING'].astype('int')
df['RATING/10'] = df['RATING/10']/10

# 3) Qual a media, maior e menor nota?
df['RATING/10'].mean()
min(df['RATING/10'])
max(df['RATING/10'])

# 4) Quais amostras sao nota 1(min)
df[df['RATING/10'] == 1.0]
