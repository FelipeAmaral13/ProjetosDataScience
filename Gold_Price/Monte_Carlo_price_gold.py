# Biblioteca
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as m
import seaborn as sns
import numpy as np
from scipy.stats import norm

# Ticket
gold = yf.Ticker("GC=F")

# Pegar todo o historico
hist = gold.history(period="max")

hist['Close'].plot(figsize=(15,6))
plt.xlabel('anos', fontsize=8)
plt.ylabel('Valores', fontsize=8)
plt.title('Valores de Fechamento', fontsize=16)
plt.show()



n = len(hist)
x = np.linspace(1, n, n)
coef = np.polyfit(x, hist['Close'], 1)
tendencia = coef[1]+coef[0]*x

print(' Coeficientes tendencia linear y = ax + b')
print('a = ', coef[0], 'b = ', coef[1])

ax1 = plt.subplot(311)
ax1.plot(x, hist['Close'], '-k', x, tendencia, '-k')
ax1.fill_between(x, hist['Close'], tendencia, facecolor='gray')
plt.xlabel('dias', fontsize=8)

ax1 = plt.subplot(312)
filtro = m.detrend_linear(hist['Close'])
mi = filtro.mean()
sigma = filtro.std()
ax1.plot(x, filtro, '-k')

ax1=plt.subplot(313)
ax1.hist(np.asarray(filtro, dtype='float'), bins=10, color='black', alpha=0.4)
plt.title('Histograma da diferença entre a tendência a Gold', fontsize=8)
xmin,xmax=plt.xlim()
eixox=np.linspace(xmin,xmax,100)
eixoy=norm.pdf(eixox,mi,sigma)
ax1.plot(eixox, eixoy, '--k', linewidth=3)
plt.xlabel('Classes para diferença entre tendican e gold', fontsize=8)
plt.show()

# Simulacao de monte carlo
num = 5
dias = 10
aleat = np.zeros((dias, num))
simul = np.zeros((dias, num))
eixo = np.zeros((dias,num))
for j in range(num):
    for i in range(dias):
        eixo[i,0] = n+i
        aleat[i,j] = np.random.normal(mi, sigma/np.sqrt(n))*np.sqrt(i)
        simul[i,j] = hist['Close'][-1]+aleat[i,j]



plt.figure()
plt.plot(x[-60:], hist['Close'][-60:], '-k', linewidth=5)
plt.plot(eixo[:,0], simul, '--k', linewidth=0.7)
plt.xlabel('dias', fontsize=16)
plt.ylabel('Gold', fontsize=16)
plt.grid()
plt.title('Simulação de Monte Carlo para o Gold', fontsize=16)
plt.show()

print('Media Real (detrends) = ', float(mi))
print('Media da simulacao (detrends) = ', simul.mean())
print('Volatilidade Real (desvio padrao dos detrends passados) = ', float(sigma))
print('Volatilidade da simulacao Real (desvio padrao dos detrends futuros) = ', simul.std())
