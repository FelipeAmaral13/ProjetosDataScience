import pandas as pd

df = pd.read_csv('framingham.csv')

# Analise basica
df.info()

# Proporcao de dados faltantes
dados_faltantes = df.isnull().sum() / df.shape[0] * 100.00

