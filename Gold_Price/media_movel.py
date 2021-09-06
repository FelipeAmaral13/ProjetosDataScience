import matplotlib.pyplot as plt
import seaborn as sns
from seaborn.rcmod import set_style
import yfinance as yf

# Ticket
gold = yf.Ticker("GC=F")

# Pegar todo o historico
df = gold.history(period="max")

# Media movel de 150 dias
df['med_mov_150'] = df['Close'].rolling(window=150, min_periods=0).mean()


# Plot do preco de fechamento e da media movel
df['Close'].plot(color='k', lw=2, alpha=0.6)
df['med_mov_150'].plot(color='b', lw=3, style='--')
plt.grid()
plt.title('Gold Histórico')
plt.legend(['Gold', 'Media Movel 150 dias'])
plt.show()

# Calculo do retorno do ativo
df['retorno'] = df['Close'].pct_change()

# Analise do desvio padrao do ativo Gold
# Analise de 10 dias do desvio padrao. A cad anova amostra(dia) é analisado a volatilidade do retorno
df['std_mov'] = df['retorno'].rolling(window=10, min_periods=0).std()

# Plot do retorno x volatilidade (desv. padrao)
df['retorno'].plot(color='r', alpha=0.4)
df['std_mov'].plot(color='g', style='-')
plt.grid()
plt.title('Retorno x Volatilidade do Gold')
plt.legend(['Retorno', 'Volatilidade - 10 dias'])
plt.show()